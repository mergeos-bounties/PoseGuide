"""Tests for pose export functions."""
from poseguide.data.export import pose_to_coco


def test_pose_to_coco_known_pose():
    pose = {
        "id": "test_pose",
        "joints": {
            "nose": [0.5, 0.1, 0.0],
            "l_shoulder": [0.4, 0.25, 0.0],
            "r_shoulder": [0.6, 0.25, 0.0],
            "l_hip": [0.4, 0.5, 0.0],
            "r_hip": [0.6, 0.5, 0.0],
            "l_knee": [0.4, 0.7, 0.0],
            "r_knee": [0.6, 0.7, 0.0],
        },
    }
    coco = pose_to_coco(pose)
    assert coco["num_keypoints"] == 7
    assert len(coco["keypoints"]) == 17 * 3
    assert len(coco["bbox"]) == 4
    assert coco["bbox"][0] == 0.4


def test_pose_to_coco_empty_joints():
    coco = pose_to_coco({"joints": {}})
    assert coco["num_keypoints"] == 0
    assert len(coco["keypoints"]) == 17 * 3
    assert all(v == 0.0 for v in coco["keypoints"])
    assert coco["bbox"] == []


def test_pose_to_coco_missing_pose():
    coco = pose_to_coco({"id": "missing"})
    assert coco["num_keypoints"] == 0