from __future__ import annotations

from pathlib import Path

from poseguide.data.loader import list_sample_files, list_scene_files
from poseguide.guide.recommend import recommend_for_scene_path, recommend_for_tags
from poseguide.guide.score import score_subject_against_pose
from poseguide.render.overlay import write_guidance_overlay


def test_recommend_for_tags() -> None:
    result = recommend_for_tags("urban,wall,daylight", top_k=3)
    assert result["scene_tags"]
    assert len(result["recommendations"]) == 3
    assert result["recommendations"][0]["score"] >= 0


def test_recommend_for_scene_files() -> None:
    path = list_scene_files()[0]
    result = recommend_for_scene_path(path, top_k=3)
    assert result["recommendations"]
    assert "pose_id" in result["recommendations"][0]


def test_score_subject_high_match() -> None:
    samples = list_sample_files()
    assert samples
    # subject_contrapposto.json -> target contrapposto
    path = next(p for p in samples if "contrapposto" in p.name)
    result = score_subject_against_pose("contrapposto", path)
    assert result["confidence"] >= 0.75
    assert result["cues"]


def test_overlay_write(tmp_path: Path) -> None:
    result = recommend_for_tags("beach,portrait", top_k=2)
    out = tmp_path / "overlay.json"
    path = write_guidance_overlay(result, out)
    assert path.exists()
    assert "poseguide.overlay" in path.read_text(encoding="utf-8")
