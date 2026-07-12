from __future__ import annotations

from poseguide.data.loader import list_scene_files, load_scene
from poseguide.models.toy import ToyPoseRanker


def evaluate_scenes(top_k: int = 3) -> dict:
    ranker = ToyPoseRanker()
    scenes = [load_scene(p) for p in list_scene_files()]
    hits = 0
    labeled = 0
    precision_sum = 0.0
    recall_sum = 0.0
    rows = []
    for scene in scenes:
        expected = {str(x).lower() for x in (scene.get("expected_poses") or [])}
        recs = ranker.recommend(scene, top_k=top_k)
        top_ids = {str(r["pose_id"]).lower() for r in recs}
        inter = top_ids & expected
        hit = bool(expected and inter)
        if expected:
            labeled += 1
            if hit:
                hits += 1
            precision_sum += len(inter) / max(1, len(top_ids))
            recall_sum += len(inter) / max(1, len(expected))
        rows.append(
            {
                "scene": scene.get("id"),
                "expected": sorted(expected),
                "top": [r["pose_id"] for r in recs],
                "hit": hit,
                "overlap": sorted(inter),
            }
        )
    return {
        "top_k": top_k,
        "n_scenes": len(scenes),
        "n_labeled": labeled,
        "hit_at_k": round(hits / labeled, 4) if labeled else None,
        "precision_at_k": round(precision_sum / labeled, 4) if labeled else None,
        "recall_at_k": round(recall_sum / labeled, 4) if labeled else None,
        "rows": rows,
    }
