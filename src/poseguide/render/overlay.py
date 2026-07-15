from __future__ import annotations

import json
from pathlib import Path

from poseguide.models.catalog import get_pose_by_id
from poseguide.render.svg import EDGES

# ---------------------------------------------------------------------------
# JSON guidance payload (dependency-free, always available)
# ---------------------------------------------------------------------------


def write_guidance_overlay(result: dict, out_path: Path) -> Path:
    """Write a JSON guidance payload a camera UI could consume.

    This is the dependency-free path. For a rendered PNG skeleton overlay use
    :func:`render_overlay_png` (requires the ``vision`` extra).
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "kind": "poseguide.overlay.v1",
        "result": result,
        "draw_hints": [
            {"type": "skeleton", "source": "target_pose"},
            {"type": "text_banner", "text": "Align your stance with the guide"},
        ],
    }
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return out_path


# ---------------------------------------------------------------------------
# PNG skeleton overlay (OpenCV) — issue #7
# ---------------------------------------------------------------------------

# BGR colors (OpenCV uses BGR order)
_TARGET_COLOR = (233, 158, 14)  # amber-ish for the target/guide pose
_SUBJECT_COLOR = (113, 204, 46)  # green for the live subject
_JOINT_TARGET = (161, 105, 3)
_JOINT_SUBJECT = (46, 137, 22)


class VisionUnavailableError(RuntimeError):
    """Raised when the optional ``vision`` extra (opencv) is not installed."""


def _require_cv2():
    try:
        import cv2  # noqa: PLC0415
        import numpy as np  # noqa: PLC0415
    except ImportError as exc:  # pragma: no cover - exercised via monkeypatch
        raise VisionUnavailableError(
            "PNG overlay needs the vision extra: pip install 'poseguide[vision]'"
        ) from exc
    return cv2, np


def _joint_points(joints: dict, w: int, h: int) -> dict[str, tuple[int, int]]:
    """Convert normalized [0..1] joint coords into pixel points."""
    pts: dict[str, tuple[int, int]] = {}
    for name, xyz in (joints or {}).items():
        if not isinstance(xyz, (list, tuple)) or len(xyz) < 2:
            continue
        pts[name] = (int(round(float(xyz[0]) * w)), int(round(float(xyz[1]) * h)))
    return pts


def _draw_skeleton(img, joints: dict, w: int, h: int, line_color, joint_color) -> None:
    cv2, _ = _require_cv2()
    pts = _joint_points(joints, w, h)
    for a, b in EDGES:
        if a in pts and b in pts:
            cv2.line(img, pts[a], pts[b], line_color, 3, lineType=cv2.LINE_AA)
    for p in pts.values():
        cv2.circle(img, p, 5, joint_color, -1, lineType=cv2.LINE_AA)


def render_overlay_png(
    target_pose_id: str,
    out_path: Path,
    *,
    subject_joints: dict | None = None,
    background: Path | None = None,
    width: int = 360,
    height: int = 480,
) -> Path:
    """Render target (and optional subject) skeleton onto an image, save PNG.

    - ``target_pose_id``: pose id from the catalog whose joints form the guide.
    - ``subject_joints``: optional dict of normalized joints for the live
      subject, drawn in a second color so the user can align.
    - ``background``: optional image path to draw on; a dark canvas is used
      when omitted or unreadable.

    Requires the ``vision`` extra (``opencv-python-headless``). Raises
    :class:`VisionUnavailableError` when it is missing so callers can fall back
    to :func:`write_guidance_overlay`.
    """
    cv2, np = _require_cv2()

    pose = get_pose_by_id(target_pose_id)
    if pose is None:
        raise KeyError(f"unknown pose {target_pose_id!r}")

    img = None
    if background is not None:
        img = cv2.imread(str(background))
        if img is not None:
            img = cv2.resize(img, (width, height))
    if img is None:
        img = np.full((height, width, 3), 15, dtype=np.uint8)  # dark slate canvas

    _draw_skeleton(img, pose.get("joints") or {}, width, height, _TARGET_COLOR, _JOINT_TARGET)
    if subject_joints:
        _draw_skeleton(img, subject_joints, width, height, _SUBJECT_COLOR, _JOINT_SUBJECT)

    title = str(pose.get("name") or target_pose_id)
    cv2.putText(
        img, title, (12, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (226, 232, 240), 1, cv2.LINE_AA
    )
    legend = "amber=guide  green=you" if subject_joints else "amber=guide"
    cv2.putText(
        img,
        legend,
        (12, height - 14),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.4,
        (148, 163, 184),
        1,
        cv2.LINE_AA,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(out_path), img):  # pragma: no cover - fs failure
        raise OSError(f"failed to write PNG to {out_path}")
    return out_path
