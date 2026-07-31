# sfm
[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)

This project provides a modular implementation of Structure-from-Motion (SfM) for 3D reconstruction using feature extraction, matching, and camera localization. It is specifically designed to work with a database of reticle images, supporting integration with SuperPoint for feature extraction, SuperGlue/LightGlue for matching, and COLMAP models within the SfM pipeline.

## Requirements

- Python 3.8 or higher

## Installation

```bash
git clone https://github.com/AllenNeuralDynamics/sfm.git
cd sfm
pip install -e .
```

### Enable SuperPoint + SuperGlue Reticle Detection
Sfm supports reticle detection using SuperPoint + LightGlue.
To enable reticle detection using SuperPoint + SuperGlue, you must manually download 'SuperGluePretrainedNetwork' pretrained models.

The SuperGluePretrainedNetwork is not included in this repository and is distributed under its own licensing terms.
Please review their [license](https://github.com/magicleap/SuperGluePretrainedNetwork) before use.

Manual Setup Instructions
Clone the repository into the external/ folder in your project root:
```bash
git clone https://github.com/magicleap/SuperGluePretrainedNetwork.git external/SuperGluePretrainedNetwork
```
Verify your folder structure looks like this:
```bash
sfm/
├── external/
│   └── SuperGluePretrainedNetwork/
│       └── models/
│           ├── superpoint.py
│           └── weights/
│               ├── superpoint_v1.pth
│               └── superglue_indoor.pth
```

Run,

```bash
python -m sfm.scripts --image_dir /path/to/img_dir --query myimage.jpg --export_dir /path/to/export_dir
```
As output, it will print the pose — including the quaternion vector (qvec: QX, QY, QZ, QW) and translation vector (tvec) — of intrisics of the Blackfly S BFS-U3-120S4C camera.
Also, show the pose of camera. 

<img width="800" alt="example" src="https://github.com/user-attachments/assets/f8de8ba7-3d1d-4983-bfbf-992ff3482741" />
From images, red shows the camera pose in the database, yellow shows the reticle images in the database and green shows quering camera and conisible reticle points. 

### Example
Run the following command to visualize the results:
```bash
python -m sfm.scripts --image_dir .\tests\test_img_dir\ --query img.png --export_dir .\tests\output\
```

### How It Works (The Pipeline)
The core goal of this pipeline is to estimate the 6-Degrees-of-Freedom (6-DoF) pose of a new camera by comparing a query image against a pre-established database. This database contains a set of reticle images, each paired with its known camera pose (extrinsic parameters) and camera intrinsics.

The Database (Offline SfM): The system relies on a pre-built reference database of reticle images. Through an offline Structure-from-Motion process (via COLMAP), a foundational 3D point cloud is constructed, and the exact extrinsics (rotation/translation) and intrinsics (focal length, optical center, etc.) for every reticle image in the database are established.

Feature Extraction: For any new query image, the pipeline uses SuperPoint (a deep-learning-based feature detector) to extract keypoints and descriptors. The reticle patterns in the field of view serve as anchor points.

Feature Matching: The query image features are matched against the database images using SuperGlue (or LightGlue). These graph-neural-network matchers excel at finding correspondences even with repetitive structures or lighting variations.

Camera Localization (Online PnP): Using the 2D-to-2D matches between the query image and the database images, the system links the 2D query pixels to the existing 3D map from the database. It then uses a Perspective-n-Point (PnP) solver (often with RANSAC) to calculate the exact rotation (quaternion) and translation vectors of the query camera relative to the established reticle map.

## Documentation
To generate the rst files source files for documentation, run

```bash
sphinx-apidoc -o docs/source/ src/sfm
```
Then to create the documentation HTML files, run
```bash
sphinx-build -b html docs/source/ docs/build/html
```

## Acknowledgment
Portions of this codebase are adapted from the [Hierarchical Localization](https://github.com/cvg/Hierarchical-Localization) project by the Computer Vision Group at ETH Zurich. We thank the authors for their excellent work and open-source contribution.
