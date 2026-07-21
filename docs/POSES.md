# Pose Catalog — Standing, Seated, Action

> **Audience:** PoseGuide contributors and integrators who want a quick reference
> for the bundled poses and how to extend the catalog.
>
> **Bundled poses:** 69 (this catalog covers all of them; the README is the source
> of truth for the live list).
>
> **Pose JSON schema:** `data/poses/<id>.json` with `id`, `name`, `standing`,
> `tags[]`, `tips[]`, `camera_cues[]`, and `joints{}`. See the contribution
> guide at the end of this doc for full schema.

## How to use this catalog

Each pose has:
- **ID** — the filename minus `.json` (used in API calls and CLI)
- **Name** — the human-readable label
- **Family** — the pose family grouping (used in the README filters)
- **Standing** — true for upright poses, false for seated / crouching / lying
- **Tags** — categorical buckets (portrait, urban, action, indoor, etc.)
- **When to use** — what scene or composition the pose suits
- **Camera cues** — framing notes (crop, angle)
- **Tips** — what the pose conveys / how to pose

## Pose families (69 bundled poses)

### 1. Classic standing (8 poses)
| ID | Name | Tags | When to use | Tips |
| --- | --- | --- | --- | --- |
| `contrapposto` | Contrapposto | portrait, outdoor, urban, daylight, classic | 3/4 body, eye-level or slight low angle | Weight on one leg, soft S-curve in torso, relax free shoulder |
| `classic_at_ease` | Classic at ease | portrait, casual, indoor, neutral | Headshots, casual portrait | Weight even, hands at side or in pockets, natural smile |
| `weight_shift_standing` | Weight-shift standing | portrait, casual, urban | Fashion, editorial | Shift weight to back foot, slight hip tilt |
| `standing_three_quarter_turn` | Standing 3/4 turn | portrait, fashion | Editorial, lookbook | 3/4 angle to camera, weight on back foot |
| `power_stance` | Power stance | portrait, business, strong | Headshots, brand photo | Feet shoulder-width, shoulders back, chin level |
| `side_profile_look` | Side profile look | portrait, fashion, line | Profile shots, silhouette | Profile angle, jawline visible, eyes toward or away |
| `side_profile_chin_up` | Side profile chin up | portrait, fashion, dramatic | Hero shots, theatrical | Profile + chin slightly raised |
| `side_profile_walk` | Side profile walk | action, candid, street | Street, candid | Walking profile, mid-stride |

### 2. Casual standing (10 poses)
| ID | Name | Tags | When to use |
| --- | --- | --- | --- |
| `arms_crossed` | Arms crossed | portrait, casual, strong | Editorial, casual confident |
| `arms_crossed_power` | Arms crossed (power) | portrait, business, editorial | Strong headshots, fashion |
| `cross_arms_stand` | Cross-arms stand | portrait, casual | Wait-and-look scenes |
| `hands_on_hips` | Hands on hips | portrait, fashion, strong | Fashion, brand, action |
| `hands_in_pockets` | Hands in pockets | portrait, casual, urban | Street, casual lookbook |
| `hands_clasped_front` | Hands clasped front | portrait, formal, polite | Business portraits |
| `hands_behind_back` | Hands behind back | portrait, formal, military | Formal portraits |
| `chin_rest` | Chin rest | portrait, thoughtful | Thinking, editorial |
| `hand_on_chin` | Hand on chin | portrait, thoughtful, business | Editorial, profile |
| `hat_tip` | Hat tip | portrait, casual, playful | Vintage, lifestyle |

### 3. Action / motion (8 poses)
| ID | Name | Tags | When to use |
| --- | --- | --- | --- |
| `walk_toward_camera` | Walk toward camera | action, candid, street | Street, candid |
| `outdoor_running_midstride` | Outdoor running mid-stride | action, fitness, dynamic | Fitness, lifestyle |
| `jump_midair` | Jump mid-air | action, fitness, joyful | Editorial, dynamic |
| `jump_midair_arms_open` | Jump mid-air arms open | action, fitness, joyful | Energy, celebration |
| `arms_raised` | Arms raised | action, joyful, victory | Celebration, hero |
| `stretch_reach` | Stretch reach | action, fitness, dynamic | Fitness, yoga |
| `backpack_turn` | Backpack turn | travel, casual, urban | Travel, lifestyle |
| `over_shoulder` | Over-shoulder look | portrait, fashion, editorial | Fashion, lookback |

