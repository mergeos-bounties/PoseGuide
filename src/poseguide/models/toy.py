from __future__ import annotations

import numpy as np

from poseguide.data.loader import scene_tag_set
from poseguide.models.catalog import load_pose_catalog


class ToyPoseRanker:
    """
    Offline demo ranker:
    - score = tag Jaccard * 0.65 + joint cosine prior * 0.35
    - joint prior uses mean joint vector similarity when subject available
    """

    def __init__(self, poses: list[dict] | None = None):
        self.poses = poses if poses is not None else load_pose_catalog()

    def recommend(
        self,
        scene: dict,
        top_k: int = 3,
        subject_vector: np.ndarray | None = None,
    ) -> list[dict]:
        scene_tags = scene_tag_set(scene)
        ranked: list[dict] = []
        for pose in self.poses:
            pose_tags = {str(t).strip().lower() for t in (pose.get("tags") or []) if t}
            inter = len(scene_tags & pose_tags)
            union = len(scene_tags | pose_tags) or 1
            tag_score = inter / union
            joint_score = 0.5
            if subject_vector is not None and pose.get("joint_vector") is not None:
                joint_score = _cosine(subject_vector, np.asarray(pose["joint_vector"]))
                joint_score = max(0.0, min(1.0, (joint_score + 1.0) / 2.0))
            score = 0.65 * tag_score + 0.35 * joint_score
            # slight boost for standing poses in outdoor wide scenes
            if pose.get("standing", True) and "outdoor" in scene_tags:
                score = min(1.0, score + 0.05)
            ranked.append(
                {
                    "pose_id": pose.get("id"),
                    "name": pose.get("name"),
                    "score": round(float(score), 4),
                    "tag_overlap": sorted(scene_tags & pose_tags),
                    "tips": pose.get("tips") or [],
                    "camera_cues": pose.get("camera_cues") or [],
                }
            )
        ranked.sort(key=lambda r: r["score"], reverse=True)
        return ranked[: max(1, top_k)]

    def score_match(self, pose: dict, subject_vector: np.ndarray) -> dict:
        target = np.asarray(pose.get("joint_vector"), dtype=np.float64)
        cos = _cosine(subject_vector, target)
        confidence = max(0.0, min(1.0, (cos + 1.0) / 2.0))
        # Per-region crude deltas for coaching cues
        cues = _coaching_cues(target, subject_vector)
        return {
            "pose_id": pose.get("id"),
            "name": pose.get("name"),
            "similarity": round(float(cos), 4),
            "confidence": round(float(confidence), 4),
            "cues": cues,
            "pass": confidence >= 0.75,
        }


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=np.float64).ravel()
    b = np.asarray(b, dtype=np.float64).ravel()
    n = min(a.size, b.size)
    if n == 0:
        return 0.0
    a = a[:n]
    b = b[:n]
    denom = (np.linalg.norm(a) * np.linalg.norm(b)) + 1e-9
    return float(np.dot(a, b) / denom)


def _coaching_cues(target: np.ndarray, subject: np.ndarray) -> list[str]:
    """Generate short human-readable adjustments from joint deltas."""
    labels = [
        "nose",
        "left shoulder",
        "right shoulder",
        "left elbow",
        "right elbow",
        "left wrist",
        "right wrist",
        "left hip",
        "right hip",
        "left knee",
        "right knee",
        "left ankle",
        "right ankle",
    ]
    t = np.asarray(target, dtype=np.float64).ravel()
    s = np.asarray(subject, dtype=np.float64).ravel()
    cues: list[str] = []
    for i, name in enumerate(labels):
        base = i * 3
        if base + 1 >= t.size or base + 1 >= s.size:
            break
        dy = float(s[base + 1] - t[base + 1])
        dx = float(s[base] - t[base])
        if abs(dy) < 0.04 and abs(dx) < 0.04:
            continue
        if abs(dy) >= abs(dx):
            direction = "lower" if dy > 0 else "raise"
            cues.append(f"{direction} your {name} slightly")
        else:
            direction = "shift right" if dx > 0 else "shift left"
            cues.append(f"{direction} with your {name}")
        if len(cues) >= 4:
            break
    if not cues:
        cues.append("Hold the pose — alignment looks close")
    return cues


def tags_from_text(text: str) -> list[str]:
    parts = [p.strip().lower() for p in text.replace(";", ",").split(",")]
    return [p for p in parts if p]
