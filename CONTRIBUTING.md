# Contributing to PoseGuide

Thanks for contributing! PoseGuide recommends photography poses using pose estimation and scene analysis.

## Quick Start

```bash
git clone https://github.com/mergeos-bounties/PoseGuide.git
cd PoseGuide
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Development Loop

1. **Pick an issue** — browse [open bounties](https://github.com/mergeos-bounties/PoseGuide/issues?q=is%3Aissue+is%3Aopen+label%3Abounty)
2. **Claim it** — comment `I claim this bounty` on the issue AND on [MergeOS Claim Token #1](https://github.com/mergeos-bounties/mergeos/issues/1)
3. **Create a branch** — `git checkout -b fix/issue-NN-short-description`
4. **Implement** — write code + tests
5. **Verify locally** (same steps as GitHub Actions CI):
   ```bash
   pip install -e ".[dev]"
   ruff check src tests
   ruff format src tests          # apply style (required — CI runs format --check)
   ruff format --check src tests
   pytest -q --cov=src --cov-report=term --cov-fail-under=30
   # If you add/rename poses or scenes, regenerate the web demo catalog:
   python scripts/build-web-catalog.py
   ```
6. **Push and open PR** — target `master`, reference the issue with `Closes #NN`

### Why CI fails most often

| Symptom | Cause | Fix |
|---------|--------|-----|
| `Would reformat: …` | Code not run through `ruff format` | `ruff format src tests` then commit |
| Ruff F541 / lint | Style / unused imports | `ruff check --fix src tests` |
| Coverage below 30% | Missing tests | Add unit tests for new code |
| Web catalog assertion | `data/poses` out of sync with `web/data/catalog.json` | `python scripts/build-web-catalog.py` |
| Node 20 deprecation notice | Old Actions runtime warning only | Harmless; CI uses Node 24 actions (`checkout@v5`, `setup-python@v6`) |

Dev deps pin **ruff 0.15.x** so formatter rules match between your machine and CI.

## Acceptance Gates

| Gate | Command | Notes |
|------|---------|-------|
| Tests | `pytest -q` | All tests pass |
| Lint | `ruff check src tests` | No lint errors |
| Format | `ruff format --check src tests` | Consistent formatting |
| Coverage | `pytest --cov=src --cov-report=term` | CI enforces threshold |

## Good First Issues

Look for issues labelled `good first issue`. These are small, self-contained tasks ideal for new contributors:
- Documentation improvements
- Test coverage additions
- Small CLI features

## MergeOS Bounty Flow

1. Claim on the issue + MergeOS Claim Token #1
2. Submit PR to `mergeos-bounties/PoseGuide`
3. After merge, MRG tokens are awarded through the MergeOS ledger

## Need Help?

- Comment on the issue you're working on
- Check existing PRs for examples
- Read `AGENTS.md` for automated contribution rules
