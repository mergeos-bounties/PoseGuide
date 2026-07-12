from __future__ import annotations

from poseguide.data.loader import list_pose_files, load_pose


def load_pose_catalog() -> list[dict]:
    return [load_pose(path) for path in list_pose_files()]


def get_pose_by_id(pose_id: str) -> dict | None:
    key = pose_id.strip().lower()
    for pose in load_pose_catalog():
        if str(pose.get("id", "")).lower() == key:
            return pose
        if str(pose.get("name", "")).lower().replace(" ", "_") == key:
            return pose
    return None
