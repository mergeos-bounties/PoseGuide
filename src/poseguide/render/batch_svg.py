"""Batch SVG rendering for pose packs."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from poseguide.models.catalog import get_all_poses
from poseguide.render.svg import render_pose_svg


def batch_render_svg(
    out_dir: Path,
    *,
    width: int = 360,
    height: int = 480,
    pose_ids: Optional[list[str]] = None,
) -> list[Path]:
    """Render all poses (or specific ones) to SVG files."""
    out_dir.mkdir(parents=True, exist_ok=True)
    
    if pose_ids:
        poses = []
        for pid in pose_ids:
            pose = get_pose_by_id(pid)
            if pose:
                poses.append((pid, pose))
    else:
        all_poses = get_all_poses()
        poses = [(p.get("id"), p) for p in all_poses if p.get("id")]
    
    rendered_paths: list[Path] = []
    
    for pose_id, _ in poses:
        out_path = out_dir / f"{pose_id}.svg"
        try:
            render_pose_svg(pose_id, out_path, width=width, height=height)
            rendered_paths.append(out_path)
        except Exception as e:
            print(f"Warning: Failed to render {pose_id}: {e}")
    
    return rendered_paths


def batch_render_svg_with_manifest(
    out_dir: Path,
    *,
    width: int = 360,
    height: int = 480,
    pose_ids: Optional[list[str]] = None,
) -> tuple[list[Path], Path]:
    """Render poses and create a manifest file."""
    rendered_paths = batch_render_svg(out_dir, width=width, height=height, pose_ids=pose_ids)
    
    manifest = {
        "rendered_at": str(Path.cwd()),
        "width": width,
        "height": height,
        "total_poses": len(rendered_paths),
        "poses": [str(p.name) for p in rendered_paths],
    }
    
    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    
    return rendered_paths, manifest_path


def render_pose_pack_svg(
    pack_dir: Path,
    out_dir: Path,
    *,
    width: int = 360,
    height: int = 480,
) -> list[Path]:
    """Render all poses from a pose pack directory."""
    pose_files = list(pack_dir.glob("*.json"))
    
    pose_ids = []
    for pf in pose_files:
        try:
            data = json.loads(pf.read_text(encoding="utf-8"))
            if isinstance(data, dict) and "id" in data:
                pose_ids.append(data["id"])
        except Exception:
            continue
    
    return batch_render_svg(out_dir, width=width, height=height, pose_ids=pose_ids)
