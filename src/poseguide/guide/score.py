from __future__ import annotations

from pathlib import Path
from typing import Optional

from poseguide.data.loader import load_subject
from poseguide.models.catalog import get_pose_by_id
from poseguide.models.toy import ToyPoseRanker


def score_subject_against_pose(pose_id: str, subject_path: Path, use_mediapipe: bool = False) -> dict:
    """
    Score a subject photo against a reference pose.

    Args:
        pose_id: The pose ID to score against.
        subject_path: Path to the subject (JSON file or image).
        use_mediapipe: If True, use MediaPipe to extract pose from image (requires vision extra).
                       If False, load subject from JSON file (default).

    Returns:
        A dictionary with the score and metadata.
    """
    pose = get_pose_by_id(pose_id)
    if pose is None:
        raise KeyError(f"unknown pose {pose_id!r}")

    if use_mediapipe:
        try:
            from poseguide.data.extract import extract_pose
        except ImportError as e:
            raise RuntimeError(
                "MediaPipe is not installed. Install the 'vision' extra to use this feature."
            ) from e
        subject = extract_pose(subject_path)
    else:
        subject = load_subject(subject_path)

    result = ToyPoseRanker().score_match(pose, subject["joint_vector"])
    result["subject_id"] = subject.get("id")
    result["source"] = str(subject_path)
    return result