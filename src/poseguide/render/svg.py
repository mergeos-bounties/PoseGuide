from __future__ import annotations

from pathlib import Path

from poseguide.models.catalog import get_pose_by_id


# Stick figure edges (joint name pairs)
EDGES = [
    ("nose", "l_shoulder"),
    ("nose", "r_shoulder"),
    ("l_shoulder", "r_shoulder"),
    ("l_shoulder", "l_elbow"),
    ("l_elbow", "l_wrist"),
    ("r_shoulder", "r_elbow"),
    ("r_elbow", "r_wrist"),
    ("l_shoulder", "l_hip"),
    ("r_shoulder", "r_hip"),
    ("l_hip", "r_hip"),
    ("l_hip", "l_knee"),
    ("l_knee", "l_ankle"),
    ("r_hip", "r_knee"),
    ("r_knee", "r_ankle"),
]


def _pt(joints: dict, name: str, w: int, h: int) -> tuple[float, float] | None:
    xyz = joints.get(name)
    if not xyz or len(xyz) < 2:
        return None
    return float(xyz[0]) * w, float(xyz[1]) * h


def render_pose_svg(pose_id: str, out_path: Path, *, width: int = 360, height: int = 480) -> Path:
    pose = get_pose_by_id(pose_id)
    if pose is None:
        raise KeyError(f"unknown pose {pose_id!r}")
    joints = pose.get("joints") or {}
    lines = []
    for a, b in EDGES:
        pa, pb = _pt(joints, a, width, height), _pt(joints, b, width, height)
        if pa and pb:
            lines.append(
                f'<line x1="{pa[0]:.1f}" y1="{pa[1]:.1f}" x2="{pb[0]:.1f}" y2="{pb[1]:.1f}" '
                f'stroke="#0ea5e9" stroke-width="4" stroke-linecap="round"/>'
            )
    dots = []
    for name, xyz in joints.items():
        if not isinstance(xyz, (list, tuple)) or len(xyz) < 2:
            continue
        x, y = float(xyz[0]) * width, float(xyz[1]) * height
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#0369a1"/>')
    title = pose.get("name") or pose_id
    tips = pose.get("tips") or []
    tip_text = " · ".join(str(t) for t in tips[:2])
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#0f172a"/>
  <text x="16" y="28" fill="#e2e8f0" font-family="system-ui,sans-serif" font-size="16">{title}</text>
  <text x="16" y="48" fill="#94a3b8" font-family="system-ui,sans-serif" font-size="11">{tip_text}</text>
  <g transform="translate(0,20)">
    {"".join(lines)}
    {"".join(dots)}
  </g>
</svg>
'''
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(svg, encoding="utf-8")
    return out_path
