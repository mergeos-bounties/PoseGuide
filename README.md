# PoseGuide

**PoseGuide** trains and runs **photography pose guidance**:

| Mode | Description |
| --- | --- |
| **Scene → pose** | Background / scene tags → ranked standing poses |
| **Live coach** | Compare a subject's landmarks to a target pose (scaffold) |
| **Overlay** | Emit guidance cues for framing (JSON / text overlay stubs) |

Built under [mergeos-bounties](https://github.com/mergeos-bounties) so delivery can be funded as MergeOS tasks with MRG payouts.


## Screenshots

Real captures from running the product demo (PoseGuide).

![Beach preset · pose recommend + stick figure](docs/screenshots/demo-beach.png)

*Beach preset · pose recommend + stick figure*

![Urban preset demo](docs/screenshots/demo-urban.png)

*Urban preset demo*

![Studio preset demo](docs/screenshots/demo-studio.png)

*Studio preset demo*

## Stack

- Python 3.11+
- CLI: `typer` + `rich`
- Pose library + scene samples (JSON)
- Toy ranker (tag overlap + landmark prototypes)
- Optional vision extras (MediaPipe / OpenCV) via bounties
- Inference API sketch (FastAPI optional)

## Quick start

```bash
cd PoseGuide
python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -e ".[dev]"
poseguide --help
```

## Commands (runnable)

```bash
poseguide version
poseguide demo --preset beach          # recommend + SVG stick figure
poseguide poses list
poseguide scenes list
poseguide guide recommend --tags "urban,wall,daylight" --top 3
poseguide guide score --pose contrapposto --subject data/samples/subject_contrapposto.json
poseguide poses svg --pose power_stance --out data/out/power.svg
poseguide train toy --epochs 3
```

## Layout

```
src/poseguide/
  cli.py
  config.py
  data/           # loaders for poses + scenes
  models/         # toy ranker + pose library
  guide/          # recommend + score pipelines
  train/          # training stubs
  render/         # overlay / cue stubs
  api/            # optional FastAPI
data/poses/       # standing pose templates
data/scenes/      # background / scene samples
data/samples/     # subject landmark demos
docs/BOUNTY.md
```

## MergeOS bounties

1. Star this repo + [mergeos](https://github.com/mergeos-bounties/mergeos)
2. Claim an issue labeled `bounty`
3. Also claim on MergeOS [issue #1](https://github.com/mergeos-bounties/mergeos/issues/1)
4. Open a PR with tests/evidence
5. Maintainer merges and credits MRG (25/50/100/200)

See [docs/BOUNTY.md](docs/BOUNTY.md).

## Privacy

- Prefer consented photos and public pose datasets with clear licenses.
- Do not ship private client images without permission.
- Document dataset licenses in every PR that adds data.

## License

MIT
