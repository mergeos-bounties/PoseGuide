from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from poseguide import __version__
from poseguide.config import OUT_DIR
from poseguide.data.loader import list_pose_files, list_scene_files, load_pose, load_scene
from poseguide.guide.demo import PRESETS, run_demo
from poseguide.guide.recommend import recommend_for_scene_path, recommend_for_tags
from poseguide.guide.score import score_subject_against_pose
from poseguide.render.overlay import (
    VisionUnavailableError,
    render_overlay_png,
    write_guidance_overlay,
)
from poseguide.render.svg import render_pose_svg
from poseguide.eval.metrics import evaluate_scenes
from poseguide.train.toy_train import train_toy

app = typer.Typer(
    help="PoseGuide — photography pose guidance (scene → standing pose coach).",
    no_args_is_help=True,
)
poses_app = typer.Typer(help="Standing pose catalog")
scenes_app = typer.Typer(help="Background / scene samples")
guide_app = typer.Typer(help="Recommend and score poses")
train_app = typer.Typer(help="Training")
eval_app = typer.Typer(help="Evaluation")
data_app = typer.Typer(help="Data utilities (import/extract)")
app.add_typer(poses_app, name="poses")
app.add_typer(scenes_app, name="scenes")
app.add_typer(guide_app, name="guide")
app.add_typer(train_app, name="train")
app.add_typer(eval_app, name="eval")
app.add_typer(data_app, name="data")
console = Console()


@app.command("version")
def version_cmd() -> None:
    console.print(f"PoseGuide {__version__}")
    console.print(f"Poses: {len(list_pose_files())} | Scenes: {len(list_scene_files())}")


@app.command("stats")
def stats_cmd() -> None:
    """Catalog inventory: pose/scene counts and top tags."""
    from collections import Counter

    tags: Counter[str] = Counter()
    standing = 0
    for path in list_pose_files():
        pose = load_pose(path)
        if pose.get("standing"):
            standing += 1
        for t in pose.get("tags") or []:
            tags[str(t).lower()] += 1
    console.print_json(
        data={
            "version": __version__,
            "poses": len(list_pose_files()),
            "scenes": len(list_scene_files()),
            "standing_poses": standing,
            "top_tags": tags.most_common(10),
        }
    )


@app.command("demo")
def demo_cmd(
    preset: str = typer.Option("beach", "--preset", "-p", help="Scene preset to use when no image is provided"),
    image: Optional[Path] = typer.Option(None, "--image", "-i", exists=True, dir_okay=False, help="Input background image for overlay demo"),
    tags: Optional[str] = typer.Option(None, "--tags", "-t", help="Scene tags (comma-separated). If not provided with --image, attempt to infer from filename."),
    out: Optional[Path] = typer.Option(None, "--out", "-o", help="Output overlay image path (default: <input>_overlay.png when using --image)"),
    width: int = typer.Option(360, "--width", min=64, max=4096),
    height: int = typer.Option(480, "--height", min=64, max=4096),
) -> None:
    """End-to-end demo: preset scene tags → pose recommendations + SVG stick figure.
    If --image is provided, infer scene tags (or use provided tags) → recommend pose → render overlay on input image.
    """
    if image is not None:
        # Image-based demo
        # Infer tags from filename if not provided
        if tags is None:
            stem = image.stem.lower()
            # Known scene presets
            matched = [p for p in PRESETS if p in stem]
            if matched:
                tags = matched[0]
            else:
                tags = "beach"  # default
            console.print(f"[dim]Inferred scene tags from filename: {tags}[/dim]")
        else:
            console.print(f"[dim]Using provided scene tags: {tags}[/dim]")
        
        # Get top pose recommendation for the scene tags
        try:
            recs = recommend_for_tags(tags, top_k=1)
        except Exception as exc:
            console.print(f"[red]Failed to get recommendations for tags '{tags}': {exc}[/red]")
            raise typer.Exit(1) from exc
        
        if not recs or not recs.get("recommendations"):
            console.print(f"[red]No recommendations found for tags '{tags}'[/red]")
            raise typer.Exit(1)
        
        pose_id = str(recs["recommendations"][0]["pose_id"])
        console.print(f"[dim]Recommended pose: {pose_id}[/dim]")
        
        # Determine output path
        if out is None:
            out = image.parent / f"{image.stem}_overlay.png"
        
        # Render overlay
        try:
            path = render_overlay_png(pose_id, out, background=image, width=width, height=height)
        except VisionUnavailableError as exc:
            console.print(f"[red]{exc}[/red]")
            console.print("Please install the '[vision]' extra to use this feature: pip install -e '.[vision]'")
            raise typer.Exit(1) from exc
        except KeyError as exc:
            console.print(f"[red]{exc}[/red]")
            raise typer.Exit(1) from exc
        
        console.print(f"[green]Wrote overlay:[/green] {path}")
        console.print(f"[dim]Scene tags: {tags}[/dim]")
        console.print(f"[dim]Pose ID: {pose_id}[/dim]")
    else:
        # Preset-based demo (original behavior)
        try:
            result = run_demo(preset)
        except KeyError as exc:
            console.print(f"[red]{exc}[/red]")
            console.print(f"Presets: {', '.join(PRESETS)}")
            raise typer.Exit(1) from exc
        console.print_json(data=result)
        console.print(f"[green]SVG[/green] {result.get('svg_path')}")


