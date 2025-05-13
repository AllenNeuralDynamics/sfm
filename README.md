# aind-python-library-template
[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)


This is a repository template to quickly setup a python library project. This repository utilizes a tool called **uv** to handle all dependency and package management. For more information on this tool go to the [uv wiki](https://docs.astral.sh/uv/). 

##  Getting Started

```bash
pip install -e .
python -m sfm.main
```
### Optional: Enable SuperPoint + SuperGlue Reticle Detection
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

## Documentation
To generate the rst files source files for documentation, run
```bash
sphinx-apidoc -o docs/source/ src
```
Then to create the documentation HTML files, run
```bash
sphinx-build -b html docs/source/ docs/build/html
```


