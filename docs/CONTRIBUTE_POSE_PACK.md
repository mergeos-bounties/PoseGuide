# How to Contribute a Pose Pack

## Overview

PoseGuide accepts community-contributed pose packs for camera positioning guidance.

## Pose JSON Schema

```json
{
  "id": "unique_pose_id",
  "name": "Human Readable Name",
  "difficulty": "easy|medium|hard",
  "category": "standing|sitting|action|portrait",
  "joints": {
    "head": [x, y, z],
    "shoulders": [x, y, z],
    "hips": [x, y, z],
    "knees": [x, y, z],
    "feet": [x, y, z]
  },
  "tips": ["Tip 1", "Tip 2"],
  "camera_cues": ["Front view", "Eye level"]
}
```

## Steps to Contribute

1. **Fork** the PoseGuide repository
2. **Create** your pose JSON in `data/poses/`
3. **Follow** the schema above
4. **Add** at least 3 helpful tips
5. **Include** camera angle suggestions
6. **Test** with `pytest tests/`
7. **Submit** PR with description

## Quality Guidelines

- Coordinates should be realistic (meters from origin)
- Tips should be actionable and specific
- Camera cues should include angle and framing
- Use descriptive IDs (e.g., `sitting_cross_legged`)

## Example

See `data/poses/standing_neutral.json` for a complete example.
