# PoseGuide Pose Catalog

This document catalogs all standing pose families available in PoseGuide, with when-to-use notes for different backgrounds and scenes.

## Pose Categories

### Classic Standing Poses

| Pose | Best For | Key Tips |
|------|----------|----------|
| `contrapposto` | Portrait, Urban, Daylight | Weight on one leg, soft S-curve, relax shoulders |
| `power_stance` | Studio, Fashion, Empowerment | Wide stance, hands on hips, confident posture |
| `hands_on_hips` | Portrait, Business, Confidence | Elbows out, chest open, assertive stance |
| `arms_crossed` | Portrait, Professional, Casual | Relaxed crossed arms, slight lean |
| `hands_in_pockets` | Casual, Street, Lifestyle | Relaxed shoulders, natural weight shift |
| `classic_at_ease` | Military, Formal, Ceremonial | Heels together, hands at sides, upright posture |

### Leaning Poses

| Pose | Best For | Key Tips |
|------|----------|----------|
| `lean_wall_casual` | Urban, Street, Lifestyle | One shoulder against wall, relaxed |
| `leaning_rail` | Outdoor, Rooftop, waterfront | Elbow on rail, body angled |
| `lean_forward_desk` | Office, Work, Indoor | Forward lean, hands on surface |
| `coffee_table_lean` | Cafe, Indoor, Casual | Side lean, one arm on table |
| `leaning_doorframe` | Indoor, Portrait, Casual | One shoulder in frame, relaxed |

### Walking & Movement

| Pose | Best For | Key Tips |
|------|----------|----------|
| `walk_toward_camera` | Street, Urban, Fashion | Mid-stride, natural arm swing |
| `side_profile_walk` | Profile, Movement, Street | Side view, walking motion |
| `umbrella_walk` | Rain, Urban, Moody | Walking with umbrella, atmospheric |
| `couple_walk_holding_hands` | Romantic, Outdoor, Duo | Two subjects, connected movement |

### Seated Poses

| Pose | Best For | Key Tips |
|------|----------|----------|
| `seated_profile` | Portrait, Indoor, Pensive | Side profile, thoughtful expression |
| `seated_crossed_legs` | Casual, Indoor, Relaxed | Cross-legged, comfortable posture |
| `seated_window_light` | Indoor, Natural Light, Moody | Window light, contemplative |
| `sitting_stairs_casual` | Urban, Outdoor, Relaxed | Stairs, casual seated position |

### Dynamic & Action

| Pose | Best For | Key Tips |
|------|----------|----------|
| `jump_midair` | Energy, Fun, Action | Mid-jump, dynamic energy |
| `stretch_reach` | Fitness, Yoga, Movement | Arms extended, stretching |
| `yoga_tree` | Yoga, Balance, Nature | Balance pose, one leg raised |
| `outdoor_running_midstride` | Sports, Fitness, Action | Running motion, mid-stride |

### Profile & Over Shoulder

| Pose | Best For | Key Tips |
|------|----------|----------|
| `over_shoulder_look` | Portrait, Mystery, Flirty | Look back over shoulder |
| `side_profile_standing` | Profile, Fashion, Minimalist | Clean side profile |
| `back_to_camera` | Mystery, Landscape, Silhouette | Back turned, facing away |
| `looking_away` | Pensive, Dreamy, Candid | Gaze directed away from camera |

### Prop & Object Poses

| Pose | Best For | Key Tips |
|------|----------|----------|
| `coffee_cup` | Cafe, Lifestyle, Casual | Holding coffee cup, relaxed |
| `phone_scroll` | Modern, Urban, Candid | Looking at phone, natural |
| `book_reading` | Indoor, Intellectual, Quiet | Reading a book, contemplative |
| `hat_tip` | Formal, Classic,绅士 | Adjusting hat, stylish |
| `umbrella_walk` | Rain, Urban, Moody | Walking with umbrella |

### Specialty Poses

| Pose | Best For | Key Tips |
|------|----------|----------|
| `kneel_propose` | Romantic, Proposal, Special | One knee down, romantic |
| `crouch_ready` | Sporty, Action, Ready | Crouched position, ready to move |
| `point_forward` | Directing, Leading, Action | Pointing gesture, directional |
| `selfie_peace` | Fun, Casual, Social | Peace sign, selfie pose |

## Background Matching Guide

### Urban & City
- **Best**: `contrapposto`, `lean_wall_casual`, `walking_toward_camera`, `phone_scroll`
- **Avoid**: `yoga_tree`, `kneel_propose`

### Nature & Outdoor
- **Best**: `contrapposto`, `hands_on_hips`, `umbrella_walk`, `stretch_reach`
- **Avoid**: `laptop_desk`, `seated_cafe_laptop`

### Studio & Portrait
- **Best**: `power_stance`, `hands_on_hips_hero`, `over_shoulder_look`, `side_profile_standing`
- **Avoid**: `coffee_cup`, `phone_scroll`

### Indoor & Lifestyle
- **Best**: `seated_profile`, `lean_forward_desk`, `book_reading`, `coffee_cup`
- **Avoid**: `jump_midair`, `outdoor_running_midstride`

### Romantic & Duo
- **Best**: `couple_walk_holding_hands`, `kneel_propose`, `over_shoulder_look`
- **Avoid**: `power_stance`, `arms_crossed`

## Creating Custom Poses

To add a new pose:

1. Create a JSON file in `data/poses/`
2. Include required fields: `id`, `name`, `tags`, `tips`, `camera_cues`, `joints`
3. Ensure `standing: true` for standing poses
4. Use normalized coordinates (0-1) for joints
5. Add appropriate tags for scene matching

### JSON Structure

```json
{
  "id": "pose_name",
  "name": "Display Name",
  "standing": true,
  "tags": ["tag1", "tag2"],
  "tips": ["Tip 1", "Tip 2"],
  "camera_cues": ["Cue 1", "Cue 2"],
  "joints": {
    "nose": [0.5, 0.12, 0.0],
    "l_shoulder": [0.42, 0.28, 0.0],
    ...
  }
}
```

## Usage Examples

### CLI Usage
```bash
# List all poses
poseguide poses list

# Get pose recommendations for a scene
poseguide guide --scene beach

# Get recommendations with custom presets
poseguide guide --preset urban
```

### API Usage
```python
from poseguide import PoseGuide

guide = PoseGuide()
recommendations = guide.recommend(scene_tags=["outdoor", "beach"])
```

## Contributing

See [BOUNTY.md](../BOUNTY.md) for information on contributing poses via bounties.

All poses must be:
- Synthetic scaffold data (no real person data without consent)
- Properly tagged and documented
- Include camera cues and tips
- Use normalized joint coordinates
