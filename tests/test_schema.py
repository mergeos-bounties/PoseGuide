from __future__ import annotations

import pytest
from pydantic import ValidationError

from poseguide.data.loader import list_pose_files, list_scene_files
from poseguide.data.schema import (
    load_poses,
    load_scenes,
    validate_pose,
    validate_scene,
)


def test_all_shipped_poses_validate() -> None:
    poses = load_poses()
    assert len(poses) == len(list_pose_files())
    assert all(pose.id for pose in poses)


def test_all_shipped_scenes_validate() -> None:
    scenes = load_scenes()
    assert len(scenes) == len(list_scene_files())
    assert all(scene.id for scene in scenes)


def test_malformed_pose_raises_validation_error() -> None:
    bad_pose = {
        "id": "broken_pose",
        "name": "Broken Pose",
        "joints": {
            "l_shoulder": [0.1, 0.2],
            "r_shoulder": [0.2, 0.2],
            "l_hip": [0.1, 0.5],
            "r_hip": [0.2, 0.5],
            "not_a_real_joint": [0.0, 0.0],
        },
    }
    with pytest.raises(ValidationError):
        validate_pose(bad_pose)


def test_pose_missing_required_field_raises() -> None:
    with pytest.raises(ValidationError):
        validate_pose({"name": "No Id Pose"})


def test_pose_missing_required_joint_raises() -> None:
    with pytest.raises(ValidationError):
        validate_pose(
            {
                "id": "incomplete_joints",
                "name": "Incomplete Joints",
                "joints": {"l_shoulder": [0.1, 0.2]},
            }
        )


def test_scene_missing_required_field_raises() -> None:
    with pytest.raises(ValidationError):
        validate_scene({"tags": ["urban"]})
