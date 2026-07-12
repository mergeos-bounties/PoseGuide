from __future__ import annotations

from pathlib import Path

from poseguide.data.loader import load_scene, load_subject
from poseguide.models.toy import ToyPoseRanker, tags_from_text


def recommend_for_scene_path(
    scene_path: Path,
    top_k: int = 3,
    subject_path: Path | None = None,
) -> dict:
    scene = load_scene(scene_path)
    subject_vec = None
    if subject_path is not None:
        subject_vec = load_subject(subject_path)["joint_vector"]
    ranker = ToyPoseRanker()
    recs = ranker.recommend(scene, top_k=top_k, subject_vector=subject_vec)
    return {
        "scene_id": scene.get("id"),
        "scene_tags": sorted(set(str(t).lower() for t in (scene.get("tags") or []))),
        "recommendations": recs,
    }


def recommend_for_tags(tags: str | list[str], top_k: int = 3) -> dict:
    if isinstance(tags, str):
        tag_list = tags_from_text(tags)
    else:
        tag_list = [str(t).strip().lower() for t in tags if str(t).strip()]
    scene = {"id": "adhoc", "tags": tag_list, "mood": []}
    recs = ToyPoseRanker().recommend(scene, top_k=top_k)
    return {"scene_id": "adhoc", "scene_tags": tag_list, "recommendations": recs}
