from pathlib import Path
import pycolmap

feature_conf_list = {
    "superpoint_parallax": {
        "output": "feats-superpoint-n1024-r4000",
        "model": {
            "name": "superpoint",
            "nms_radius": 3,
            "max_keypoints": 2048,
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


# Path to the model
model_dir = Path(__file__).resolve().parent.parent.parent / "dataset" / "reticle_model"

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

reference_img_path = model_dir / "images_name.txt"
references = [line.strip() for line in reference_img_path.read_text().splitlines() if line.strip()]