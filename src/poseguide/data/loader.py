from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from poseguide.config import POSES_DIR, SAMPLES_DIR, SCENES_DIR


def _list_json(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(directory.glob("*.json"))


def list_pose_files(directory: Path | None = None) -> list[Path]:
    return _list_json(directory or POSES_DIR)


def list_scene_files(directory: Path | None = None) -> list[Path]:
    return _list_json(directory or SCENES_DIR)


def list_sample_files(directory: Path | None = None) -> list[Path]:
    return _list_json(directory or SAMPLES_DIR)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_pose(path: Path) -> dict:
    payload = load_json(path)
    payload.setdefault("id", path.stem)
    payload.setdefault("name", path.stem.replace("_", " ").title())
    payload.setdefault("tags", [])
    payload.setdefault("standing", True)
    joints = payload.get("joints") or {}
    payload["joint_vector"] = joints_to_vector(joints)
    return payload


def load_scene(path: Path) -> dict:
    payload = load_json(path)
    payload.setdefault("id", path.stem)
    payload.setdefault("tags", [])
    payload.setdefault("mood", [])
    return payload


def load_subject(path: Path) -> dict:
    payload = load_json(path)
    joints = payload.get("joints") or {}
    payload["joint_vector"] = joints_to_vector(joints)
    payload.setdefault("id", path.stem)
    return payload


def joints_to_vector(joints: dict) -> np.ndarray:
    """
    Flatten a small standing skeleton into a fixed feature vector.
    Expected keys (optional): nose, l_shoulder, r_shoulder, l_hip, r_hip,
    l_elbow, r_elbow, l_wrist, r_wrist, l_knee, r_knee, l_ankle, r_ankle.
    """
    order = [
        "nose",
        "l_shoulder",
        "r_shoulder",
        "l_elbow",
        "r_elbow",
        "l_wrist",
        "r_wrist",
        "l_hip",
        "r_hip",
        "l_knee",
        "r_knee",
        "l_ankle",
        "r_ankle",
    ]
    vec: list[float] = []
    for key in order:
        xyz = joints.get(key) or [0.0, 0.0, 0.0]
        if not isinstance(xyz, (list, tuple)) or len(xyz) < 2:
            vec.extend([0.0, 0.0, 0.0])
        else:
            x = float(xyz[0])
            y = float(xyz[1])
            z = float(xyz[2]) if len(xyz) > 2 else 0.0
            vec.extend([x, y, z])
    return np.asarray(vec, dtype=np.float64)


def scene_tag_set(scene: dict) -> set[str]:
    tags = [str(t).strip().lower() for t in (scene.get("tags") or [])]
    mood = [str(m).strip().lower() for m in (scene.get("mood") or [])]
    return {t for t in tags + mood if t}
