from __future__ import annotations

from pathlib import Path

import pytest

from poseguide.render.overlay import (
    VisionUnavailableError,
    render_overlay_png,
    write_guidance_overlay,
)

# The PNG renderer needs the optional ``vision`` extra (opencv + numpy). CI's
# ``[dev]`` install does not pull it in, so skip only the cv2-dependent tests
# when the extra is absent — the JSON path and error-message tests still run.
try:
    import cv2  # noqa: F401

    _HAS_CV2 = True
except ImportError:
    _HAS_CV2 = False

_needs_cv2 = pytest.mark.skipif(not _HAS_CV2, reason="vision extra (opencv) not installed")


def test_write_guidance_overlay_json(tmp_path: Path) -> None:
    out = tmp_path / "guidance.json"
    path = write_guidance_overlay({"pose": "contrapposto"}, out)
    assert path.exists()
    assert "poseguide.overlay.v1" in path.read_text(encoding="utf-8")


@_needs_cv2
def test_render_overlay_png_target_only(tmp_path: Path) -> None:
    out = tmp_path / "overlay.png"
    result = render_overlay_png("contrapposto", out)
    assert result == out
    assert out.exists()
    assert out.stat().st_size > 0
    # PNG magic bytes
    assert out.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


@_needs_cv2
def test_render_overlay_png_with_subject(tmp_path: Path) -> None:
    out = tmp_path / "overlay_subject.png"
    subject = {
        "nose": [0.5, 0.08],
        "l_shoulder": [0.4, 0.2],
        "r_shoulder": [0.6, 0.2],
        "l_hip": [0.42, 0.55],
        "r_hip": [0.58, 0.55],
    }
    result = render_overlay_png("contrapposto", out, subject_joints=subject)
    assert result.exists()
    assert result.stat().st_size > 0


@_needs_cv2
def test_render_overlay_png_unknown_pose(tmp_path: Path) -> None:
    with pytest.raises(KeyError):
        render_overlay_png("not-a-real-pose", tmp_path / "x.png")


@_needs_cv2
def test_render_overlay_png_custom_size(tmp_path: Path) -> None:
    out = tmp_path / "sized.png"
    render_overlay_png("contrapposto", out, width=200, height=200)
    cv2, _ = __import__("poseguide.render.overlay", fromlist=["_require_cv2"])._require_cv2()
    img = cv2.imread(str(out))
    assert img.shape[0] == 200
    assert img.shape[1] == 200


def test_vision_unavailable_error_message_mentions_extra(monkeypatch) -> None:
    import poseguide.render.overlay as ov

    def _boom():
        raise ov.VisionUnavailableError(
            "PNG overlay needs the vision extra: pip install 'poseguide[vision]'"
        )

    monkeypatch.setattr(ov, "_require_cv2", _boom)
    with pytest.raises(VisionUnavailableError, match="vision"):
        ov.render_overlay_png("contrapposto", __import__("pathlib").Path("/tmp/never.png"))
