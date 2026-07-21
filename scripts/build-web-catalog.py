import json
import os
from pose_guide.export import export_pose

def build_web_catalog():
    """Build web demo catalog with exported pose formats."""
    # Load poses from fixtures
    with open('tests/fixtures/export_fixtures.json', 'r') as f:
        fixtures = json.load(f)

    # Create output directory if it doesn't exist
    os.makedirs('web/catalog', exist_ok=True)

    # Export each pose in both formats
    for pose_name, pose_joints in fixtures.items():
        # Export to COCO format
        coco_data = export_pose(pose_joints, 'coco')
        with open(f'web/catalog/{pose_name}_coco.json', 'w') as f:
            json.dump(coco_data, f, indent=2)

        # Export to MediaPipe format
        mediapipe_data = export_pose(pose_joints, 'mediapipe')
        with open(f'web/catalog/{pose_name}_mediapipe.json', 'w') as f:
            json.dump(mediapipe_data, f, indent=2)

    print("Web catalog built successfully")

if __name__ == '__main__':
    build_web_catalog()