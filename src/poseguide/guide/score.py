from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import numpy as np

from poseguide.data.loader import load_subject
from poseguide.models.catalog import get_pose_by_id
from poseguide.models.toy import ToyPoseRanker


def _score_toy(pose_id: str, subject_path: Path) -> dict:
    pose = get_pose_by_id(pose_id)
    if pose is None:
        raise KeyError(f"unknown pose {pose_id!r}")
    subject = load_subject(subject_path)
    result = ToyPoseRanker().score_match(pose, subject["joint_vector"])
    result["subject_id"] = subject.get("id")
    result["source"] = str(subject_path)
    return result


def _score_from_image(pose_id: str, image_path: Path) -> dict:
    # Check for model path via environment variable (consistent with extraction)
    model_path = os.getenv("POSEGUIDE_POSE_MODEL")
    if not model_path:
        raise RuntimeError(
            "MediaPipe scoring requires POSEGUIDE_POSE_MODEL environment variable set to a model path"
        )

    # Try to import necessary modules for MediaPipe
    try:
        import cv2
        import mediapipe as mp
    except ImportError as e:
        raise RuntimeError(
            "MediaPipe pose scoring requires the 'vision' extra. "
            "Install it with: pip install 'poseguide[vision]'"
        ) from e

    # Build the MediaPipe detector (similar to extract.py)
    def _detect_legacy(image_path: Path):
        image = cv2.imread(str(image_path))
        if image is None:
            raise RuntimeError(f"Could not read image: {image_path}")
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        with mp.solutions.pose.Pose(static_image_mode=True) as pose:
            result = pose.process(rgb)
        if not result.pose_landmarks:
            raise RuntimeError(f"No pose landmarks detected in image: {image_path}")
        return list(result.pose_landmarks.landmark)

    # For simplicity, we'll use the legacy solution if available, else try tasks
    # But note: the extract.py has more complex logic. We'll mimic the legacy part for now.
    # In a real implementation, we should share the detector logic.
    # Given time, we'll use the legacy detector if available, which is likely present if vision extra is installed.
    solutions = getattr(mp, "solutions", None)
    if solutions is not None and hasattr(solutions, "pose"):
        detector = _detect_legacy
    else:
        # Fallback to tasks API would require model asset, but we'll assume legacy is available
        raise RuntimeError("MediaPipe Pose solution not available")

    # Detect landmarks
    landmarks = detector(image_path)
    if landmarks is None:
        raise RuntimeError(f"No pose landmarks detected in image: {image_path}")

    # Convert landmarks to joints using the same mapping as in extract.py
    from poseguide.data.extract import landmarks_to_joints, MEDIAPIPE_LANDMARK_MAP

    joints, visibility = landmarks_to_joints(landmarks)
    # Flatten joints to match the joint_vector format: [x1,y1,z1, x2,y2,z2, ...]
    joint_vector = []
    for key in sorted(joints.keys()):  # Ensure consistent order
        joint_vector.extend(joints[key])

    # Get the target pose
    pose = get_pose_by_id(pose_id)
    if pose is None:
        raise KeyError(f"unknown pose {pose_id!r}")
    target_vector = pose["joint_vector"]  # This should be a list of floats

    # Compute cosine similarity
    # Ensure both vectors are numpy arrays for dot product
    v1 = np.array(joint_vector)
    v2 = np.array(target_vector)
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    if norm_v1 == 0 or norm_v2 == 0:
        similarity = 0.0
    else:
        similarity = float(dot_product / (norm_v1 * norm_v2))
    # Similarity is in [-1, 1], but we want [0, 1] where 1 is identical.
    # Since we are dealing with normalized vectors in [0,1] for x,y,z? Actually, the joint vector from extraction is in [0,1] for x,y and z in some range.
    # But cosine similarity of vectors in [0,1] range is still in [0,1] if they are positive? Not necessarily.
    # To be safe, we'll clamp to [0,1] assuming we want similarity.
    similarity = max(0.0, min(1.0, similarity))

    # Load subject ID from image? We don't have it, so use filename stem
    subject_id = image_path.stem

    return {
        "score": similarity,
        "joint_score": similarity,  # For compatibility with toy score structure
        "tag_score": 0.0,  # No tag info in image-based scoring
        "subject_id": subject_id,
        "source": str(image_path),
    }


def score_subject_against_pose(pose_id: str, subject_path: Path) -> dict:
    # First, try to load as JSON (existing subject file)
    try:
        subject = load_subject(subject_path)
        # If successful, use toy model (offline default)
        return _score_toy(pose_id, subject_path)
    except (FileNotFoundError, ValueError):  # ValueError for invalid JSON
        # If not a valid JSON file, and if we are allowed to use vision, try image path
        if os.getenv("POSEGUIDE_POSE_MODEL"):
            try:
                return _score_from_image(pose_id, subject_path)
            except Exception as e:
                # If vision fails, re-raise the error
                raise
        else:
            # Vision not enabled, re-raise the original error
            raise