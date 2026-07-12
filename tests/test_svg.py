from __future__ import annotations

from pathlib import Path

from poseguide.guide.demo import run_demo
from poseguide.render.svg import render_pose_svg


def test_render_pose_svg(tmp_path: Path) -> None:
    out = tmp_path / "pose.svg"
    path = render_pose_svg("contrapposto", out)
    text = path.read_text(encoding="utf-8")
    assert "<svg" in text
    assert "line" in text or "circle" in text


def test_run_demo_beach() -> None:
    result = run_demo("beach")
    assert result["recommendations"]
    assert Path(result["svg_path"]).exists()
