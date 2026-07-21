"""Tests for scene difficulty tagging."""

from poseguide.scenes import tag_difficulty, Difficulty, filter_by_difficulty

def test_easy_scene():
    scene = {"joints": {"head": [0,1,0]}, "tips": ["Tip 1"]}
    assert tag_difficulty(scene) == Difficulty.EASY

def test_medium_scene():
    scene = {"joints": {"head": [0,1,0], "hips": [0,0.5,0]}, "tips": ["T1", "T2", "T3"], "camera_cues": ["Front"]}
    assert tag_difficulty(scene) == Difficulty.MEDIUM

def test_filter_by_difficulty():
    scenes = [
        {"joints": {"head": [0,1,0]}, "tips": ["T1"]},
        {"joints": {"head": [0,1,0], "hips": [0,0.5,0]}, "tips": ["T1", "T2", "T3"], "camera_cues": ["Front"]}
    ]
    easy = filter_by_difficulty(scenes, Difficulty.EASY)
    assert len(easy) == 1
