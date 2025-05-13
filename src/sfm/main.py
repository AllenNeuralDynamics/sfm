import pycolmap
import time
from sfm.visualize import visualize_query_pose
from sfm.extract_features import main as extract_features_main
from sfm.match_features import main as match_features
from sfm.pairs_from_exhaustive import pairs_from_exhaustive
from sfm.localize_sfm import QueryLocalizer, pose_from_cluster
from sfm.config import model_dir, references, FLIR_CAMERA, feature_conf, matcher_conf
from pathlib import Path

images_dir = Path(r"C:\Users\hanna.lee\Documents\00_Parallax\002_TestCode\000_ReticleImages")
query = "queries/Microscope_3_20250403-094514.png"
export_path = Path(r"C:\Users\hanna.lee\Documents\sfm_output")


def main(export_path: Path=export_path, query: str=query, visualize: bool=True) -> dict:
    print("Sfm localization started...")

    # Reconstruct
    model = pycolmap.Reconstruction(model_dir)

    # Feature extraction
    start = time.time()
    print("\nExtracting features...")
    extract_features_main(
        conf=feature_conf,
        image_dir=images_dir,
        image=query,
        export_path=export_path / "features.h5"
    )
    print(f"Feature extraction time: {time.time() - start} sec")
    
    # Matching
    start = time.time()
    print("\nMatching features...")
    pairs_from_exhaustive(
        output=export_path / "pairs-loc.txt",
        image = query,
        ref_list=references
    )
    match_features(
        conf=matcher_conf,
        pairs=export_path / "pairs-loc.txt",
        features=export_path / "features.h5",
        matches=export_path / "matches.h5",
        features_ref = model_dir / "features.h5",
        overwrite=True
    )
    print(f"Match generation time: {time.time() - start} sec")

    # Localize
    start = time.time()
    print("\nLocalizing...")
    localizer = QueryLocalizer(model, {
        "estimation": {"ransac": {"max_error": 20}},
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
    print(f"Localization time: {time.time() - start} sec")

    if visualize:
        visualize_query_pose(model, query, ret, log, FLIR_CAMERA)
    
        
    if "cam_from_world" in ret and "num_inliers" in ret:
        print(ret["cam_from_world"])
        print("num_inliers: ", ret["num_inliers"])
        return ret["cam_from_world"]

    return {}

if __name__ == "__main__":
    main()
