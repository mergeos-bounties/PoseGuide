from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from poseguide import __version__
from poseguide.data.loader import list_pose_files, list_scene_files, load_pose, load_scene


def build_web_catalog() -> dict[str, Any]:
    """Build the JSON payload consumed by the static web demo."""
    poses = [_public_pose(load_pose(path)) for path in list_pose_files()]
    scenes = [_public_scene(load_scene(path)) for path in list_scene_files()]
    tags = sorted(
        {
            tag
            for item in [*poses, *scenes]
            for tag in [*item.get("tags", []), *item.get("mood", [])]
        }
    )
    return {
        "schema": "poseguide.web.catalog.v1",
        "poseguide_version": __version__,
        "poses": sorted(poses, key=lambda pose: str(pose["id"])),
        "scenes": sorted(scenes, key=lambda scene: str(scene["id"])),
        "tags": tags,
    }


def write_web_catalog(out_path: Path | None = None) -> Path:
    root = Path(__file__).resolve().parents[3]
    path = out_path or root / "web" / "data" / "catalog.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_web_catalog()
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _public_pose(pose: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(pose.get("id", "")),
        "name": str(pose.get("name", "")),
        "standing": bool(pose.get("standing", True)),
        "tags": _strings(pose.get("tags")),
        "tips": _strings(pose.get("tips")),
        "camera_cues": _strings(pose.get("camera_cues")),
        "joints": pose.get("joints") or {},
    }


def _public_scene(scene: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(scene.get("id", "")),
        "name": str(scene.get("name", "")),
        "tags": _strings(scene.get("tags")),
        "mood": _strings(scene.get("mood")),
        "expected_poses": _strings(scene.get("expected_poses")),
        "composition": scene.get("composition") or {},
    }


def _strings(values: Any) -> list[str]:
    if values is None:
        return []
    return [str(value).strip().lower() for value in values if str(value).strip()]
