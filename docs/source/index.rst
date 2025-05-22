sfm
===

.. image:: https://img.shields.io/badge/license-MIT-brightgreen
   :target: LICENSE
   :alt: MIT License

This project provides a lightweight, modular implementation of Structure-from-Motion (SfM) for 3D reconstruction using feature extraction, matching, and camera localization. It supports integration with SuperPoint for feature extraction, LightGlue for matching, and COLMAP models within the SfM pipeline.

Getting Started
---------------

Installation
^^^^^^^^^^^^

.. code-block:: bash

   git clone https://github.com/AllenNeuralDynamics/sfm.git
   cd sfm
   pip install .

Enable SuperPoint + LightGlue Reticle Detection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Parallax supports reticle detection using SuperPoint and LightGlue.

To enable reticle detection, you must manually download the pretrained models from the `SuperGluePretrainedNetwork` repository. This is not bundled with this project and is distributed under its own licensing terms. Please review their `license <https://github.com/magicleap/SuperGluePretrainedNetwork>`_ before use.

Manual Setup Instructions:

.. code-block:: bash

   git clone https://github.com/magicleap/SuperGluePretrainedNetwork.git external/SuperGluePretrainedNetwork

Folder structure should look like:

.. code-block:: text

   sfm/
   ├── external/
   │   └── SuperGluePretrainedNetwork/
   │       └── models/
   │           ├── superpoint.py
   │           └── weights/
   │               ├── superpoint_v1.pth
   │               └── superglue_indoor.pth

Running the Pipeline
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python -m sfm.scripts --image_dir /path/to/img_dir --query myimage.jpg --export_dir /path/to/export_dir

As output, it will print the pose — including the quaternion vector (*qvec*: QX, QY, QZ, QW) and translation vector (*tvec*) — of the **Blackfly S BFS-U3-120S4C** camera. It will also show the estimated camera pose.


Documentation
-------------

To generate `.rst` source files for documentation:

.. code-block:: bash

   sphinx-apidoc -o docs/source/ src

Then to build the HTML documentation:

.. code-block:: bash

   sphinx-build -b html docs/source/ docs/build/html


Contents
==================
.. toctree::
   :maxdepth: 2

   modules