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

### Required Joints Keys

Every pose JSON must include these joint keys (coordinates in meters from origin):

| Joint | Description |
|-------|-------------|
| `nose` | Face center |
| `l_shoulder`, `r_shoulder` | Shoulder points |
| `l_elbow`, `r_elbow` | Elbow bends |
| `l_wrist`, `r_wrist` | Hand positions |
| `l_hip`, `r_hip` | Hip reference |
| `l_knee`, `r_knee` | Knee bends |
| `l_ankle`, `r_ankle` | Foot placement |

Additional joints are encouraged for complex poses (e.g., `neck`, `spine`, `l_ear`, `r_ear`).

### Difficulty Field

The `difficulty` field classifies pose complexity:

- **easy**: Standing, neutral pose, minimal limb articulation (e.g., standing_neutral, hand_wave)
- **medium**: Seated or dynamic pose, moderate joint variation (e.g., sitting_cross_legged, crouch_ready)
- **hard**: Complex action, unusual angles, or multiple interacting joints (e.g., jump_midair, yoga_tree)

### Catalog Rebuild

After adding or modifying pose packs, rebuild the web catalog:

```bash
python scripts/build-web-catalog.py
```

This regenerates `web/catalog.json` and updates the pose index.

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
- Include `difficulty` and `category` fields
- Run `python scripts/build-web-catalog.py` before submitting

## Evidence Requirements

When submitting a pose pack PR, include:

1. **Screenshot** — rendered pose visualization (see `docs/screenshots/` for examples)
2. **JSON validation** — output of `python -m json.tool data/poses/<your_pose>.json`
3. **Catalog rebuild** — confirm `web/catalog.json` includes your pose
4. **Test pass** — `pytest tests/ -v` output

## Example

See `data/poses/standing_neutral.json` for a complete example.

## Pose Pack Bounty Workflow

For pose pack bounties specifically:

1. Claim the bounty issue (comment `I claim this bounty`)
2. Fork + create branch: `pose-pack/<pose-id>`
3. Add pose JSON + screenshot + tips
4. Run catalog rebuild + tests
5. Open PR with evidence (screenshots, test output)
6. Maintainer reviews → merge → MRG credit issued
