# sfm
[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)

This project provides a lightweight, modular implementation of Structure-from-Motion (SfM) for 3D reconstruction using feature extraction, matching, and camera localization. It supports integration with SuperPoint for feature extraction, LightGlue for matching, and COLMAP models within the SfM pipeline.


##  Getting Started
### Installation
```bash
git clone https://github.com/AllenNeuralDynamics/sfm.git
cd sfm
pip install .
```

### Enable SuperPoint + SuperGlue Reticle Detection
Parallax supports reticle detection using SuperPoint + LightGlue.
To enable reticle detection using SuperPoint + SuperGlue, you must manually download 'SuperGluePretrainedNetwork' pretrained models.

The SuperGluePretrainedNetwork is not included in this repository and is distributed under its own licensing terms.
Please review their [license](https://github.com/magicleap/SuperGluePretrainedNetwork) before use.

Manual Setup Instructions
Clone the repository into the external/ folder in your Parallax project root:
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
As output, it will print the pose — including the quaternion vector (qvec: QX, QY, QZ, QW) and translation vector (tvec) — of the Blackfly S BFS-U3-120S4C camera.
Also, show the pose of camera. 

<img width="800" alt="example" src="https://github.com/user-attachments/assets/f8de8ba7-3d1d-4983-bfbf-992ff3482741" />


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


