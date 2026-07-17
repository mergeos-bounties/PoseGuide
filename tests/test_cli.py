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


def test_pose_list_filters_by_tag_and_difficulty() -> None:
    result = runner.invoke(app, ["poses", "list", "--tag", "power", "--difficulty", "easy"])

    assert result.exit_code == 0
    assert "arms_crossed_power" in result.output
    assert "jump_midair_arms_open" not in result.output


def test_pose_search_accepts_filters_without_query() -> None:
    result = runner.invoke(app, ["poses", "search", "--tag", "jump", "--difficulty", "medium"])

    assert result.exit_code == 0
    assert "Jump Midair Arms" in result.output
    assert "Arms Crossed Power" not in result.output
    assert "filters" in result.output


def test_pose_search_rejects_unknown_difficulty() -> None:
    result = runner.invoke(app, ["poses", "search", "--difficulty", "extreme"])

    assert result.exit_code == 2
    assert "easy, medium, hard" in result.output
