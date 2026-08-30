from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, Field, field_validator, model_validator

REQUIRED_JOINTS = [
    "nose", "l_shoulder", "r_shoulder", "l_elbow", "r_elbow",
    "l_wrist", "r_wrist", "l_hip", "r_hip", "l_knee", "r_knee",
    "l_ankle", "r_ankle"
]

class Joint(BaseModel):
    x: float = Field(..., ge=0, le=1)
    y: float = Field(..., ge=0, le=1)
    visibility: Optional[float] = Field(default=1.0, ge=0, le=1)

class Pose(BaseModel):
    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    tags: List[str] = Field(..., min_length=1)
    standing: bool = Field(...)
    difficulty: Literal["easy", "medium", "hard"] = "easy"
    joints: Dict[str, Joint]

    @field_validator("tags")
    @classmethod
    def tags_not_empty(cls, v):
        if not v or any(not t.strip() for t in v):
            raise ValueError("tags must be non-empty strings")
        return [t.strip().lower() for t in v]

    @model_validator(mode="after")
    def check_required_joints(self):
        missing = [j for j in REQUIRED_JOINTS if j not in self.joints]
        if missing:
            raise ValueError(f"Missing required joints: {missing}")
        if not self.standing:
            raise ValueError("Pose must be standing pose (standing=True)")
        return self

class Scene(BaseModel):
    id: str
    tags: List[str] = Field(..., min_length=1)
    preset: Optional[str] = None
    standing_required: bool = True

class PoseCatalog(BaseModel):
    poses: List[Pose]
