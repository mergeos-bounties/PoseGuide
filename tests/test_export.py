import unittest
import json
from pose_guide.export import coco_format, mediapipe_format, export_pose

class TestExport(unittest.TestCase):
    def setUp(self):
        self.test_pose = [
            {'x': 10, 'y': 20, 'score': 0.9},
            {'x': 30, 'y': 40, 'score': 0.8},
            {'x': 50, 'y': 60}
        ]

    def test_coco_format(self):
        result = coco_format(self.test_pose)
        self.assertEqual(result['num_keypoints'], 3)
        self.assertEqual(len(result['keypoints']), 9)
        self.assertEqual(result['keypoints'][0], 10)
        self.assertEqual(result['keypoints'][1], 20)
        self.assertEqual(result['keypoints'][2], 0.9)
        self.assertEqual(result['keypoints'][6], 50)
        self.assertEqual(result['keypoints'][7], 60)
        self.assertEqual(result['keypoints'][8], 1.0)

    def test_mediapipe_format(self):
        result = mediapipe_format(self.test_pose)
        self.assertEqual(len(result['keypoints']), 3)
        self.assertEqual(result['keypoints'][0]['x'], 10)
        self.assertEqual(result['keypoints'][0]['y'], 20)
        self.assertEqual(result['keypoints'][0]['score'], 0.9)
        self.assertEqual(result['keypoints'][2]['x'], 50)
        self.assertEqual(result['keypoints'][2]['y'], 60)
        self.assertEqual(result['keypoints'][2]['score'], 1.0)

    def test_export_pose(self):
        coco_result = export_pose(self.test_pose, 'coco')
        self.assertEqual(coco_result['num_keypoints'], 3)

        mediapipe_result = export_pose(self.test_pose, 'mediapipe')
        self.assertEqual(len(mediapipe_result['keypoints']), 3)

        with self.assertRaises(ValueError):
            export_pose(self.test_pose, 'invalid')

    def test_round_trip(self):
        # Test round-trip for COCO format
        coco_exported = coco_format(self.test_pose)
        coco_imported = []
        for i in range(0, len(coco_exported['keypoints']), 3):
            coco_imported.append({
                'x': coco_exported['keypoints'][i],
                'y': coco_exported['keypoints'][i+1],
                'score': coco_exported['keypoints'][i+2]
            })
        self.assertEqual(len(coco_imported), len(self.test_pose))

        # Test round-trip for MediaPipe format
        mediapipe_exported = mediapipe_format(self.test_pose)
        mediapipe_imported = []
        for keypoint in mediapipe_exported['keypoints']:
            mediapipe_imported.append({
                'x': keypoint['x'],
                'y': keypoint['y'],
                'score': keypoint['score']
            })
        self.assertEqual(len(mediapipe_imported), len(self.test_pose))

if __name__ == '__main__':
    unittest.main()