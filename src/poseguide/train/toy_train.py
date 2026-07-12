from __future__ import annotations

import json

from poseguide.config import RUNS_DIR
from poseguide.data.loader import list_scene_files, load_scene
from poseguide.models.toy import ToyPoseRanker


def train_toy(epochs: int = 3) -> dict:
    """
    'Training' for the toy ranker: evaluate top-1 tag retrieval on scenes.
    Real training bounties replace this with embedding/ranking models.
    """
    scenes = [load_scene(p) for p in list_scene_files()]
    if not scenes:
        raise FileNotFoundError("no scenes under data/scenes")

    history = []
    ranker = ToyPoseRanker()
    for epoch in range(1, max(1, epochs) + 1):
        hits = 0
        for scene in scenes:
            expected = set(str(x).lower() for x in (scene.get("expected_poses") or []))
            recs = ranker.recommend(scene, top_k=3)
            top_ids = {str(r["pose_id"]).lower() for r in recs}
            if expected and (top_ids & expected):
                hits += 1
            elif not expected and recs and recs[0]["score"] > 0:
                hits += 1
        acc = hits / len(scenes)
        history.append({"epoch": epoch, "hit_rate_at_3": round(acc, 4), "n": len(scenes)})

    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = RUNS_DIR / "toy_train_report.json"
    report = {
        "model": "ToyPoseRanker",
        "epochs": epochs,
        "history": history,
        "n_poses": len(ranker.poses),
        "n_scenes": len(scenes),
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return {"report_path": str(report_path), **report}
