from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, field_validator

# Canonical standing-skeleton joints understood by the pose engine.
JOINT_KEYS = (
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
)

# Joints that must be present for a pose to be scoreable.
REQUIRED_JOINTS = ("l_shoulder", "r_shoulder", "l_hip", "r_hip")


class Pose(BaseModel):
    """Validated schema for a shipped pose template (``data/poses/*.json``)."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    standing: bool = True
    tags: list[str] = Field(default_factory=list)
    tips: list[str] = Field(default_factory=list)
    camera_cues: list[str] = Field(default_factory=list)
    joints: dict[str, list[float]] = Field(default_factory=dict)

    @field_validator("joints")
    @classmethod
    def _check_joints(cls, value: dict[str, list[float]]) -> dict[str, list[float]]:
        missing = [key for key in REQUIRED_JOINTS if key not in value]
        if missing:
            raise ValueError(f"missing required joints: {', '.join(missing)}")
        for key, coords in value.items():
            if key not in JOINT_KEYS:
                raise ValueError(f"unknown joint key: {key!r}")
            if len(coords) < 2:
                raise ValueError(f"joint {key!r} needs at least [x, y] coordinates")
        return value


class Scene(BaseModel):
    """Validated schema for a shipped scene template (``data/scenes/*.json``)."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    tags: list[str] = Field(default_factory=list)
    mood: list[str] = Field(default_factory=list)
    expected_poses: list[str] = Field(default_factory=list)
    composition: dict[str, str] = Field(default_factory=dict)
    notes: str | None = None


def validate_pose(payload: dict) -> Pose:
    """Validate a single pose payload, raising ``ValidationError`` on bad data."""
    return Pose.model_validate(payload)


def validate_scene(payload: dict) -> Scene:
    """Validate a single scene payload, raising ``ValidationError`` on bad data."""
    return Scene.model_validate(payload)


def validate_pose_file(path: Path) -> Pose:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return validate_pose(payload)


def validate_scene_file(path: Path) -> Scene:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return validate_scene(payload)


def load_poses(paths: list[Path] | None = None) -> list[Pose]:
    """Validate and return every shipped pose (or the given ``paths``)."""
    from poseguide.data.loader import list_pose_files

    files = paths if paths is not None else list_pose_files()
    return [validate_pose_file(path) for path in files]


def load_scenes(paths: list[Path] | None = None) -> list[Scene]:
    """Validate and return every shipped scene (or the given ``paths``)."""
    from poseguide.data.loader import list_scene_files

    files = paths if paths is not None else list_scene_files()
    return [validate_scene_file(path) for path in files]
