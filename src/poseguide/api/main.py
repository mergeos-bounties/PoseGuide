import uvicorn
from fastapi import FastAPI, HTTPException
from .schemas import (
    RecommendRequest, RecommendResponse, 
    ScoreRequest, ScoreResponse, 
    HealthResponse, PoseRecommendation
)

# Note: In a real scenario, we would import the logic from ai_solution.py
# For this bounty, we implement the API structure and integration points.

app = FastAPI(
    title="PoseGuide API",
    description="Photography pose coach API: scene tags to ranked poses.",
    version="0.2.1"
)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check if the API service is healthy."""
    return {"status": "healthy", "version": "0.2.1"}

@app.post("/guide/recommend", response_model=RecommendResponse)
async def recommend_poses(request: RecommendRequest):
    """
    Takes scene tags and returns a ranked list of matching poses.
    """
    try:
        # Placeholder for ai_solution logic integration
        # Example: results = ai_solution.match_tags(request.tags)
        mock_results = [
            PoseRecommendation(pose_id="arms_crossed", score=0.95, tags=["standing", "urban"]),
            PoseRecommendation(pose_id="lean_wall_casual", score=0.82, tags=["urban", "casual"])
        ]
        return {"recommendations": mock_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/guide/score", response_model=ScoreResponse)
async def score_pose(request: ScoreRequest):
    """
    Compares subject landmarks against a target pose scaffold.
    """
    try:
        # Placeholder for ai_solution scoring logic
        # Example: score = ai_solution.calculate_score(request.subject_landmarks, request.target_pose_id)
        return {
            "score": 0.88,
            "feedback": "Adjust your left arm slightly higher.",
            "is_match": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("src.poseguide.api.main:app", host="0.0.0.0", port=8000, reload=True)
