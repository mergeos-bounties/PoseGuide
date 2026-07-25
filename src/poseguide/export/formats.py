"""Pose format conversion utilities for COCO and MediaPipe."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import json

from poseguide.data.loader import load_pose


@dataclass
class Keypoint:
    """A single keypoint with x, y coordinates and visibility."""
    x: float
    y: float
    visibility: int  # 0: not labeled, 1: labeled but not visible, 2: labeled and visible


@dataclass
class PoseKeypoints:
    """Collection of keypoints for a pose."""
    keypoints: List[Keypoint]
    name: str


# COCO keypoint indices (17 keypoints)
COCO_KEYPOINT_NAMES = [
    "nose",
    "left_eye",
    "right_eye",
    "left_ear",
    "right_ear",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
    "left_hip",
    "right_hip",
    "left_knee",
    "right_knee",
    "left_ankle",
    "right_ankle",
]

# MediaPipe pose landmark indices (33 landmarks)
# We'll use the pose landmarks subset that corresponds to body joints
MEDIAPIPE_POSE_LANDMARK_NAMES = [
    "nose",
    "left_eye_inner",
    "left_eye",
    "left_eye_outer",
    "right_eye_inner",
    "right_eye",
    "right_eye_outer",
    "left_ear",
    "right_ear",
    "mouth_left",
    "mouth_right",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
    "left_pinky",
    "right_pinky",
    "left_index",
    "right_index",
    "left_thumb",
    "right_thumb",
    "left_hip",
    "right_hip",
    "left_knee",
    "right_knee",
    "left_ankle",
    "right_ankle",
    "left_heel",
    "right_heel",
    "left_foot_index",
    "right_foot_index",
]

# PoseGuide joint names (from JSON files)
POSEGUIDE_JOINT_NAMES = [
    "nose",
    "l_eye",  # left eye
    "r_eye",  # right eye
    "l_ear",  # left ear
    "r_ear",  # right ear
    "l_shoulder",
    "r_shoulder",
    "l_elbow",
    "r_elbow",
    "l_wrist",
    "r_wrist",
    "l_hip",
    "r_hip",
    "l_knee",
    "r_knee",
    "l_ankle",
    "r_ankle",
    # Additional PoseGuide joints if present
    "l_heel",
    "r_heel",
    "l_foot_index",
    "r_foot_index",
]


def pose_to_coco(pose_data: dict) -> dict:
    """
    Convert PoseGuide pose format to COCO keypoint format.
    
    Args:
        pose_data: PoseGuide pose dictionary with 'joints' key
        
    Returns:
        COCO format dictionary with 'keypoints' list and 'bbox'
    """
    # Initialize all COCO keypoints as not labeled (visibility=0)
    coco_keypoints = [0.0, 0.0, 0] * len(COCO_KEYPOINT_NAMES)
    
    # Map PoseGuide joints to COCO indices
    joint_mapping = {
        "nose": 0,
        "l_eye": 1,      # left_eye
        "r_eye": 2,      # right_eye
        "l_ear": 3,      # left_ear
        "r_ear": 4,      # right_ear
        "l_shoulder": 5,
        "r_shoulder": 6,
        "l_elbow": 7,
        "r_elbow": 8,
        "l_wrist": 9,
        "r_wrist": 10,
        "l_hip": 11,
        "r_hip": 12,
        "l_knee": 13,
        "r_knee": 14,
        "l_ankle": 15,
        "r_ankle": 16,
    }
    
    joints = pose_data.get("joints", {})
    
    for pg_joint, coco_idx in joint_mapping.items():
        if pg_joint in joints:
            x, y, z = joints[pg_joint]  # z is depth/confidence, we'll ignore for 2D
            # Convert normalized coordinates [0,1] to pixel coordinates (assuming 640x480)
            # For now, keep normalized as COCO expects normalized or we can scale later
            coco_keypoints[coco_idx * 3] = x
            coco_keypoints[coco_idx * 3 + 1] = y
            coco_keypoints[coco_idx * 3 + 2] = 2  # visible and labeled
    
    # Calculate bounding box from visible keypoints
    visible_points = [
        (coco_keypoints[i], coco_keypoints[i+1])
        for i in range(0, len(coco_keypoints), 3)
        if coco_keypoints[i+2] > 0
    ]
    
    if visible_points:
        xs, ys = zip(*visible_points)
        bbox = [
            min(xs), min(ys),  # top-left
            max(xs) - min(xs), max(ys) - min(ys)  # width, height
        ]
    else:
        bbox = [0, 0, 0, 0]
    
    return {
        "keypoints": coco_keypoints,
        "bbox": bbox,
        "category_id": 1,  # person
    }


def coco_to_poseguide(coco_data: dict) -> dict:
    """
    Convert COCO keypoint format to PoseGuide pose format.
    
    Args:
        coco_data: COCO format dictionary with 'keypoints' list
        
    Returns:
        PoseGuide pose dictionary with 'joints' key
    """
    keypoints = coco_data.get("keypoints", [])
    if len(keypoints) != 51:  # 17 keypoints * 3 (x, y, visibility)
        raise ValueError(f"Expected 51 COCO keypoint values, got {len(keypoints)}")
    
    joints = {}
    joint_mapping = {
        0: "nose",
        1: "l_eye",
        2: "r_eye",
        3: "l_ear",
        4: "r_ear",
        5: "l_shoulder",
        6: "r_shoulder",
        7: "l_elbow",
        8: "r_elbow",
        9: "l_wrist",
        10: "r_wrist",
        11: "l_hip",
        12: "r_hip",
        13: "l_knee",
        14: "r_knee",
        15: "l_ankle",
        16: "r_ankle",
    }
    
    for coco_idx, pg_joint in joint_mapping.items():
        x = keypoints[coco_idx * 3]
        y = keypoints[coco_idx * 3 + 1]
        visibility = keypoints[coco_idx * 3 + 2]
        
        if visibility > 0:  # labeled and visible
            joints[pg_joint] = [x, y, 0.0]  # z=0 for depth
    
    # Build minimal pose data
    pose_data = {
        "id": coco_data.get("id", "converted"),
        "name": coco_data.get("name", "Converted Pose"),
        "standing": True,
        "tags": ["converted"],
        "tips": [],
        "camera_cues": [],
        "joints": joints,
    }
    
    return pose_data


def pose_to_mediapipe(pose_data: dict) -> dict:
    """
    Convert PoseGuide pose format to MediaPipe pose landmark format.
    
    Args:
        pose_data: PoseGuide pose dictionary with 'joints' key
        
    Returns:
        MediaPipe format dictionary with 'landmarks' list
    """
    # Initialize all MediaPipe landmarks as not present (visibility=0)
    mediapipe_landmarks = [0.0, 0.0, 0.0, 0.0] * len(MEDIAPIPE_POSE_LANDMARK_NAMES)
    
    # Map PoseGuide joints to MediaPipe landmark indices
    joint_mapping = {
        "nose": 0,
        "l_eye": 2,      # left_eye (skip inner/outer for simplicity)
        "r_eye": 5,      # right_eye
        "l_ear": 7,
        "r_ear": 8,
        "l_shoulder": 11,
        "r_shoulder": 12,
        "l_elbow": 13,
        "r_elbow": 14,
        "l_wrist": 15,
        "r_wrist": 16,
        "l_hip": 23,
        "r_hip": 24,
        "l_knee": 25,
        "r_knee": 26,
        "l_ankle": 27,
        "r_ankle": 28,
        "l_heel": 29,
        "r_heel": 30,
        "l_foot_index": 31,
        "r_foot_index": 32,
    }
    
    joints = pose_data.get("joints", {})
    
    for pg_joint, mp_idx in joint_mapping.items():
        if pg_joint in joints:
            x, y, z = joints[pg_joint]
            # MediaPipe uses normalized coordinates [0,1] with visibility
            mediapipe_landmarks[mp_idx * 4] = x
            mediapipe_landmarks[mp_idx * 4 + 1] = y
            mediapipe_landmarks[mp_idx * 4 + 2] = z  # depth
            mediapipe_landmarks[mp_idx * 4 + 3] = 2.0  # visibility (present)
    
    return {
        "landmarks": mediapipe_landmarks,
    }


def mediapipe_to_poseguide(mp_data: dict) -> dict:
    """
    Convert MediaPipe pose landmark format to PoseGuide pose format.
    
    Args:
        mp_data: MediaPipe format dictionary with 'landmarks' list
        
    Returns:
        PoseGuide pose dictionary with 'joints' key
    """
    landmarks = mp_data.get("landmarks", [])
    if len(landmarks) != 132:  # 33 landmarks * 4 (x, y, z, visibility)
        raise ValueError(f"Expected 132 MediaPipe landmark values, got {len(landmarks)}")
    
    joints = {}
    joint_mapping = {
        0: "nose",
        2: "l_eye",
        5: "r_eye",
        7: "l_ear",
        8: "r_ear",
        11: "l_shoulder",
        12: "r_shoulder",
        13: "l_elbow",
        14: "r_elbow",
        15: "l_wrist",
        16: "r_wrist",
        23: "l_hip",
        24: "r_hip",
        25: "l_knee",
        26: "r_knee",
        27: "l_ankle",
        28: "r_ankle",
        29: "l_heel",
        30: "r_heel",
        31: "l_foot_index",
        32: "r_foot_index",
    }
    
    for mp_idx, pg_joint in joint_mapping.items():
        x = landmarks[mp_idx * 4]
        y = landmarks[mp_idx * 4 + 1]
        z = landmarks[mp_idx * 4 + 2]
        visibility = landmarks[mp_idx * 4 + 3]
        
        if visibility > 0:  # present and visible
            joints[pg_joint] = [x, y, z]
    
    # Build minimal pose data
    pose_data = {
        "id": mp_data.get("id", "converted"),
        "name": mp_data.get("name", "Converted Pose"),
        "standing": True,
        "tags": ["converted"],
        "tips": [],
        "camera_cues": [],
        "joints": joints,
    }
    
    return pose_data


def round_trip_test(pose_id: str) -> tuple[bool, bool]:
    """
    Test round-trip conversion: PoseGuide -> COCO -> PoseGuide and PoseGuide -> MediaPipe -> PoseGuide.
    
    Args:
        pose_id: ID of pose to test
        
    Returns:
        Tuple of (coco_success, mediapipe_success)
    """
    try:
        # Load original pose
        original_pose = load_pose(Path(f"data/poses/{pose_id}.json"))
        
        # Test COCO round-trip
        coco_data = pose_to_coco(original_pose)
        restored_pose = coco_to_poseguide(coco_data)
        coco_success = _poses_equivalent(original_pose, restored_pose)
        
        # Test MediaPipe round-trip
        mp_data = pose_to_mediapipe(original_pose)
        restored_pose2 = mediapipe_to_poseguide(mp_data)
        mediapipe_success = _poses_equivalent(original_pose, restored_pose2)
        
        return coco_success, mediapipe_success
    except Exception as e:
        print(f"Round-trip test failed for {pose_id}: {e}")
        return False, False


def _poses_equivalent(pose1: dict, pose2: dict, tolerance: float = 0.01) -> bool:
    """
    Check if two poses are equivalent within tolerance.
    
    Args:
        pose1: First pose dictionary
        pose2: Second pose dictionary
        tolerance: Tolerance for coordinate comparison
        
    Returns:
        True if poses are equivalent
    """
    joints1 = pose1.get("joints", {})
    joints2 = pose2.get("joints", {})
    
    # Check same joint keys
    if set(joints1.keys()) != set(joints2.keys()):
        return False
    
    # Check coordinates within tolerance
    for joint_name in joints1:
        coord1 = joints1[joint_name]
        coord2 = joints2[joint_name]
        if len(coord1) != len(coord2):
            return False
        for c1, c2 in zip(coord1, coord2):
            if abs(c1 - c2) > tolerance:
                return False
    
    return True


def export_pose_to_file(pose_id: str, format_type: str, output_path: Path) -> bool:
    """
    Export a pose to a file in the specified format.
    
    Args:
        pose_id: ID of pose to export
        format_type: Either 'coco' or 'mediapipe'
        output_path: Path to write the output file
        
    Returns:
        True if successful
    """
    try:
        pose_data = load_pose(Path(f"data/poses/{pose_id}.json"))
        
        if format_type.lower() == 'coco':
            export_data = pose_to_coco(pose_data)
        elif format_type.lower() == 'mediapipe':
            export_data = pose_to_mediapipe(pose_data)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Export failed: {e}")
        return False