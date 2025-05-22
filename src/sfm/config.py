from pathlib import Path
import pycolmap

feature_conf_list = {
    "superpoint_parallax": {
        "output": "feats-superpoint-n1024-r4000",
        "model": {
            "name": "superpoint",
            "nms_radius": 3,
            "max_keypoints": 1024,
            "keypoint_threshold": 0.005, #0.005–0.2
            "sinkhorn_iterations": 20,
            "match_threshold'": 0.05,   #0.05 (low confidence) - 0.5 (high confidence)
        },
        "preprocessing": {
            "grayscale": True,
            "resize_max": 4000,
        },
    }
}

matcher_conf_list = {
    "superpoint+lightglue": {
        "output": "matches-superpoint-lightglue",
        "model": {
            "name": "lightglue",
            "features": "superpoint",
        },
    },
}

loc_config = {
    "estimation": {
        "ransac": {
            "max_error": 0.5,
            "min_inlier_ratio": 0.07,
        }
    },
    "refinement": {"refine_focal_length": False, "refine_extra_params": False}
}

# Path to the model
model_dir = Path(__file__).resolve().parent / "dataset" / "reticle_model"
reference_img_path = model_dir / "images_name.txt"
if not reference_img_path.exists():
    raise FileNotFoundError(f"Reference image list not found at {reference_img_path}")
references = [line.strip() for line in reference_img_path.read_text().splitlines() if line.strip()]

# feature and matcher configurations
feature_conf = feature_conf_list["superpoint_parallax"]
matcher_conf = matcher_conf_list["superpoint+lightglue"]

# Camera Model
Fx, Fy, Cx, Cy = 15400.0, 15400.0, 2000.0, 1500.0
WIDTH, HEIGHT = 4000, 3000  # or the actual dimensions of your query image
FLIR_CAMERA = pycolmap.Camera(
    model='OPENCV',
    width=WIDTH,
    height=HEIGHT,
    params=[Fx, Fy, Cx, Cy]
)

