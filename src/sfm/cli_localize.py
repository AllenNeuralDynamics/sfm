import pycolmap
from sfm.visualize import visualize_query_pose
from sfm.localize_sfm import QueryLocalizer, pose_from_cluster
from sfm.config import model_dir, references, FLIR_CAMERA, loc_config
from pathlib import Path
import argparse
import json

def localize(export_dir: str, query: str, visualize: bool=False) -> None:
    """Run localization only."""
    model = pycolmap.Reconstruction(model_dir)
    localizer = QueryLocalizer(model, loc_config)
    export_path = Path(export_dir)
    ref_ids = [model.find_image_with_name(r).image_id for r in references]
    ret, log = pose_from_cluster(
        localizer=localizer,
        qname=query,
        query_camera=FLIR_CAMERA,
        db_ids=ref_ids,
        features_path=export_path / "features.h5",
        matches_path=export_path / "matches.h5"
    )

    if ret is not None:
        n_in = ret["num_inliers"]
        pose = ret["cam_from_world"].todict()
        quat = pose['rotation']['quat']
        tvec = pose['translation']
        print(quat[0], quat[1], quat[2], quat[3], tvec[0], tvec[1], tvec[2])

    if visualize and ret is not None:
        visualize_query_pose(model, query, ret, log, FLIR_CAMERA)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--export_dir", required=True)
    parser.add_argument("--visualize", action='store_true', help="Visualize the localization result")

    args = parser.parse_args()
    localize(args.export_dir, args.query, visualize=args.visualize)
