"""Export pose joints to COCO keypoint format."""
from __future__ import annotations

COCO_KEYPOINT_NAMES = [
    "nose", "l_eye", "r_eye", "l_ear", "r_ear",
    "l_shoulder", "r_shoulder", "l_elbow", "r_elbow",
    "l_wrist", "r_wrist", "l_hip", "r_hip",
    "l_knee", "r_knee", "l_ankle", "r_ankle",
]

POSE_KEYPOINT_MAP = {
    "nose": "nose",
    "left_eye": "l_eye", "right_eye": "r_eye",
    "left_ear": "l_ear", "right_ear": "r_ear",
    "left_shoulder": "l_shoulder", "right_shoulder": "r_shoulder",
    "left_elbow": "l_elbow", "right_elbow": "r_elbow",
    "left_wrist": "l_wrist", "right_wrist": "r_wrist",
    "left_hip": "l_hip", "right_hip": "r_hip",
    "left_knee": "l_knee", "right_knee": "r_knee",
    "left_ankle": "l_ankle", "right_ankle": "r_ankle",
    "nose": "nose",
}


def pose_to_coco(pose: dict) -> dict:
    """Convert a PoseGuide pose dict to COCO keypoint format.

    Returns a dict with ``{"keypoints": [...], "bbox": [...], "num_keypoints": 17}``
    or empty arrays if no joints are present.
    """
    joints = pose.get("joints") or {}
    keypoints = []
    for name in COCO_KEYPOINT_NAMES:
        joint_val = joints.get(name) or joints.get(
            next((k for k in POSE_KEYPOINT_MAP if POSE_KEYPOINT_MAP[k] == name), None)
        )
        if joint_val and len(joint_val) >= 2:
            x, y = float(joint_val[0]), float(joint_val[1])
            visibility = 2 if len(joint_val) >= 3 and joint_val[2] != 0.0 else 2
            keypoints.extend([x, y, visibility])
        else:
            keypoints.extend([0.0, 0.0, 0])

    xs = [keypoints[i] for i in range(0, len(keypoints), 3) if keypoints[i + 2] > 0]
    ys = [keypoints[i + 1] for i in range(0, len(keypoints), 3) if keypoints[i + 2] > 0]
    bbox = [min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)] if xs else []

    return {
        "keypoints": keypoints,
        "bbox": bbox,
        "num_keypoints": len(xs),
    }