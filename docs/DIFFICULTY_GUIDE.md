# Difficulty Levels Guide for Pose Packs

This document defines the meaning of difficulty levels used in PoseGuide pose packs,
to help contributors choose the right level for their poses.

## Overview

Difficulty indicates how complex a pose is to execute and photograph well. It helps
photographers and models select appropriate challenges.

## Levels

### Easy

- **Description**: Simple, natural standing or seated poses that require no special training
- **Characteristics**:
  - Minimal joint deviation from neutral stance
  - One or two subtle changes (e.g., arm position, head tilt)
  - No balance challenges or contortions
  - Suitable for beginners and casual photography
- **Examples**: Arms crossed, hands in pockets, leaning against wall, looking away
- **Joint complexity**: Standard skeleton, mostly planar (z ≈ 0)

### Medium

- **Description**: Poses requiring some body awareness, slight asymmetry, or balance
- **Characteristics**:
  - Noticeable weight shift or hip rotation
  - Multiple limb positions with clear intent
  - May require brief practice to look natural
  - Good for intermediate photographers/models
- **Examples**: Contrapposto stance, one-knee down, side profile with hand on hip
- **Joint complexity**: Some z-axis variation, asymmetric limb placement

### Hard

- **Description**: Dynamic, athletic, or highly stylized poses requiring flexibility or strength
- **Characteristics**:
  - Significant joint angles or extended ranges of motion
  - Balance challenges (single-leg, deep squat, etc.)
  - Requires physical fitness or dance/martial arts background
  - Best for professional shoots with experienced models
- **Examples**: Jump mid-air, yoga poses, deep lunges, acrobatic positions
- **Joint complexity**: Full 3D skeleton, significant depth variation, non-standard angles

## Adding Difficulty to Your Pose Pack

When creating a new pose JSON file, include the `difficulty` field:

```json
{
  "id": "beach_sunset_stretch",
  "name": "Beach Sunset Stretch",
  "difficulty": "easy",
  "standing": true,
  "tags": ["outdoor", "beach", "sunset", "relaxed"],
  "tips": [
    "Stand sideways to the sunset for rim lighting",
    "Reach one arm up, other on hip for S-curve silhouette"
  ],
  "camera_cues": ["full body", "golden hour", "slight low angle"],
  "joints": { ... }
}
```

## Quality Checklist

Before submitting, verify:

- [ ] Difficulty matches the pose complexity (see definitions above)
- [ ] Tips are actionable and specific to this pose
- [ ] Camera cues include angle and framing notes
- [ ] Joints are realistic (coordinates within normalized image space)
- [ ] Tags cover at least 3 relevant scene categories
- [ ] Pose passes `pytest tests/` locally

---

*Last updated: 2026-07-16*
*Author: lushan888*
*Closes mergeos-bounties/PoseGuide#55*
