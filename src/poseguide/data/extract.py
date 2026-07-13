"""Extract a normalized standing skeleton from a still image.

The public entry point is :func:`extract_pose`, which takes an image path and a
landmark *detector* and returns a subject payload compatible with the rest of
PoseGuide (same ``joints`` schema used by ``data/samples/*.json`` and consumed
by :func:`poseguide.data.loader.joints_to_vector`).

The detector is injected (dependency injection) so the mapping logic can be
tested with a fake detector returning known landmarks — no MediaPipe binary or
model download required for the unit tests. In production the default detector
wraps MediaPipe Pose, imported lazily so the ``vision`` extra stays optional.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol, Sequence

# Repo joint schema (matches loader.joints_to_vector order).
JOINT_KEYS: tuple[str, ...] = (
    "nose",
    "l_shoulder",
    "r_shoulder",
    "l_elbow",
    "r_elbow",
    "l_wrist",
    "r_wrist",
    "l_hip",
    "r_hip",
    "l_knee",
    "r_knee",
    "l_ankle",
    "r_ankle",
)

# MediaPipe Pose landmark index -> repo joint key.
# MediaPipe "left/right" is the *subject's* anatomical side; we preserve that
# naming (LEFT -> l_, RIGHT -> r_) so joint keys stay semantically consistent.
MEDIAPIPE_LANDMARK_MAP: dict[int, str] = {
    0: "nose",
    11: "l_shoulder",
    12: "r_shoulder",
    13: "l_elbow",
    14: "r_elbow",
    15: "l_wrist",
    16: "r_wrist",
    23: "l_hip",
    24: "r_hip",
    25: "l_knee",
    26: "r_knee",
    27: "l_ankle",
    28: "r_ankle",
}


class Landmark(Protocol):
    """Minimal shape of a single MediaPipe pose landmark."""

    x: float
    y: float
    z: float
    visibility: float


class LandmarkDetector(Protocol):
    """Anything that turns an image path into a flat list of landmarks.

    The list is indexed by the MediaPipe Pose landmark index (0..32). A
    detector may return ``None`` when no person is found.
    """

    def __call__(self, image_path: Path) -> Sequence[Landmark] | None: ...


def landmarks_to_joints(
    landmarks: Sequence[Landmark],
) -> tuple[dict[str, list[float]], dict[str, float]]:
    """Map a MediaPipe landmark list to the repo joint schema.

    Returns ``(joints, visibility)`` where ``joints[key]`` is ``[x, y, z]`` in
    normalized image space and ``visibility[key]`` is the detector confidence.
    Missing landmarks default to ``[0, 0, 0]`` with ``0.0`` visibility.
    """
    joints: dict[str, list[float]] = {}
    visibility: dict[str, float] = {}
    for index, key in MEDIAPIPE_LANDMARK_MAP.items():
        if index < len(landmarks) and landmarks[index] is not None:
            lm = landmarks[index]
            joints[key] = [
                round(float(lm.x), 6),
                round(float(lm.y), 6),
                round(float(getattr(lm, "z", 0.0)), 6),
            ]
            visibility[key] = round(float(getattr(lm, "visibility", 1.0)), 6)
        else:
            joints[key] = [0.0, 0.0, 0.0]
            visibility[key] = 0.0
    return joints, visibility


def extract_pose(
    image_path: str | Path,
    detector: LandmarkDetector | None = None,
    *,
    subject_id: str | None = None,
) -> dict:
    """Extract a subject skeleton from a still image.

    Parameters
    ----------
    image_path:
        Path to the source photo.
    detector:
        Injectable landmark detector. When ``None`` the default MediaPipe-backed
        detector is created lazily (requires the ``vision`` extra).
    subject_id:
        Optional id for the payload; defaults to the image file stem.

    Returns
    -------
    dict
        Subject payload with ``id``, ``source``, ``joints`` and ``visibility``,
        matching the schema in ``data/samples/*.json``.

    Raises
    ------
    FileNotFoundError
        If ``image_path`` does not exist.
    RuntimeError
        If the detector finds no person in the image.
    """
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    if detector is None:
        detector = default_mediapipe_detector()

    landmarks = detector(path)
    if not landmarks:
        raise RuntimeError(f"No pose landmarks detected in image: {path}")

    joints, visibility = landmarks_to_joints(landmarks)
    return {
        "id": subject_id or path.stem,
        "source": "mediapipe-extract",
        "image": path.name,
        "joints": joints,
        "visibility": visibility,
    }


def extract_to_file(
    image_path: str | Path,
    out_path: str | Path,
    detector: LandmarkDetector | None = None,
    *,
    subject_id: str | None = None,
) -> Path:
    """Extract a pose and write the subject JSON to ``out_path``."""
    payload = extract_pose(image_path, detector, subject_id=subject_id)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return out


def default_mediapipe_detector(model_asset_path: str | Path | None = None) -> LandmarkDetector:
    """Build a detector backed by MediaPipe Pose (lazy, optional import).

    Supports both MediaPipe APIs:

    * The modern **Tasks** API (``mediapipe.tasks`` / ``PoseLandmarker``), which
      needs a downloaded ``.task`` model asset. Pass ``model_asset_path`` or set
      the ``POSEGUIDE_POSE_MODEL`` environment variable.
    * The legacy **solutions** API (``mediapipe.solutions.pose``) when present,
      which bundles its own model.

    Raises
    ------
    RuntimeError
        With a clear, actionable message if the ``vision`` extra is missing, or
        if only the Tasks API is available but no model asset was provided.
    """
    import os

    try:
        import cv2  # type: ignore
        import mediapipe as mp  # type: ignore
    except ImportError as exc:  # pragma: no cover - exercised only without extra
        raise RuntimeError(
            "MediaPipe pose extraction requires the optional 'vision' extra. "
            "Install it with: pip install 'poseguide[vision]'"
        ) from exc

    solutions = getattr(mp, "solutions", None)
    if solutions is not None and hasattr(solutions, "pose"):

        def _detect_legacy(image_path: Path) -> Sequence[Landmark] | None:  # pragma: no cover
            image = cv2.imread(str(image_path))
            if image is None:
                raise RuntimeError(f"Could not read image: {image_path}")
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            with solutions.pose.Pose(static_image_mode=True) as pose:
                result = pose.process(rgb)
            if not result.pose_landmarks:
                return None
            return list(result.pose_landmarks.landmark)

        return _detect_legacy

    # Modern Tasks API (PoseLandmarker) — requires a model asset.
    model_path = str(model_asset_path or os.getenv("POSEGUIDE_POSE_MODEL", "")).strip()
    if not model_path:
        raise RuntimeError(
            "This MediaPipe build exposes only the Tasks API (PoseLandmarker), "
            "which needs a pose landmarker model. Provide model_asset_path or set "
            "POSEGUIDE_POSE_MODEL to a downloaded .task file "
            "(https://developers.google.com/mediapipe/solutions/vision/pose_landmarker)."
        )

    def _detect_tasks(image_path: Path) -> Sequence[Landmark] | None:  # pragma: no cover
        from mediapipe.tasks import python as mp_python
        from mediapipe.tasks.python import vision as mp_vision

        base_options = mp_python.BaseOptions(model_asset_path=model_path)
        options = mp_vision.PoseLandmarkerOptions(base_options=base_options)
        with mp_vision.PoseLandmarker.create_from_options(options) as landmarker:
            mp_image = mp.Image.create_from_file(str(image_path))
            result = landmarker.detect(mp_image)
        if not result.pose_landmarks:
            return None
        return list(result.pose_landmarks[0])

    return _detect_tasks