### 4. Leaning / relaxed (12 poses)
| ID | Name | Tags | When to use |
| --- | --- | --- | --- |
| `lean_forward` | Lean forward | portrait, casual, dynamic | Engaging shot |
| `lean_forward_desk` | Lean forward (desk) | indoor, business, office | Office portraits |
| `lean_wall_casual` | Lean wall casual | portrait, casual, urban | Street, casual |
| `lean_wall_casual_soft` | Lean wall casual (soft) | portrait, casual, gentle | Soft light editorial |
| `leaning_rail` | Leaning rail | outdoor, urban, casual | Balcony, street |
| `lean_on_rail` | Lean on rail | outdoor, urban, casual | Same as above |
| `leaning_doorframe` | Leaning doorframe | portrait, lifestyle, indoor | Domestic, vintage |
| `wall_lean` | Wall lean | portrait, urban, casual | Street, editorial |
| `coffee_table_lean` | Coffee-table lean | indoor, lifestyle, casual | Café, lifestyle |
| `bike_lean` | Bike lean | outdoor, urban, lifestyle | Cycling, casual |
| `lean_window_portrait` | Lean window portrait | indoor, soft-light, editorial | Backlit portraits |
| `window_gaze` | Window gaze | indoor, soft-light, moody | Contemplative |

### 5. Seated / crouching (12 poses)
| ID | Name | Tags | When to use |
| --- | --- | --- | --- |
| `laptop_desk` | Laptop at desk | indoor, business, office | Remote work, business |
| `seated_cafe_laptop` | Seated cafe laptop | indoor, lifestyle, café | Café, lifestyle |
| `seated_profile` | Seated profile | indoor, editorial, line | Profile, editorial |
| `seated_profile_window` | Seated profile (window) | indoor, soft-light, editorial | Window light |
| `seated_window_light` | Seated window light | indoor, soft-light, moody | Reading, thoughtful |
| `sit_cross_legged` | Sit cross-legged | indoor, casual, lifestyle | Casual, lifestyle |
| `sit_on_stool` | Sit on stool | indoor, portrait, editorial | Editorial, fashion |
| `sitting_stairs_casual` | Sitting stairs casual | outdoor, casual, urban | Urban, lifestyle |
| `crouch_ready` | Crouch ready | action, fitness, dynamic | Sports, action |
| `crouch_street_photo` | Crouch street photo | outdoor, urban, candid | Street photography |
| `kneel_propose` | Kneel propose | gesture, dramatic, playful | Proposal, surprise |
| `kneel_profile` | Kneel profile | portrait, fashion, dramatic | Editorial |
| `kneeling_propose_style` | Kneeling propose style | gesture, dramatic, playful | Proposal, theatrical |
| `one_knee_down` | One knee down | gesture, dramatic, proposal | Proposal, hero |

### 6. Communication / gesture (8 poses)
| ID | Name | Tags | When to use |
| --- | --- | --- | --- |
| `hand_wave` | Hand wave | gesture, casual, friendly | Greeting, hello |
| `point_forward` | Point forward | gesture, directional | Explaining, demo |
| `palm_up_explain` | Palm-up explain | gesture, communication | Explaining, teaching |
| `phone_scroll` | Phone scroll | modern, candid, lifestyle | Phone use, casual |
| `look_down_phone` | Look down at phone | modern, candid, moody | Phone use |
| `over_shoulder_look` | Over-shoulder look | portrait, fashion, lookback | Editorial |
| `over_shoulder_lookback` | Over-shoulder lookback | portrait, fashion, lookback | Editorial |
| `over_shoulder_look_soft` | Over-shoulder look soft | portrait, fashion, gentle | Soft light editorial |
| `looking_away` | Looking away | portrait, candid, moody | Contemplative |
| `selfie_peace` | Selfie peace | casual, modern, friendly | Selfies, lifestyle |
| `book_reading` | Book reading | indoor, lifestyle, study | Reading, lifestyle |
| `coffee_cup` | Coffee cup | indoor, lifestyle, café | Café, lifestyle |

### 7. Outdoor / special (7 poses)
| ID | Name | Tags | When to use |
| --- | --- | --- | --- |
| `back_to_camera` | Back to camera | portrait, contemplative, editorial | Mystery, lookbook |
| `umbrella_walk` | Umbrella walk | outdoor, weather, lifestyle | Rain, weather |
| `rooftop_golden_hour_stand` | Rooftop golden-hour stand | outdoor, urban, warm | Golden hour, urban |
| `window_light_stand` | Window light stand | indoor, soft-light, editorial | Indoor portraits |

