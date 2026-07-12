from __future__ import annotations

from poseguide.eval.metrics import evaluate_scenes


def test_evaluate_scenes() -> None:
    report = evaluate_scenes(top_k=3)
    assert report["n_scenes"] >= 1
    assert report["hit_at_k"] is None or report["hit_at_k"] >= 0.5
