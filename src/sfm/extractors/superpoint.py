import sys
from pathlib import Path
import os

import torch
from ..utils.base_model import BaseModel

# 1. Check if Parallax provided an external path via environment variable
external_path_str = os.environ.get("PARALLAX_EXTERNAL_PATH")
if external_path_str:
    external_path = Path(external_path_str)
    if external_path.exists() and str(external_path) not in sys.path:
        sys.path.append(str(external_path))
        print(f"[INFO] Using external path from PARALLAX_EXTERNAL_PATH: {external_path}")
else:
    print("[INFO] Using pretrained model in sfm/external/...")
    # 2. Fallback to local path resolution (sfm/external)
    local_external = Path(__file__).resolve().parent.parent.parent.parent / "external"
    if local_external.exists() and str(local_external) not in sys.path:
        sys.path.append(str(local_external))
        print(f"[INFO] Using local external path: {local_external}")

from SuperGluePretrainedNetwork.models import superpoint  # noqa E402

# The original keypoint sampling is incorrect. We patch it here but
# we don't fix it upstream to not impact exisiting evaluations.
def sample_descriptors_fix_sampling(keypoints, descriptors, s: int = 8):
    """Interpolate descriptors at keypoint locations"""
    b, c, h, w = descriptors.shape
    keypoints = (keypoints + 0.5) / (keypoints.new_tensor([w, h]) * s)
    keypoints = keypoints * 2 - 1  # normalize to (-1, 1)
    descriptors = torch.nn.functional.grid_sample(
        descriptors, keypoints.view(b, 1, -1, 2), mode="bilinear", align_corners=False
    )
    descriptors = torch.nn.functional.normalize(
        descriptors.reshape(b, c, -1), p=2, dim=1
    )
    return descriptors


class SuperPoint(BaseModel):
    default_conf = {
        "nms_radius": 4,
        "keypoint_threshold": 0.005,
        "max_keypoints": -1,
        "remove_borders": 4,
        "fix_sampling": False,
    }
    required_inputs = ["image"]
    detection_noise = 2.0

    def _init(self, conf):
        if conf["fix_sampling"]:
            superpoint.sample_descriptors = sample_descriptors_fix_sampling
        self.net = superpoint.SuperPoint(conf)

    def _forward(self, data):
        return self.net(data)
