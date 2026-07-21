import argparse
import json
from .export import export_pose

def add_export_command(subparsers):
    """Add export command to CLI."""
    export_parser = subparsers.add_parser('export', help='Export pose joints')
    export_parser.add_argument('--input', required=True, help='Input pose joints JSON file')
    export_parser.add_argument('--format', required=True, choices=['coco', 'mediapipe'], help='Export format')
    export_parser.add_argument('--output', required=True, help='Output file path')

def handle_export(args):
    """Handle export command."""
    try:
        with open(args.input, 'r') as f:
            pose_joints = json.load(f)

        exported_data = export_pose(pose_joints, args.format)

        with open(args.output, 'w') as f:
            json.dump(exported_data, f, indent=2)

        print(f"Successfully exported pose joints to {args.format} format at {args.output}")
    except Exception as e:
        print(f"Error exporting pose joints: {str(e)}")
        raise