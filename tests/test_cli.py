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


def test_poses_show_table_output() -> None:
    """poseguide poses show <id> prints a Rich table with fields and joints."""
    result = runner.invoke(app, ["poses", "show", "yoga_tree"])

    assert result.exit_code == 0
    assert "Yoga Tree Pose" in result.output
    assert "yoga_tree" in result.output
    assert "indoor" in result.output or "yoga" in result.output
    assert "Joints" in result.output
    assert "nose" in result.output
    assert "l_shoulder" in result.output


def test_poses_show_json_output() -> None:
    """poseguide poses show <id> --json prints clean JSON."""
    result = runner.invoke(app, ["poses", "show", "yoga_tree", "--json"])

    assert result.exit_code == 0
    assert '"id"' in result.output
    assert '"name"' in result.output
    assert '"joints"' in result.output
    # joint_vector (numpy) should NOT be in JSON output
    assert "joint_vector" not in result.output


def test_poses_show_not_found() -> None:
    """poseguide poses show with a nonexistent ID exits with error."""
    result = runner.invoke(app, ["poses", "show", "nonexistent_pose_xyz"])

    assert result.exit_code == 1
    assert "not found" in result.output
