"""Batch SVG render for pose packs."""

from pathlib import Path
import json

def render_pose_svg(pose):
    """Render a single pose to SVG string."""
    joints = pose.get('joints', {})
    svg = '<svg width="200" height="300" xmlns="http://www.w3.org/2000/svg">'
    svg += '<rect width="100%" height="100%" fill="white"/>'
    
    for joint, coords in joints.items():
        x = coords[0] * 100 + 100
        y = 250 - coords[1] * 100
        svg += f'<circle cx="{x}" cy="{y}" r="5" fill="blue"/>'
        svg += f'<text x="{x+5}" y="{y}" font-size="10">{joint}</text>'
    
    svg += '</svg>'
    return svg

def render_all_poses(poses_dir, output_dir):
    """Render all poses in a pack to SVG files."""
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    
    count = 0
    for f in Path(poses_dir).glob('*.json'):
        pose = json.loads(f.read_text())
        svg = render_pose_svg(pose)
        svg_file = output / f'{f.stem}.svg'
        svg_file.write_text(svg)
        count += 1
    
    return count
