from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class RecommendRequest(BaseModel):
    tags: List[str] = Field(..., example=["beach", "standing", "sunset"])

class PoseRecommendation(BaseModel):
    pose_id: str
    score: float
    tags: List[str]
    svg_overlay: Optional[str] = None

class RecommendResponse(BaseModel):
    recommendations: List[PoseRecommendation]

class ScoreRequest(BaseModel):
    subject_landmarks: Dict[str, Any] = Field(..., description="Subject joint coordinates")
    target_pose_id: str = Field(..., description="ID of the pose to compare against")

class ScoreResponse(BaseModel):
    score: float
    feedback: Optional[str] = None
    is_match: bool

class HealthResponse(BaseModel):
    status: str
    version: str
