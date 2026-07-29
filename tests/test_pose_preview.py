import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.poseguide.preview import calculate_pose_placement

def test_pose_placement_valid():
    """Test pose placement box respects horizon and safe margins."""
    bg_w, bg_h = 1920, 1080
    horizon = 540
    joints = {"head": [0.5, 0.2], "ankle": [0.5, 0.8]}
    
    result = calculate_pose_placement(bg_w, bg_h, horizon, joints, margin=20)
    assert result["fits_safe_margin"] is True
    assert result["placement_box"]["y_min"] >= horizon
    assert result["placement_box"]["x_min"] >= 20

def test_pose_placement_invalid_dimensions():
    """Test pose placement raises ValueError on invalid background bounds."""
    with pytest.raises(ValueError, match="Invalid background dimensions"):
        calculate_pose_placement(-100, 1080, 540, {})
