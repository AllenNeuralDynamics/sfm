from .config import model_dir, references, FLIR_CAMERA, feature_conf, matcher_conf
from sfm.reconstruct import reconstruct, visualize_query_pose
from sfm.extract_features import main as extract_features_main
from sfm.match_features import main as match_features
from sfm.pairs_from_exhaustive import pairs_from_exhaustive
from sfm.localize_sfm import QueryLocalizer, pose_from_cluster
from pathlib import Path
from sfm.utils import viz_3d
import cv2

images_dir = Path(r"C:\Users\hanna.lee\Documents\00_Parallax\002_TestCode\000_ReticleImages")
query = "queries/Microscope_3_20250403-094514.png"
export_path = Path(r"C:\Users\hanna.lee\Documents\sfm_output")

import pycolmap
print(pycolmap.__version__)
def main() -> None:
    # Reconstruct
    model = reconstruct(model_dir)
    fig = viz_3d.init_figure()
    viz_3d.plot_reconstruction(
        fig, model, color="rgba(255,0,0,0.5)", name="final_model", points_rgb=True
    )
    fig.show()
    
    
    # Feature extraction
    extract_features_main(
        conf=feature_conf,
        image_dir=images_dir,
        image=query,
        export_path=export_path / "features.h5"
    )
    
    # Matching
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
    #print("ret", ret)
    #print("log", log)
    visualize_query_pose(model, query, ret, log, FLIR_CAMERA, fig=fig)
    fig.show()

if __name__ == "__main__":
    main()
