from __future__ import annotations

import json
from pathlib import Path

from poseguide.data.loader import list_pose_files, list_scene_files, load_pose, load_scene


ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "web"


def test_web_demo_assets_are_present_and_mobile_ready() -> None:
    index = WEB_DIR / "index.html"
    stylesheet = WEB_DIR / "styles.css"
    app = WEB_DIR / "app.js"

    assert index.exists(), "web/index.html is missing"
    assert stylesheet.exists(), "web/styles.css is missing"
    assert app.exists(), "web/app.js is missing"

    html = index.read_text(encoding="utf-8")
    css = stylesheet.read_text(encoding="utf-8")
    script = app.read_text(encoding="utf-8")

    assert '<meta name="viewport"' in html
    assert 'type="file"' in html
    assert "web/data/catalog.json" in script
    assert "@media" in css
    assert "max-width" in css


def test_web_catalog_is_synced_with_poseguide_data() -> None:
    catalog_path = WEB_DIR / "data" / "catalog.json"
    assert catalog_path.exists(), "web/data/catalog.json is missing"

    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    source_poses = [load_pose(path) for path in list_pose_files()]
    source_scenes = [load_scene(path) for path in list_scene_files()]

    assert sorted(pose["id"] for pose in catalog["poses"]) == sorted(
        str(pose["id"]) for pose in source_poses
    )
    assert sorted(scene["id"] for scene in catalog["scenes"]) == sorted(
        str(scene["id"]) for scene in source_scenes
    )
    assert all("joint_vector" not in pose for pose in catalog["poses"])
    assert all(pose.get("tips") for pose in catalog["poses"])


def test_web_demo_documents_local_api_fallback() -> None:
    readme = WEB_DIR / "README.md"
    assert readme.exists(), "web/README.md is missing"

    body = readme.read_text(encoding="utf-8")
    assert "python -m http.server" in body
    assert "Local API" in body
    assert "offline catalog" in body
    assert "screenshots" in body.lower()
