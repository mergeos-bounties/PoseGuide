# PoseGuide

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-0.2.1-0E8A16.svg)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MergeOS](https://img.shields.io/badge/MergeOS-bounties-5319E7.svg)](https://github.com/mergeos-bounties)

**PoseGuide** is a photography **pose coach**: scene tags → ranked standing poses, stick-figure SVG overlays, and offline demos — no camera required for the CLI smoke path.

**Product:** [mergeos-bounties/PoseGuide](https://github.com/mergeos-bounties/PoseGuide)

---

## Table of contents

- [Highlights](#highlights)
- [Screenshots](#screenshots)
- [Quick start](#quick-start)
- [CLI reference](#cli-reference)
- [Presets & data](#presets--data)
- [Diagrams](#diagrams)
- [Repository layout](#repository-layout)
- [Development](#development)
- [MergeOS bounties](#mergeos-bounties)
- [License](#license)

---

## Highlights

| Mode | Description |
| --- | --- |
| **Scene → pose** | Tags (beach, urban, studio…) → ranked pose catalog matches |
| **SVG stick figure** | Render target pose joints as guidance overlay |
| **Score** | Compare subject landmarks vs target pose (scaffold) |
| **Train / eval** | Toy calibration loop + scene evaluation metrics |
| **Offline demo** | `poseguide demo --preset beach` end-to-end |

---

## Screenshots

Live demo captures (recommend + stick figure).

| Beach | Urban | Studio |
| :---: | :---: | :---: |
| ![Beach](docs/screenshots/demo-beach.png) | ![Urban](docs/screenshots/demo-urban.png) | ![Studio](docs/screenshots/demo-studio.png) |
| *Beach preset* | *Urban preset* | *Studio preset* |

---

## Quick start

```powershell
cd PoseGuide
python -m venv .venv
.\.venv\Scripts\activate
pip install -e ".[dev]"

poseguide version
poseguide demo --preset beach
poseguide poses list
poseguide scenes list
```

SVG / overlay outputs are written under the configured `OUT_DIR` (see `poseguide.config`).

---

## CLI reference

| Command | Purpose |
| --- | --- |
| `poseguide version` | Version + pose/scene counts |
| `poseguide demo -p beach` | Full recommend + SVG for a preset |
| `poseguide poses list` | Standing pose catalog |
| `poseguide poses svg -p <id>` | Render one pose SVG |
| `poseguide scenes list` | Scene samples |
| `poseguide guide …` | Recommend / score helpers |
| `poseguide train` / `eval` | Toy train + evaluation |

**Presets:** `beach` · `urban` · `studio` · `forest` · `office`

```powershell
poseguide demo -p urban
poseguide demo -p studio
```

---

## Presets & data

| Area | Location |
| --- | --- |
| Pose catalog | `data/poses/` |
| Scene samples | `data/scenes/` |
| Demo presets | `poseguide.guide.demo.PRESETS` |

---

## Diagrams

System architecture and workflow — full width. Open the HTML files for **dark/light theme** and export (PNG/SVG).

### Architecture

[Open interactive diagram](docs/diagrams/architecture.html)

<p align="center">
  <img src="docs/diagrams/architecture.svg" alt="PoseGuide architecture" width="100%" />
</p>

### Workflow

[Open interactive diagram](docs/diagrams/workflow.html)

<p align="center">
  <img src="docs/diagrams/workflow.svg" alt="PoseGuide workflow" width="100%" />
</p>

*Generated with [archify](https://github.com/tt-a1i).*

---

## Repository layout

```text
src/poseguide/
  cli.py
  guide/          # recommend, score, demo presets
  render/         # SVG stick figure, overlay JSON
  data/loader.py  # poses & scenes
  train/          # toy calibration
  eval/           # metrics
docs/screenshots/
docs/diagrams/
```

---

## Development

```powershell
pytest -q
ruff check src tests
poseguide demo -p beach
```

---

## MergeOS bounties

Star this repo + [mergeos](https://github.com/mergeos-bounties/mergeos) → claim bounty issue → PR to **master** → MRG **25–200**.

Evidence: demo SVG / stick-figure screenshots + recommend JSON.

---

## Tiếng Việt

**PoseGuide** gợi ý tư thế chụp ảnh theo scene (beach / urban / studio…), vẽ stick figure SVG. Chạy: `poseguide demo -p beach`.

---

## License

MIT · MergeOS / ThanhTrucSolutions
