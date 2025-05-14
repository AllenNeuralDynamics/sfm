import pycolmap
import time
from sfm.visualize import visualize_query_pose
from sfm.extract_features import main as extract_features_main
from sfm.match_features import main as match_features
from sfm.pairs_from_exhaustive import pairs_from_exhaustive
from sfm.localize_sfm import QueryLocalizer, pose_from_cluster
from sfm.config import model_dir, references, FLIR_CAMERA, feature_conf, matcher_conf
from pathlib import Path
from typing import Optional
images_dir = Path(r"C:\Users\hanna.lee\Documents\00_Parallax\002_TestCode\000_ReticleImages")
query = "queries/22433200_20250424-153426.png"
export_path = Path(r"C:\Users\hanna.lee\Documents\sfm_output")

def extract_and_match_features(images_dir: Path, query: str, export_path: Path):
    """Extract and match features."""
    print("\nExtracting features...")
    start = time.time()
    extract_features_main(
        conf=feature_conf,
        image_dir=images_dir,
        image=query,
        export_path=export_path / "features.h5"
    )
    print(f"Feature extraction time: {time.time() - start} sec")    
    
    print("\nGenerating pairs and matching...")
    start = time.time()
    pairs_from_exhaustive(
        output=export_path / "pairs-loc.txt",
        image=query,
        ref_list=references
    )
    match_features(
        conf=matcher_conf,
        pairs=export_path / "pairs-loc.txt",
        features=export_path / "features.h5",
        matches=export_path / "matches.h5",
        features_ref=model_dir / "features.h5",
        overwrite=True
    )
    print(f"Match generation time: {time.time() - start} sec")

def localize(export_path: Path, visualize: bool = False) -> Optional[dict]:
    """Run localization only."""
    print("\nStarting localization...")

    model = pycolmap.Reconstruction(model_dir)
    localizer = QueryLocalizer(model, {
        "estimation": {
            "ransac": {
                "max_error": 2.0,
                "min_inlier_ratio": 0.2
            }
        },
        "refinement": {"refine_focal_length": False, "refine_extra_params": False}
    })
    
    ref_ids = [model.find_image_with_name(r).image_id for r in references]
    ret, log = pose_from_cluster(
        localizer=localizer,
        qname=query,
        query_camera=FLIR_CAMERA,
        db_ids=ref_ids,
        features_path=export_path / "features.h5",
        matches_path=export_path / "matches.h5"
    )

    if visualize and ret is not None:
        visualize_query_pose(model, query, ret, log, FLIR_CAMERA)

    if ret is not None:
        print("num_inliers:", ret["num_inliers"])
        print("camera:", ret["camera"])
        print("cam_from_world:", ret["cam_from_world"].todict())
        return ret["cam_from_world"].todict()

    return None


def main(images_dir: Path=images_dir, query: str=query, export_path: Path=export_path, visualize: bool = False):
    print("Sfm localization started...")
    extract_and_match_features(images_dir, query, export_path)
    result = localize(export_path, visualize)
    return result

if __name__ == "__main__":
    main()
