# Public Pose & Photography Datasets Index

A curated index of publicly available datasets for human pose estimation, photography
pose guidance, and body composition research. This document is **license-safe**: it
contains metadata only and does **not** redistribute any restricted media.

> **Note:** Each dataset has its own license terms. Always review the original license
> before downloading or using any dataset. "Research use only" datasets must not be
> used for commercial purposes without explicit permission from the copyright holders.

---

## Summary Table

| # | Dataset | Description | Keypoints | License | Link |
|---|---------|-------------|-----------|---------|------|
| 1 | **COCO Keypoints** | Large-scale object detection & pose estimation dataset. 250K+ people with keypoints across 330K images. | 17 | CC BY 4.0 (annotations); images retain original Flickr licenses | [cocodataset.org](https://cocodataset.org/) |
| 2 | **MPII Human Pose** | Single-person pose estimation benchmark. ~25K images, 40K+ annotated people across 410 everyday activities. | 16 | BSD 2-Clause (annotations); images for research only, no commercial use | [human-pose.mpi-inf.mpg.de](http://human-pose.mpi-inf.mpg.de/) |
| 3 | **PoseTrack** | Video-based multi-person pose estimation and articulated tracking. 514 videos, 66K+ frames. | 15 | Free for research purposes | [posetrack.net](https://posetrack.net/) |
| 4 | **Human3.6M** | Large-scale 3D human pose dataset. 3.6M poses from 11 actors, 4 camera views, 15 scenarios. | 32 (3D) | Free for academic use only; commercial use requires license | [vision.imar.ro/human3.6m](http://vision.imar.ro/human3.6m/) |
| 5 | **Leeds Sports Pose (LSP / LSPET)** | Sports pose dataset. LSP: 2K images; LSP Extended: 10K images from Flickr (parkour, gymnastics, athletics). | 14 | Research use; images retain Flickr licenses | [sam.johnson.io/research/lspet.html](http://sam.johnson.io/research/lspet.html) |
| 6 | **DensePose-COCO** | Dense image-to-surface correspondences annotated on COCO images. 50K+ instances with UV surface maps. | Dense (surface) | CC BY-NC 4.0 | [densepose.org](https://densepose.org/) |
| 7 | **MPI-INF-3DHP** | 3D human pose estimation with indoor and outdoor scenes. 1.3M+ frames, 8 subjects, 14 camera angles. | 28 (3D) | Research purposes only; non-commercial | [vcai.mpi-inf.mpg.de/3dhp-dataset](https://vcai.mpi-inf.mpg.de/3dhp-dataset/) |
| 8 | **CrowdPose** | Crowded-scenes pose estimation benchmark. 20K images, 80K human instances with 14 keypoints. | 14 | Research use | [github.com/Jeff-sjtu/CrowdPose](https://github.com/Jeff-sjtu/CrowdPose) |
| 9 | **Penn Action** | Human action and pose estimation from video. 2,326 sequences, 15 action categories, 13 joints. | 13 | Research use | [dreamdragon.github.io/PennAction](http://dreamdragon.github.io/PennAction/) |
| 10 | **AI Challenger Human Pose** | Large-scale Chinese human pose estimation dataset. 300K+ images with 14 keypoints. | 14 | Free for research and education | [AIChallenger/AI_Challenger_2017](https://github.com/AIChallenger/AI_Challenger_2017) |

---

## Detailed Descriptions

### 1. COCO Keypoints (Common Objects in Context)

- **Homepage:** <https://cocodataset.org/>
- **Paper:** Lin et al., "Microsoft COCO: Common Objects in Context," ECCV 2014
- **Annotations:** 17 keypoints per person (nose, eyes, ears, shoulders, elbows, wrists, hips, knees, ankles)
- **License:** CC BY 4.0 for annotations. Images are sourced from Flickr and retain their original licenses.
- **Use case:** General-purpose pose estimation, multi-person detection, benchmarking

### 2. MPII Human Pose

- **Homepage:** <http://human-pose.mpi-inf.mpg.de/>
- **Paper:** Andriluka et al., "2D Human Pose Estimation: New Benchmark and State of the Art Analysis," CVPR 2014
- **Annotations:** 16 body joints per person, activity labels for 410 categories
- **License:** BSD 2-Clause for annotations. Images are for research purposes only; commercial use is not allowed.
- **Use case:** Single-person pose estimation, activity-aware pose analysis

### 3. PoseTrack

- **Homepage:** <https://posetrack.net/>
- **Paper:** Andriluka et al., "PoseTrack: A Benchmark for Human Pose Estimation and Tracking," CVPR 2018
- **Annotations:** 15 keypoints, person track IDs, head bounding boxes
- **License:** Free for research purposes
- **Use case:** Video-based pose estimation, multi-person tracking, temporal consistency

### 4. Human3.6M

- **Homepage:** <http://vision.imar.ro/human3.6m/>
- **Paper:** Ionescu et al., "Human3.6M: Large Scale Datasets and Predictive Methods for 3D Human Sensing in Natural Environments," IEEE TPAMI 2014
- **Annotations:** 3D joint positions from motion capture, 4 camera views, pixel-level body part labels
- **License:** Free for academic use only. Commercial licensing available upon request.
- **Use case:** 3D human pose estimation, view-invariant pose analysis

### 5. Leeds Sports Pose (LSP / LSPET)

- **Homepage:** <http://sam.johnson.io/research/lspet.html>
- **Paper:** Johnson & Everingham, "Learning Effective Human Pose Estimation from Inaccurate Annotation," CVPR 2011
- **Annotations:** 14 joints per person (ankles, knees, hips, wrists, elbows, shoulders, neck, head top)
- **License:** Research use. Images sourced from Flickr retain original licenses.
- **Use case:** Sports pose estimation, learning from noisy annotations

### 6. DensePose-COCO

- **Homepage:** <https://densepose.org/>
- **Paper:** Güler et al., "DensePose: Dense Human Pose Estimation In The Wild," CVPR 2018
- **Annotations:** Dense surface correspondences (UV maps) for 50K+ person instances on COCO images
- **License:** CC BY-NC 4.0
- **Use case:** Dense pose estimation, surface-level body analysis, texture mapping

### 7. MPI-INF-3DHP

- **Homepage:** <https://vcai.mpi-inf.mpg.de/3dhp-dataset/>
- **Paper:** Mehta et al., "Monocular 3D Human Pose Estimation In The Wild Using Improved CNN Supervision," 3DV 2017
- **Annotations:** 3D joint positions, 14 camera views, indoor and outdoor scenes
- **License:** Research purposes only; non-commercial use
- **Use case:** 3D pose estimation in the wild, multi-view pose analysis

### 8. CrowdPose

- **Homepage:** <https://github.com/Jeff-sjtu/CrowdPose>
- **Paper:** Li et al., "CrowdPose: Efficient Crowded Scenes Pose Estimation and A New Benchmark," CVPR 2019
- **Annotations:** 14 keypoints per person, crowd index annotation
- **License:** Research use
- **Use case:** Pose estimation in crowded scenes, robustness to occlusion

### 9. Penn Action

- **Homepage:** <http://dreamdragon.github.io/PennAction/>
- **Paper:** Zhang et al., "From Actemes to Action Pose: A Weakly Supervised Approach," CVPR 2013
- **Annotations:** 13 joints per person, action labels for 15 categories
- **License:** Research use
- **Use case:** Action recognition, pose estimation from video sequences

### 10. AI Challenger Human Pose

- **Homepage:** <https://github.com/AIChallenger/AI_Challenger_2017>
- **Paper:** Wu et al., "AI Challenger: A Large-scale Dataset for Going Deeper in Image Understanding," 2017
- **Annotations:** 14 keypoints per person, 300K+ images
- **License:** Free for research and education
- **Use case:** Large-scale pose estimation, cross-cultural pose analysis

---

## Usage Guidelines for PoseGuide

When integrating external datasets into PoseGuide:

1. **Respect license terms** — Never redistribute dataset images or annotations outside their original license.
2. **Attribute properly** — Include dataset citations in any published work or derivative models.
3. **Research-only datasets** — Datasets marked "research use only" or "academic use only" must not be used to train commercial models without explicit permission.
4. **No restricted media** — This index contains metadata only. Do not commit dataset images or annotations to this repository.

---

## Contributing

To add a new dataset to this index:

1. Verify the dataset is publicly accessible
2. Confirm the license terms from the official source
3. Add a row to the summary table and a detailed description section
4. Submit a PR with the update

See [CONTRIBUTE_POSE_PACK.md](CONTRIBUTE_POSE_PACK.md) for general contribution guidelines.