@poses_app.command("list")
def poses_list() -> None:
    files = list_pose_files()
    if not files:
        console.print("[yellow]No poses in data/poses[/yellow]")
        raise typer.Exit()
    table = Table(title=f"Standing poses ({len(files)})")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Tags")
    for path in files:
        pose = load_pose(path)
        tags = ", ".join(pose.get("tags") or [])
        table.add_row(str(pose.get("id")), str(pose.get("name")), tags)
    console.print(table)


@poses_app.command("show")
def poses_show(
    pose_id: str = typer.Argument(..., help="Pose ID (filename stem without .json)"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON instead of table"),
) -> None:
    """Pretty-print a single pose by ID: joints summary + tips + camera cues."""
    # Find the pose file by stem
    pose_path = None
    for path in list_pose_files():
        if path.stem == pose_id:
            pose_path = path
            break

    if pose_path is None:
        available = [p.stem for p in list_pose_files()]
        hint = ""
        if available:
            closest = sorted(available, key=lambda x: len(set(x) & set(pose_id)), reverse=True)[:5]
            hint = f" Available: {', '.join(closest)}"
        console.print(f"[red]Pose '{pose_id}' not found.{hint}[/red]")
        raise typer.Exit(code=1)

    pose = load_pose(pose_path)

    if json_output:
        # Strip the numpy joint_vector (not JSON serializable) and print clean JSON
        pose_clean = {k: v for k, v in pose.items() if k != "joint_vector"}
        console.print_json(data=pose_clean)
        return

    # Rich table output
    table = Table(title=f"Pose: {pose.get('name', pose_id)} ({pose.get('id', pose_id)})")
    table.add_column("Field", style="bold cyan")
    table.add_column("Value", style="green")

    table.add_row("ID", str(pose.get("id", pose_id)))
    table.add_row("Name", str(pose.get("name", "")))
    table.add_row("Standing", "yes" if pose.get("standing") else "no")
    table.add_row("Tags", ", ".join(pose.get("tags") or []))
    table.add_row("Tips", "\n".join(f"  • {t}" for t in (pose.get("tips") or [])) or "(none)")
    table.add_row(
        "Camera Cues",
        "\n".join(f"  • {c}" for c in (pose.get("camera_cues") or [])) or "(none)",
    )

    # Joints summary table
    joints = pose.get("joints") or {}
    if joints:
        joint_table = Table(title="Joints")
        joint_table.add_column("Joint", style="bold")
        joint_table.add_column("X", justify="right")
        joint_table.add_column("Y", justify="right")
        joint_table.add_column("Z", justify="right")
        for joint_name in sorted(joints.keys()):
            xyz = joints[joint_name]
            x = f"{xyz[0]:.3f}" if len(xyz) > 0 else "-"
            y = f"{xyz[1]:.3f}" if len(xyz) > 1 else "-"
            z = f"{xyz[2]:.3f}" if len(xyz) > 2 else "-"
            joint_table.add_row(joint_name, x, y, z)
    else:
        joint_table = Table(title="Joints")
        joint_table.add_column("Joint", style="bold")
        joint_table.add_row("(no joints defined)")

    console.print(table)
    console.print(joint_table)


@poses_app.command("svg")
def poses_svg(
    pose: str = typer.Option(..., "--pose", "-p"),
    out: Optional[Path] = typer.Option(None, "--out", "-o"),
) -> None:
    out_path = out or (OUT_DIR / f"{pose}.svg")
    try:
        path = render_pose_svg(pose, out_path)
    except KeyError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc
    console.print(f"[green]Wrote[/green] {path}")


@poses_app.command("overlay")
def poses_overlay(
    pose: str = typer.Option(..., "--pose", "-p"),
    out: Optional[Path] = typer.Option(None, "--out", "-o"),
    background: Optional[Path] = typer.Option(None, "--bg", exists=True, dir_okay=False),
    width: int = typer.Option(360, "--width", min=64, max=4096),
    height: int = typer.Option(480, "--height", min=64, max=4096),
) -> None:
    """Render a PNG skeleton overlay for a target pose (needs vision extra)."""
    out_path = out or (OUT_DIR / f"{pose}_overlay.png")
    try:
        path = render_overlay_png(pose, out_path, background=background, width=width, height=height)
    except VisionUnavailableError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc
    except KeyError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc
    console.print(f"[green]Wrote[/green] {path}")


@scenes_app.command("list")
def scenes_list() -> None:
    files = list_scene_files()
    if not files:
        console.print("[yellow]No scenes in data/scenes[/yellow]")
        raise typer.Exit()
    table = Table(title=f"Scenes ({len(files)})")
    table.add_column("ID")
    table.add_column("Tags")
    table.add_column("Expected poses")
    for path in files:
        scene = load_scene(path)
        tags = ", ".join(scene.get("tags") or [])
        expected = ", ".join(scene.get("expected_poses") or [])
        table.add_row(str(scene.get("id")), tags, expected)
    console.print(table)


@guide_app.command("recommend")
def guide_recommend(
    scene: Optional[Path] = typer.Option(None, "--scene", "-s", exists=True, dir_okay=False),
    tags: Optional[str] = typer.Option(None, "--tags", "-t"),
    top: int = typer.Option(3, "--top", "-k", min=1, max=20),
    subject: Optional[Path] = typer.Option(None, "--subject", exists=True, dir_okay=False),
    overlay_out: Optional[Path] = typer.Option(None, "--overlay-out"),
    svg: bool = typer.Option(True, "--svg/--no-svg"),
    difficulty: Optional[str] = typer.Option(
        None, "--difficulty", "-d", help="Filter by difficulty: easy, medium, hard"
    ),
) -> None:
    if scene is None and not tags:
        console.print("[red]Provide --scene or --tags[/red]")
        raise typer.Exit(code=1)
    if scene is not None:
        result = recommend_for_scene_path(scene, top_k=top, subject_path=subject)
    else:
        result = recommend_for_tags(tags or "", top_k=top)
    if difficulty:
        recs = result.get("recommendations", [])
        before = len(recs)
        recs = [r for r in recs if r.get("difficulty", "medium") == difficulty]
        result["recommendations"] = recs
        console.print(f"[dim]difficulty={difficulty}[/dim] {before} -> {len(recs)} recommendations")
    console.print_json(data=result)
    out = overlay_out or (OUT_DIR / "last_overlay.json")
    path = write_guidance_overlay(result, out)
    console.print(f"[dim]overlay[/dim] {path}")
    if svg and result.get("recommendations"):
        pose_id = str(result["recommendations"][0]["pose_id"])
        svg_path = render_pose_svg(pose_id, OUT_DIR / f"{pose_id}.svg")
        console.print(f"[dim]svg[/dim] {svg_path}")


@guide_app.command("score")
def guide_score(
    pose: str = typer.Option(..., "--pose", "-p"),
    subject: Path = typer.Option(..., "--subject", "-i", exists=True, dir_okay=False),
) -> None:
    try:
        result = score_subject_against_pose(pose, subject)
    except KeyError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    console.print_json(data=result)


@guide_app.command("composition")
def guide_composition(pose: str = typer.Option(..., "--pose", "-p")) -> None:
    """Rule-of-thirds composition analysis for a catalog pose."""
    from poseguide.guide.composition import composition_report

    try:
        console.print_json(data=composition_report(pose))
    except KeyError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc


@guide_app.command("coach")
def guide_coach(
    pose: str = typer.Option(..., "--pose", "-p"),
    subject: Optional[Path] = typer.Option(None, "--subject", "-i", exists=True, dir_okay=False),
) -> None:
    """Coach mode: composition tips + target SVG (+ optional subject score)."""
    from poseguide.guide.composition import coach_bundle

    try:
        console.print_json(data=coach_bundle(pose, subject_path=subject))
    except KeyError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc


@guide_app.command("demo")
def guide_demo(preset: str = typer.Option("beach", "--preset", "-p")) -> None:
    """End-to-end demo: preset scene tags → pose recommendations + SVG stick figure."""
    try:
        result = run_demo(preset)
    except KeyError as exc:
        console.print(f"[red]{exc}[/red]")
        console.print(f"Presets: {', '.join(PRESETS)}")
        raise typer.Exit(1) from exc
    console.print_json(data=result)
    console.print(f"[green]SVG[/green] {result.get('svg_path')}")





@eval_app.command("scenes")
def eval_scenes(
    top: int = typer.Option(3, "--top", "-k", min=1, max=20),
    table: bool = typer.Option(True, "--table/--json", help="Rich per-scene table vs raw JSON"),
    markdown: Optional[Path] = typer.Option(
        None, "--md", "--markdown", help="Export results as Markdown file"
    ),
) -> None:
    """Evaluate hit@k / precision / recall over labeled scenes."""
    import json
    from poseguide.config import RUNS_DIR

    report = evaluate_scenes(top_k=top)
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    path = RUNS_DIR / "eval_scenes.json"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    console.print(
        f"[green]hit@{top}[/green]={report['hit_at_k']} "
        f"P@{top}={report.get('precision_at_k')} "
        f"R@{top}={report.get('recall_at_k')} "
        f"n={report['n_labeled']}/{report['n_scenes']}"
    )
    if table and report.get("rows"):
        t = Table(title=f"hit@{top} per scene")
        t.add_column("Scene")
        t.add_column("Hit")
        t.add_column("Top poses")
        t.add_column("Overlap")
        for row in report["rows"]:
            t.add_row(
                str(row.get("scene")),
                "yes" if row.get("hit") else "no",
                ", ".join(str(x) for x in (row.get("top") or [])[:top]),
                ", ".join(str(x) for x in (row.get("overlap") or [])),
            )
        console.print(t)
    else:
        console.print_json(data=report)
    if markdown:
        md_content = _build_markdown_report(report, top)
        markdown.write_text(md_content, encoding="utf-8")
        console.print(f"[green]Markdown report[/green] -> {markdown}")
    console.print(f"Report: {path}")


def _build_markdown_report(report: dict, top: int) -> str:
    """Build a Markdown evaluation report from scene results."""
    lines = [
        "# PoseGuide Evaluation Report",
        "",
        f"**hit@{top}**: {report.get('hit_at_k', 'N/A')}  ",
        f"**Precision@{top}**: {report.get('precision_at_k', 'N/A')}  ",
        f"**Recall@{top}**: {report.get('recall_at_k', 'N/A')}  ",
        f"**Labeled scenes**: {report.get('n_labeled', 0)} / {report.get('n_scenes', 0)}",
        "",
        "## Per-Scene Results",
        "",
        "| Scene | Hit | Top Poses | Overlap |",
        "|-------|-----|-----------|---------|",
    ]
    for row in report.get("rows", []):
        scene = str(row.get("scene", "?"))
        hit = "yes" if row.get("hit") else "no"
        top_poses = ", ".join(str(x) for x in (row.get("top") or [])[:top])
        overlap = ", ".join(str(x) for x in (row.get("overlap") or []))
        lines.append(f"| {scene} | {hit} | {top_poses} | {overlap} |")
    return "\n".join(lines) + "\n"


@poses_app.command("search")
def poses_search(
    query: str = typer.Argument(..., help="Substring over id/name/tags/tips/camera cues"),
    limit: int = typer.Option(15, "--limit", "-n", min=1, max=50),
) -> None:
    """Search standing pose catalog by id, name, tags, tips, or camera cues."""
    q = query.strip().lower()
    hits = []
    for path in list_pose_files():
        pose = load_pose(path)
        searchable = {
            "id": [str(pose.get("id") or "")],
            "name": [str(pose.get("name") or "")],
            "tags": [str(tag) for tag in (pose.get("tags") or [])],
            "tips": [str(tip) for tip in (pose.get("tips") or [])],
            "camera_cues": [str(cue) for cue in (pose.get("camera_cues") or [])],
        }
        matched_fields = [
            field
            for field, values in searchable.items()
            if any(q in value.lower() for value in values)
        ]
        if matched_fields:
            hits.append((pose, matched_fields))
        if len(hits) >= limit:
            break
    table = Table(title=f"Pose search: {query} ({len(hits)})")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Tags")
    table.add_column("Matched")
    for pose, matched_fields in hits:
        table.add_row(
            str(pose.get("id")),
            str(pose.get("name")),
            ", ".join((pose.get("tags") or [])[:6]),
            ", ".join(matched_fields),
        )
    console.print(table)


@train_app.command("toy")
def train_toy_cmd(epochs: int = typer.Option(3, "--epochs", "-e", min=1, max=50)) -> None:
    report = train_toy(epochs=epochs)
    last = report["history"][-1]["hit_rate_at_3"]
    console.print(f"[green]Training complete[/green] hit@3={last}")
    console.print(f"Report: {report['report_path']}")


@data_app.command("extract")
def data_extract(
    image: Path = typer.Option(..., "--image", "-i", exists=True, dir_okay=False),
    out: Path = typer.Option(..., "--out", "-o"),
) -> None:
    """Extract joints from a photo into a PoseGuide subject JSON (MediaPipe)."""
    from poseguide.data.extract import extract_to_file

    try:
        path = extract_to_file(image, out)
    except RuntimeError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    console.print(f"[green]Wrote[/green] {path}")


@train_app.command("report")
def train_report() -> None:
    path = Path("data/runs/toy_train_report.json")
    if not path.exists():
        console.print("[yellow]No report yet. Run: poseguide train toy[/yellow]")
        raise typer.Exit(code=1)
    console.print(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    app()
