import { execSync } from 'node:child_process';
import { mkdtempSync, writeFileSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

const REPO = 'mergeos-bounties/PoseGuide';

function sh(cmd) {
  return execSync(cmd, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
}

function ensureLabel(name, color, description) {
  try {
    sh(
      `gh label create ${JSON.stringify(name)} --repo ${REPO} --color ${color} --description ${JSON.stringify(description)}`,
    );
  } catch {
    try {
      sh(
        `gh label edit ${JSON.stringify(name)} --repo ${REPO} --color ${color} --description ${JSON.stringify(description)}`,
      );
    } catch {
      // ignore
    }
  }
}

function createIssue(title, body, labels) {
  const dir = mkdtempSync(join(tmpdir(), 'poseguide-issue-'));
  const file = join(dir, 'body.md');
  try {
    writeFileSync(file, body, 'utf8');
    const labelFlags = labels.map((l) => `--label ${JSON.stringify(l)}`).join(' ');
    const out = sh(
      `gh issue create --repo ${REPO} --title ${JSON.stringify(title)} --body-file ${JSON.stringify(file)} ${labelFlags}`,
    );
    console.log(out);
    return out;
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

const labels = [
  ['bounty', '5319E7', 'Eligible for MergeOS MRG bounty'],
  ['bounty: feature', 'A2EEEF', 'Feature bounty'],
  ['bounty: bug', 'D73A4A', 'Bug bounty'],
  ['ml', 'B60205', 'Models / ranking / evaluation'],
  ['data', 'C5DEF5', 'Pose libraries / scenes / datasets'],
  ['vision', 'D93F0B', 'MediaPipe / OpenCV / camera'],
  ['api', '1D76DB', 'HTTP / websocket API'],
  ['ux', '0E8A16', 'Photography UX / overlays'],
  ['reward:25-mrg', 'FEF2C0', 'Target 25 MRG'],
  ['reward:50-mrg', 'FEF2C0', 'Target 50 MRG'],
  ['reward:100-mrg', 'FEF2C0', 'Target 100 MRG'],
  ['reward:200-mrg', 'FEF2C0', 'Target 200 MRG'],
  ['good first issue', '7057FF', 'Good for newcomers'],
  ['documentation', '0075CA', 'Documentation improvements'],
];

for (const [name, color, description] of labels) {
  ensureLabel(name, color, description);
}

const footer = `

## Claim (MergeOS MRG)

1. Follow https://github.com/mergeos-bounties  
2. Star https://github.com/mergeos-bounties/mergeos  
3. Star https://github.com/mergeos-bounties/mergeos-contracts
4. Comment on **this issue**: \`I claim this bounty\`  
5. Comment on MergeOS [Claim Token #1](https://github.com/mergeos-bounties/mergeos/issues/1) with a link to this issue  
6. Open a PR to **PoseGuide** (public product repo) with \`Fixes #<this-issue>\`

Policy: [docs/BOUNTY.md](../blob/master/docs/BOUNTY.md)

## Important

Work lands on **https://github.com/mergeos-bounties/PoseGuide** — not on private \`mergeos-prj_*\` mirror repos.

## Payout

Maintainer reviews PR → merge on PoseGuide → **MRG credit** on MergeOS ledger to \`github:<author>\` (25/50/100/200 scale).
`;

const issues = [
  {
    title: '[25 MRG] Docs: POSES.md catalog of standing pose families + photo tips',
    labels: ['bounty', 'bounty: feature', 'documentation', 'data', 'reward:25-mrg', 'good first issue'],
    body: `## Bounty: 25 MRG

Create \`docs/POSES.md\` documenting pose families (contrapposto, power stance, walk, lean, etc.) with when-to-use notes for backgrounds.

## Acceptance

- [ ] Doc covers all bundled poses + extension guide
- [ ] Linked from README
${footer}`,
  },
  {
    title: '[25 MRG] CLI: poseguide guide demo — print top pose for fixed beach/urban presets',
    labels: ['bounty', 'bounty: feature', 'ux', 'reward:25-mrg', 'good first issue'],
    body: `## Bounty: 25 MRG

Add \`poseguide guide demo --preset beach|urban|studio\` that runs recommendations without a scene file.

## Acceptance

- [ ] Command + tests
- [ ] README examples
${footer}`,
  },
  {
    title: '[25 MRG] Pose schema validation with pydantic',
    labels: ['bounty', 'bounty: feature', 'data', 'reward:25-mrg', 'good first issue'],
    body: `## Bounty: 25 MRG

Validate pose/scene JSON with pydantic models (required joints, tags, standing flag).

## Acceptance

- [ ] Invalid payloads raise clear errors
- [ ] Existing catalog validates
- [ ] Tests for good/bad fixtures
${footer}`,
  },
  {
    title: '[25 MRG] Expand standing pose library to 25+ templates',
    labels: ['bounty', 'bounty: feature', 'data', 'reward:25-mrg', 'good first issue'],
    body: `## Bounty: 25 MRG

Add more synthetic standing poses under \`data/poses/\` with tags + tips + joints. Keep licenses clean (synthetic only unless consented).

## Acceptance

- [ ] ≥25 poses total
- [ ] Each has tags, tips, joints
- [ ] \`poseguide poses list\` still works
${footer}`,
  },
  {
    title: '[50 MRG] MediaPipe Pose extractor from still image',
    labels: ['bounty', 'bounty: feature', 'vision', 'ml', 'reward:50-mrg'],
    body: `## Bounty: 50 MRG

Optional vision extra: extract joints from a photo into PoseGuide subject JSON.

## Acceptance

- [ ] \`poseguide data extract --image <path> --out data/samples/custom.json\`
- [ ] Graceful error if mediapipe missing
- [ ] Docs for \`[vision]\` extra
- [ ] No large private images committed
${footer}`,
  },
  {
    title: '[50 MRG] Scene tagger: simple CV/heuristics or CLIP-stub for background tags',
    labels: ['bounty', 'bounty: feature', 'vision', 'ml', 'reward:50-mrg'],
    body: `## Bounty: 50 MRG

Given a background image (or description), produce scene tags used by the ranker. Stub/heuristic OK; document upgrade path to CLIP.

## Acceptance

- [ ] CLI or module API
- [ ] Tests with fixtures (no network required)
- [ ] Wired into \`guide recommend\` optionally
${footer}`,
  },
  {
    title: '[50 MRG] OpenCV skeleton overlay renderer',
    labels: ['bounty', 'bounty: feature', 'vision', 'ux', 'reward:50-mrg'],
    body: `## Bounty: 50 MRG

Draw target vs subject skeleton on an image / blank canvas. Export PNG under \`data/out/\`.

## Acceptance

- [ ] \`poseguide render overlay --pose X --subject Y --out out.png\`
- [ ] Works with headless opencv
- [ ] CI test uses synthetic joints (no camera)
${footer}`,
  },
  {
    title: '[50 MRG] Ranking model: embedding / learning-to-rank beyond tag Jaccard',
    labels: ['bounty', 'bounty: feature', 'ml', 'reward:50-mrg'],
    body: `## Bounty: 50 MRG

Replace or augment \`ToyPoseRanker\` with a trainable ranker (numpy or optional torch). Keep toy fallback.

## Acceptance

- [ ] Train + save + load path
- [ ] Metrics improve or match toy on fixtures
- [ ] Tests without GPU
${footer}`,
  },
  {
    title: '[50 MRG] Composition rules engine (rule of thirds, horizon, headroom)',
    labels: ['bounty', 'bounty: feature', 'ux', 'ml', 'reward:50-mrg'],
    body: `## Bounty: 50 MRG

Given scene composition metadata + pose, emit camera framing recommendations (subject placement, crop, horizon).

## Acceptance

- [ ] Module + CLI output fields
- [ ] Unit tests for rule table
- [ ] Docs with examples
${footer}`,
  },
  {
    title: '[50 MRG] FastAPI: POST /guide/recommend and /guide/score',
    labels: ['bounty', 'bounty: feature', 'api', 'reward:50-mrg'],
    body: `## Bounty: 50 MRG

Ship optional FastAPI under \`src/poseguide/api/\` with recommend + score + health endpoints.

## Acceptance

- [ ] Documented uvicorn entry
- [ ] TestClient tests (api extra)
${footer}`,
  },
  {
    title: '[50 MRG] Live webcam coach loop (subject vs target pose)',
    labels: ['bounty', 'bounty: feature', 'vision', 'ux', 'reward:50-mrg'],
    body: `## Bounty: 50 MRG

\`poseguide guide webcam --pose contrapposto\` prints live cues; no camera → clear skip.

## Acceptance

- [ ] Command exists
- [ ] Headless CI safe
- [ ] Optional screenshot evidence in PR
${footer}`,
  },
  {
    title: '[50 MRG] Vietnamese photography tip pack for poses',
    labels: ['bounty', 'bounty: feature', 'documentation', 'ux', 'reward:50-mrg'],
    body: `## Bounty: 50 MRG

Add VI tips/tips localization for pose catalog + guide output language flag.

## Acceptance

- [ ] \`--lang vi\` or locale file
- [ ] ≥10 poses localized
- [ ] Tests for fallback to EN
${footer}`,
  },
  {
    title: '[100 MRG] Background-aware pose placement preview',
    labels: ['bounty', 'bounty: feature', 'vision', 'ml', 'reward:100-mrg'],
    body: `## Bounty: 100 MRG

Given background + chosen pose, produce a placement preview (silhouette / stick figure) respecting horizon and safe margins.

## Acceptance

- [ ] CLI or API path
- [ ] Fixture-based tests
- [ ] Screenshot evidence
${footer}`,
  },
  {
    title: '[100 MRG] Multi-subject / couple standing pose pack',
    labels: ['bounty', 'bounty: feature', 'data', 'ml', 'reward:100-mrg'],
    body: `## Bounty: 100 MRG

Extend schema for two-person standing poses and ranking by scene (wedding garden, street, studio).

## Acceptance

- [ ] Schema + ≥8 couple poses
- [ ] Ranker supports multi-subject
- [ ] Tests + docs
${footer}`,
  },
  {
    title: '[100 MRG] Mobile-friendly web demo for scene→pose',
    labels: ['bounty', 'bounty: feature', 'api', 'ux', 'reward:100-mrg'],
    body: `## Bounty: 100 MRG

Lightweight web UI under \`web/\` to pick scene tags or upload background and show top poses.

## Acceptance

- [ ] Local dev README
- [ ] Works with local API when available
- [ ] Screenshots in PR
${footer}`,
  },
  {
    title: '[100 MRG] Training pipeline: YAML config, seeds, checkpoint resume',
    labels: ['bounty', 'bounty: feature', 'ml', 'reward:100-mrg'],
    body: `## Bounty: 100 MRG

Production-shaped train loop for the ranker/embedding model with config files and resume.

## Acceptance

- [ ] Example config
- [ ] Resume tested
- [ ] Contributor docs
${footer}`,
  },
  {
    title: '[200 MRG] End-to-end product path: photo background → pose coach → overlay export',
    labels: ['bounty', 'bounty: feature', 'vision', 'ml', 'ux', 'reward:200-mrg'],
    body: `## Bounty: 200 MRG

Polished E2E: image in → scene tags → pose list → live/offline coach → overlay image out. One command, documented quality bar.

## Acceptance

- [ ] Single CLI path
- [ ] License-safe demo assets only
- [ ] Evidence: logs + overlay images
${footer}`,
  },
  {
    title: '[25 MRG] CONTRIBUTING.md + good-first-issue path',
    labels: ['bounty', 'bounty: feature', 'documentation', 'reward:25-mrg', 'good first issue'],
    body: `## Bounty: 25 MRG

Write CONTRIBUTING with setup, tests, claim flow. Emphasize PRs target **PoseGuide** public repo only.

## Acceptance

- [ ] File + README link
${footer}`,
  },
  {
    title: '[25 MRG] CI: coverage + ruff format check',
    labels: ['bounty', 'bounty: feature', 'documentation', 'reward:25-mrg', 'good first issue'],
    body: `## Bounty: 25 MRG

Improve CI with pytest-cov threshold and ruff format --check.

## Acceptance

- [ ] CI green
${footer}`,
  },
  {
    title: '[50 MRG] Dataset adapter: public pose datasets index (license-safe)',
    labels: ['bounty', 'bounty: feature', 'data', 'documentation', 'reward:50-mrg'],
    body: `## Bounty: 50 MRG

\`docs/DATASETS.md\` + optional index loader for public pose/photography datasets (no redistributing restricted media).

## Acceptance

- [ ] ≥8 corpora rows with licenses
- [ ] Optional fixture adapter test
${footer}`,
  },
  {
    title: '[50 MRG] Metrics: hit@k, MRR, confusion between pose families',
    labels: ['bounty', 'bounty: feature', 'ml', 'reward:50-mrg'],
    body: `## Bounty: 50 MRG

Eval module + CLI export for ranking quality over scene fixtures.

## Acceptance

- [ ] \`poseguide eval report\`
- [ ] Unit tests for hit@k / MRR
${footer}`,
  },
  {
    title: '[50 MRG] Export pose joints to COCO / MediaPipe-compatible formats',
    labels: ['bounty', 'bounty: feature', 'data', 'ml', 'reward:50-mrg'],
    body: `## Bounty: 50 MRG

Interoperability export/import between PoseGuide JSON and common keypoint formats.

## Acceptance

- [ ] Round-trip tests on fixtures
- [ ] CLI export command
${footer}`,
  },
];

for (const issue of issues) {
  createIssue(issue.title, issue.body, issue.labels);
}

console.log(`Created ${issues.length} issues on ${REPO}`);
