from __future__ import annotations

from typer.testing import CliRunner

from poseguide.cli import app


runner = CliRunner()


def test_pose_search_matches_tips() -> None:
    result = runner.invoke(app, ["poses", "search", "fingertips"])

    assert result.exit_code == 0
    assert "arms_raised" in result.output
    assert "tips" in result.output


def test_pose_search_matches_camera_cues() -> None:
    result = runner.invoke(app, ["poses", "search", "headroom"])

    assert result.exit_code == 0
    assert "hands_in_pockets" in result.output
    assert "camera_cues" in result.output
