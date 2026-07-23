from __future__ import annotations

import pytest
from typer.testing import CliRunner

from poseguide.cli import app
from poseguide.guide import demo as demo_module


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


def test_pose_show_known_id() -> None:
    result = runner.invoke(app, ["poses", "show", "arms_crossed"])

    assert result.exit_code == 0
    assert "arms_crossed" in result.output
    assert "joints" in result.output


def test_pose_show_unknown_id() -> None:
    result = runner.invoke(app, ["poses", "show", "nonexistent"])

    assert result.exit_code == 1
    assert "not found" in result.output


@pytest.mark.parametrize("preset", ["beach", "urban", "studio"])
def test_guide_demo_prints_top_pose(preset: str, tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(demo_module, "OUT_DIR", tmp_path)

    result = runner.invoke(app, ["guide", "demo", "--preset", preset])

    assert result.exit_code == 0
    assert f'"preset": "{preset}"' in result.output
    assert '"top_pose_id":' in result.output
    assert "Top pose" in result.output
