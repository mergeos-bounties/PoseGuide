from __future__ import annotations

from typer.testing import CliRunner

from poseguide import cli
from poseguide.guide.scene_tagger import infer_scene_tags


runner = CliRunner()


def test_infer_scene_tags_from_description() -> None:
    tags = infer_scene_tags(description="Portrait at a beach during sunset")

    assert tags == ["beach", "outdoor", "portrait", "golden_hour"]


def test_infer_scene_tags_from_image_fixture(tmp_path) -> None:
    image = tmp_path / "urban_brick_wall.jpg"
    image.write_bytes(b"offline image fixture")

    tags = infer_scene_tags(image_path=image)

    assert tags == ["urban", "outdoor", "wall"]


def test_guide_recommend_uses_inferred_tags(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(cli, "OUT_DIR", tmp_path)

    result = runner.invoke(
        cli.app,
        ["guide", "recommend", "--description", "sunset beach", "--no-svg"],
    )

    assert result.exit_code == 0
    assert '"inferred_scene_tags":' in result.output
    assert '"beach"' in result.output
    assert '"golden_hour"' in result.output


def test_guide_recommend_rejects_unknown_description() -> None:
    result = runner.invoke(
        cli.app,
        ["guide", "recommend", "--description", "plain backdropless photograph", "--no-svg"],
    )

    assert result.exit_code == 1
    assert "No scene tags inferred" in result.output
