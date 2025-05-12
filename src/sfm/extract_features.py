import pprint
from pathlib import Path
from typing import Dict, Optional, Union

import cv2
import h5py
import numpy as np
import torch
import logging

from . import extractors
from .utils.base_model import dynamic_load
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

@torch.no_grad()
def main(
    conf: Dict,
    image_dir: Union[str, Path],
    image: Union[str, Path],
    export_path: Optional[Path] = None,
    as_half: bool = True,
) -> Path:
    """Extract local features from an image path and save to an HDF5 file."""
    image_path = Path(image_dir/image)
    assert image_path.exists(), f"Image not found: {image_path}"

    logger.info(f"Extracting features from {image_path} with configuration:\n{pprint.pformat(conf)}")

    if export_path is None:
        export_path = Path("features", conf["output"] + ".h5")
    export_path.parent.mkdir(exist_ok=True, parents=True)

    # Load image as BGR numpy array
    image_data = cv2.imread(str(image_dir/image), cv2.IMREAD_COLOR)
    assert image_data is not None, f"Failed to read image: {image_path}"

    # Preprocess
    original_size = np.array(image_data.shape[:2][::-1])  # width, height
    image_data = image_data.astype(np.float32)

    if conf["preprocessing"].get("resize_max") is not None:
        max_dim = conf["preprocessing"]["resize_max"]
        if max(original_size) > max_dim:
            scale = max_dim / max(original_size)
            new_size = tuple(int(round(x * scale)) for x in original_size)
            image_data = cv2.resize(image_data, new_size, interpolation=cv2.INTER_AREA)

    if conf["preprocessing"].get("grayscale", False):
        if image_data.ndim == 3:
            image_data = cv2.cvtColor(image_data, cv2.COLOR_RGB2GRAY)
        image_data = image_data[None]  # 1 x H x W
    else:
        image_data = image_data.transpose(2, 0, 1)  # C x H x W

    image_data = image_data / 255.0
    tensor = torch.from_numpy(image_data).unsqueeze(0)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    Model = dynamic_load(extractors, conf["model"]["name"])
    model = Model(conf["model"]).eval().to(device)

    pred = model({"image": tensor.to(device)})
    pred = {k: v[0].cpu().numpy() for k, v in pred.items()}
    pred["image_size"] = original_size

    if "keypoints" in pred:
        proc_size = np.array(image_data.shape[1:][::-1])  # processed image size: W, H
        scales = (original_size / proc_size).astype(np.float32)
        pred["keypoints"] = (pred["keypoints"] + 0.5) * scales[None] - 0.5
        if "scales" in pred:
            pred["scales"] *= scales.mean()
        uncertainty = getattr(model, "detection_noise", 1) * scales.mean()

    if as_half:
        for k, v in pred.items():
            if v.dtype == np.float32:
                pred[k] = v.astype(np.float16)

    # Use relative image path as key (preserves folder structure in h5)
    image_name = Path(image).as_posix()

    with h5py.File(str(export_path), "a", libver="latest") as fd:
        if image_name in fd:
            del fd[image_name]
        grp = fd.create_group(image_name)
        for k, v in pred.items():
            grp.create_dataset(k, data=v)
        if "keypoints" in pred:
            grp["keypoints"].attrs["uncertainty"] = uncertainty

    logger.info(f"Finished exporting features to: {export_path}")
    return export_path
