import json
from typing import Dict, List, Union

def coco_format(pose_joints: List[Dict[str, Union[float, int]]]) -> Dict:
    """Convert pose joints to COCO keypoints format."""
    coco_keypoints = []
    for joint in pose_joints:
        coco_keypoints.extend([
            joint['x'], joint['y'], joint.get('score', 1.0)
        ])
    return {
        'keypoints': coco_keypoints,
        'num_keypoints': len(pose_joints)
    }

def mediapipe_format(pose_joints: List[Dict[str, Union[float, int]]]) -> Dict:
    """Convert pose joints to MediaPipe keypoints format."""
    mediapipe_keypoints = []
    for joint in pose_joints:
        mediapipe_keypoints.append({
            'x': joint['x'],
            'y': joint['y'],
            'score': joint.get('score', 1.0)
        })
    return {
        'keypoints': mediapipe_keypoints
    }

def export_pose(pose_joints: List[Dict[str, Union[float, int]]], format: str) -> Dict:
    """Export pose joints to specified format."""
    if format.lower() == 'coco':
        return coco_format(pose_joints)
    elif format.lower() == 'mediapipe':
        return mediapipe_format(pose_joints)
    else:
        raise ValueError(f"Unsupported export format: {format}")