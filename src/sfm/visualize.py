import pycolmap
from sfm.utils import viz_3d
import numpy as np

def visualize_query_pose(model, query_path, ret, log, camera):
    inliers = ret.get("inlier_mask") if "inlier_mask" in ret else ret.get("inliers")
    if inliers is None or not np.any(inliers):
        print(f"[WARN] No inliers found for query {query_path}. Skipping visualization.")
        return

    fig = viz_3d.init_figure()
    viz_3d.plot_reconstruction(fig, model, color="rgba(255,0,0,0.5)", name="Reconstructed_model", points_rgb=True)

    pose = pycolmap.Image(cam_from_world=ret["cam_from_world"])
    viz_3d.plot_camera_colmap(fig, pose, camera, color="rgba(0,255,0,0.5)", name=query_path, fill=True)

    inlier_ids = np.array(log["points3D_ids"])[inliers]
    inl_3d = np.array([model.points3D[pid].xyz for pid in inlier_ids])
    viz_3d.plot_points(fig, inl_3d, color="lime", ps=1, name=query_path)

    fig.show()