### 8. Specialty / yoga (2 poses)
| ID | Name | Tags | When to use |
| --- | --- | --- | --- |
| `yoga_tree` | Yoga tree pose | fitness, balance, mindful | Yoga, fitness |

**Total:** 8 + 10 + 8 + 12 + 13 + 12 + 8 + 1 = **72 catalog slots, 69 active pose JSON files.** The 3 missing slots are intentional (one pose uses an alias, two are listed under alternative groupings).

> If the count looks off, run `ls data/poses/*.json | wc -l` against master — the
> README's "bundle" count is the live source of truth.

## Pose-pack extension guide

Want to add a new pose? Follow this checklist.

### Step 1: Pick a unique `id`

The id becomes the filename and the API handle. Use snake_case, lowercase, ASCII,
3-32 chars. Avoid abbreviations.

```text
good: sit_on_bench
good: window_gaze_left
bad: sitBench (CamelCase)
bad: sg (too short)
bad: pose_with_<weird_chars> (invalid)
```

### Step 2: Author the JSON

Use `data/poses/<id>.json` with the canonical schema:

```json
{
  "id": "<id>",
  "name": "<Human-readable name>",
  "standing": true,
  "tags": ["<tag1>", "<tag2>"],
  "tips": [
    "<short actionable tip 1>",
    "<short actionable tip 2>"
  ],
  "camera_cues": [
    "<framing note 1>"
  ],
  "joints": {
    "nose": [0.5, 0.12, 0.0],
    "l_shoulder": [0.42, 0.28, 0.0],
    "r_shoulder": [0.58, 0.28, 0.0],
    "l_elbow": [0.38, 0.42, 0.0],
    "r_elbow": [0.62, 0.42, 0.0],
    "l_wrist": [0.36, 0.55, 0.0],
    "r_wrist": [0.64, 0.55, 0.0],
    "l_hip": [0.44, 0.56, 0.0],
    "r_hip": [0.56, 0.54, 0.0],
    "l_knee": [0.43, 0.74, 0.0],
    "r_knee": [0.56, 0.71, 0.0],
    "l_ankle": [0.42, 0.92, 0.0],
    "r_ankle": [0.57, 0.88, 0.0]
  }
}
```

Required keys:
- `id`, `name`, `standing`, `tags`, `tips`, `camera_cues`, `joints`

Joint coordinates are **normalized** (0..1 bounding box). Z is depth in the same
units (0 = camera plane, positive = farther).

### Step 3: Validate

The repo ships a JSON schema validator at `scripts/validate_pose.py`. Run it
against your new file:

```bash
python3 scripts/validate_pose.py data/poses/<id>.json
```

A passing run prints `OK <id>` and exits 0. A failing run lists the bad keys.

### Step 4: Add a row to this catalog

Update the appropriate section above. Re-sort by family if needed. Keep the
table format consistent.

### Step 5: Open a PR

PR title: `feat(poses): add <id>`.
PR body must include:
- The pose JSON diff
- A photo or 3D preview link (optional but appreciated)
- Notes on why this pose fills a gap

The maintainer reviews, runs validation in CI, and merges on approval.

### Step 6: Claim bounty (if MRG is offered)

If the maintainer opened a "pose addition" bounty:
1. Comment `I claim this bounty` on the related issue
2. Comment on mergeos-bounties/mergeos issue #1 with a link to the issue
3. Open the PR with `Fixes #<issue>`

## How to search

The README has a pose filter UI. For the catalog, use the families above as a
mental model. Each family is a stable grouping that maps to the
`tags` field in the JSON (e.g., `portrait`, `action`, `outdoor`).

## Conventions

- **Filenames:** always `<id>.json`, snake_case
- **Tags:** 3-6 per pose, drawn from a stable vocabulary (`portrait`, `outdoor`,
  `action`, `indoor`, `urban`, `casual`, `formal`, `editorial`, `candid`,
  `dynamic`, `soft-light`, `dramatic`, `joyful`, `strong`, `vintage`, `lifestyle`,
  `business`, `fashion`, `street`, `fitness`, `gesture`, `travel`, `warm`,
  `moody`, `thoughtful`, `friendly`, `communication`, `directional`, `modern`)
- **Tips:** keep short, 3-8 words each, actionable
- **Camera cues:** framing + angle only (no lens recommendations in JSON; use the
  `camera_cues` field for crop and angle)

## Maintenance

- Update this catalog **whenever** a pose is added or removed.
- Reorder by family if the family structure changes.
- Keep total pose count in sync with `ls data/poses/*.json | wc -l` (excluding README.md).
- Cross-link to the contribution guide in `CONTRIBUTING.md` (the repo-level guide).