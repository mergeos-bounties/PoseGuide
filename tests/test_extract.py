from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest

from poseguide.data.extract import (
    JOINT_KEYS,
    MEDIAPIPE_LANDMARK_MAP,
    extract_pose,
    extract_to_file,
    landmarks_to_joints,
)
from poseguide.data.loader import joints_to_vector


@dataclass
class FakeLandmark:
    x: float
    y: float
    z: float = 0.0
    visibility: float = 1.0


def _fake_landmarks() -> list[FakeLandmark]:
    """A full 33-entry MediaPipe landmark list with known values at mapped indices."""
    landmarks = [FakeLandmark(0.0, 0.0, 0.0, 0.0) for _ in range(33)]
    for index, key in MEDIAPIPE_LANDMARK_MAP.items():
        # Encode the index into coordinates so we can assert exact mapping.
        landmarks[index] = FakeLandmark(
            x=index / 100.0,
            y=index / 50.0,
            z=index / 200.0,
            visibility=0.9,
        )
    return landmarks


def _fake_detector(landmarks):
    def _detect(image_path: Path):
        return landmarks

    return _detect


def test_landmarks_map_to_repo_joint_keys() -> None:
    joints, visibility = landmarks_to_joints(_fake_landmarks())
    # Same joint keys the rest of the library uses.
    assert set(joints) == set(JOINT_KEYS)
    assert set(visibility) == set(JOINT_KEYS)
    # Values map from the correct MediaPipe indices.
    assert joints["nose"] == [0.0, 0.0, 0.0]  # index 0
    assert joints["l_shoulder"] == [0.11, 0.22, 0.055]  # index 11
    assert joints["r_shoulder"] == [0.12, 0.24, 0.06]  # index 12
    assert joints["r_ankle"] == [0.28, 0.56, 0.14]  # index 28
    assert visibility["l_shoulder"] == 0.9


def test_extract_pose_returns_subject_payload(tmp_path: Path) -> None:
    image = tmp_path / "subject.jpg"
    image.write_bytes(b"not-a-real-image-but-file-exists")

    payload = extract_pose(image, detector=_fake_detector(_fake_landmarks()))

    assert payload["id"] == "subject"
    assert payload["source"] == "mediapipe-extract"
    assert set(payload["joints"]) == set(JOINT_KEYS)
    # Output feeds the existing loader vectorizer (13 joints * 3 coords).
    assert joints_to_vector(payload["joints"]).shape == (39,)


def test_extract_to_file_writes_valid_json(tmp_path: Path) -> None:
    import json

    image = tmp_path / "photo.png"
    image.write_bytes(b"fake")
    out = tmp_path / "nested" / "custom.json"

    written = extract_to_file(image, out, detector=_fake_detector(_fake_landmarks()))

    assert written == out
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["id"] == "photo"
    assert set(data["joints"]) == set(JOINT_KEYS)


def test_missing_image_raises_clear_error(tmp_path: Path) -> None:
    missing = tmp_path / "does_not_exist.jpg"
    with pytest.raises(FileNotFoundError, match="Image not found"):
        extract_pose(missing, detector=_fake_detector(_fake_landmarks()))


def test_no_person_detected_raises_runtime_error(tmp_path: Path) -> None:
    image = tmp_path / "empty.jpg"
    image.write_bytes(b"fake")
    with pytest.raises(RuntimeError, match="No pose landmarks"):
        extract_pose(image, detector=_fake_detector(None))


def test_missing_landmark_defaults_to_zero() -> None:
    # A short list missing the leg landmarks.
    short = [FakeLandmark(0.5, 0.5, 0.0, 0.8) for _ in range(13)]
    joints, visibility = landmarks_to_joints(short)
    assert joints["r_ankle"] == [0.0, 0.0, 0.0]
    assert visibility["r_ankle"] == 0.0


def test_real_mediapipe_smoke(tmp_path: Path) -> None:
    """Live smoke test — only runs when the vision extra is installed.

    Skips cleanly if the installed MediaPipe build only ships the Tasks API
    (PoseLandmarker) with no bundled model, since downloading the ``.task``
    asset is out of scope for the unit suite. This never requires the heavy
    binary for the suite to pass.
    """
    mp = pytest.importorskip("mediapipe")
    cv2 = pytest.importorskip("cv2")
    import numpy as np

    from poseguide.data.extract import default_mediapipe_detector

    solutions = getattr(mp, "solutions", None)
    if solutions is None or not hasattr(solutions, "pose"):
        # Tasks-only build: default_mediapipe_detector() raises without a model.
        with pytest.raises(RuntimeError, match="Tasks API"):
            default_mediapipe_detector()
        pytest.skip("MediaPipe Tasks-only build; legacy solutions.pose unavailable")

    # Legacy solutions API present: blank image -> no person -> RuntimeError.
    image = tmp_path / "blank.png"
    cv2.imwrite(str(image), np.zeros((256, 256, 3), dtype=np.uint8))
    detector = default_mediapipe_detector()
    with pytest.raises(RuntimeError):
        extract_pose(image, detector=detector)
