"""Scene difficulty tagging for PoseGuide."""

from enum import Enum

class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

def tag_difficulty(scene):
    """Tag scene difficulty based on complexity."""
    joints = len(scene.get('joints', {}))
    tips = len(scene.get('tips', []))
    camera_cues = len(scene.get('camera_cues', []))
    
    score = joints + tips + camera_cues
    
    if score <= 8:
        return Difficulty.EASY
    elif score <= 15:
        return Difficulty.MEDIUM
    else:
        return Difficulty.HARD

def filter_by_difficulty(scenes, difficulty):
    """Filter scenes by difficulty level."""
    return [s for s in scenes if tag_difficulty(s) == difficulty]
