from __future__ import annotations

from poseguide.guide.recommend import recommend_for_tags
from poseguide.render.overlay import write_guidance_overlay
from poseguide.render.svg import render_pose_svg
from poseguide.config import OUT_DIR

PRESETS = {
    "beach": "beach,outdoor,golden_hour,portrait,daylight",
    "urban": "urban,wall,street,daylight,casual",
    "studio": "studio,indoor,portrait,business,confident",
    "forest": "forest,outdoor,golden_hour,romantic,portrait",
    "office": "indoor,business,urban,confident,studio",
}


def run_demo(preset: str = "beach", *, top_k: int = 3) -> dict:
    key = preset.strip().lower()
    tags = PRESETS.get(key)
    if not tags:
        raise KeyError(f"unknown preset {preset!r}; known={sorted(PRESETS)}")
    result = recommend_for_tags(tags, top_k=top_k)
    result["preset"] = key
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    overlay = write_guidance_overlay(result, OUT_DIR / f"demo_{key}_overlay.json")
    result["overlay_path"] = str(overlay)
    if result.get("recommendations"):
        pose_id = str(result["recommendations"][0]["pose_id"])
        svg_path = render_pose_svg(pose_id, OUT_DIR / f"demo_{key}_{pose_id}.svg")
        result["svg_path"] = str(svg_path)
        result["top_pose_id"] = pose_id
    return result
