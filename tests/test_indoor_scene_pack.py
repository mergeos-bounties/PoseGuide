from __future__ import annotations

from pathlib import Path

import pytest

from poseguide.data.loader import load_scene
from poseguide.guide.recommend import recommend_for_scene_path


SCENES_DIR = Path(__file__).resolve().parents[1] / "data" / "scenes"
SCENE_CASES = (
    ("indoor_loft.json", "indoor_loft"),
    ("cafe_window_counter.json", "cafe_window_counter"),
)


@pytest.mark.parametrize(("filename", "scene_id"), SCENE_CASES)
def test_indoor_scene_loads(filename: str, scene_id: str) -> None:
    scene = load_scene(SCENES_DIR / filename)

    assert scene["id"] == scene_id
    assert "indoor" in scene["tags"]
    assert scene["expected_poses"]


@pytest.mark.parametrize(("filename", "scene_id"), SCENE_CASES)
def test_indoor_scene_recommendations_include_expected_pose(
    filename: str,
    scene_id: str,
) -> None:
    path = SCENES_DIR / filename
    scene = load_scene(path)
    result = recommend_for_scene_path(path, top_k=5)
    recommended = {item["pose_id"] for item in result["recommendations"]}

    assert result["scene_id"] == scene_id
    assert len(result["recommendations"]) == 5
    assert recommended.intersection(scene["expected_poses"])
