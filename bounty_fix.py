import os
import json

def create_yoga_warrior_ii_side_pose():
    """
    Implements the Yoga Warrior II (Virabhadrasana II) side-view pose 
    definition for the PoseGuide catalog.
    """
    pose_id = "yoga_warrior_ii_side"
    
    # Pose definition: Joint angles and balance parameters for a side view
    # Coordinates are normalized relative to the center of gravity
    pose_data = {
        "id": pose_id,
        "name": "Yoga Warrior II (Side View)",
        "category": "fitness",
        "description": "Warrior II side-view focusing on hip alignment and stability.",
        "joints": {
            "right_hip": {"angle": 90, "position": [0, 0, 0]},
            "right_knee": {"angle": 90, "position": [0.5, 0, 0]},
            "right_ankle": {"angle": 0, "position": [0.5, -0.5, 0]},
            "left_hip": {"angle": 180, "position": [0, 0, 0]},
            "left_knee": {"angle": 180, "position": [-0.8, 0, 0