from __future__ import annotations

from poseguide.data.loader import (
    joints_to_vector,
    list_pose_files,
    list_scene_files,
    load_pose,
    load_scene,
)


def test_catalogs_exist() -> None:
    assert len(list_pose_files()) >= 8
    assert len(list_scene_files()) >= 6


def test_load_pose_has_joints() -> None:
    pose = load_pose(list_pose_files()[0])
    assert pose["id"]
    assert pose["joint_vector"].size == 13 * 3
    assert pose.get("standing") is True


def test_load_scene_tags() -> None:
    scene = load_scene(list_scene_files()[0])
    assert scene.get("tags")
    assert isinstance(scene["tags"], list)


def test_joints_to_vector_missing_keys() -> None:
    vec = joints_to_vector({"nose": [0.5, 0.1]})
    assert vec.shape == (39,)
