"""Tests for SVG render."""

import json
from pathlib import Path
from poseguide.render import render_pose_svg, render_all_poses

def test_render_pose_svg():
    pose = {"joints": {"head": [0, 1.7, 0], "hips": [0, 1.0, 0]}}
    svg = render_pose_svg(pose)
    assert "<svg" in svg
    assert "head" in svg

def test_render_all_poses(tmp_path):
    poses_dir = tmp_path / "poses"
    poses_dir.mkdir()
    (poses_dir / "test.json").write_text(json.dumps({"joints": {"head": [0, 1, 0]}}))
    
    output = tmp_path / "output"
    count = render_all_poses(poses_dir, output)
    assert count == 1
    assert (output / "test.svg").exists()
