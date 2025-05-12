import pycolmap
from sfm.utils import viz_3d
import numpy as np

def reconstruct(model_path, visualize=False):
    model = pycolmap.Reconstruction(model_path)
    if visualize:
        fig = viz_3d.init_figure()
        viz_3d.plot_reconstruction(
            fig, model, color="rgba(255,0,0,0.5)", name="Reconstructed_model", points_rgb=True
        )
        fig.show()
    return model

def visualize_query_pose(model, query_path, ret, log, camera, fig=None):
    print(f"Model has {len(model.points3D)} 3D points.")
    # Normalize access to inliers / inlier_mask across versions
    inliers = None
    if "inlier_mask" in ret:
        # pycolmap 3.11.0 provides a boolean mask
        inliers = ret["inlier_mask"]
    elif "inliers" in ret:
        # pycolmap 0.6.1 provides an index array or mask
        inliers = ret["inliers"]

    # Check if there are any valid inliers
    if inliers is None or not inliers.any():
        print(f"[WARN] No inliers found for query {query_path}. Skipping visualization.")
        return fig

    #visualization.visualize_loc_from_log(self.image_dir, query_path, log, self.model)
    
    if fig is None:
        fig = viz_3d.init_figure()
    pose = pycolmap.Image(cam_from_world=ret["cam_from_world"])
    
    viz_3d.plot_camera_colmap(
        fig, pose, camera, color="rgba(0,255,0,0.5)", name=query_path, fill=True
    )
    if "inliers" in ret:
        inlier_ids = np.array(log["points3D_ids"])[ret["inliers"]]
    elif "inlier_mask" in ret:
        inlier_ids = np.array(log["points3D_ids"])[ret["inlier_mask"]]
    else:
        inlier_ids = []

    inl_3d = np.array([model.points3D[pid].xyz for pid in inlier_ids])

    viz_3d.plot_points(fig, inl_3d, color="lime", ps=1, name=query_path)

def visualize_query_pose_(model, query, ret, log, camera, fig=None):
    print(f"Model has {len(model.points3D)} 3D points.")
    inliers = ret.get("inliers") or np.where(ret.get("inlier_mask", []))[0]
    inlier_ids = np.array(log["points3D_ids"])[inliers]
    #print("Inlier IDs:", inlier_ids)
    #print("Available IDs in model:", list(model.points3D.keys()))



    # Ensure inliers exist
    
    if len(inliers) == 0:
        print(f"[WARN] No inliers found for {query}. Skipping visualization.")
        return fig

    # Collect valid 3D points
    points3D_xyz = [model.points3D[pid].xyz for pid in np.array(log["points3D_ids"])[inliers] if pid in model.points3D]
    if not points3D_xyz:
        print(f"[WARN] No valid 3D points for {query}. Skipping visualization.")
        return fig

    # Initialize figure if not provided
    if fig is None:
        fig = viz_3d.init_figure()

    # Plot 3D points
    fig = viz_3d.plot_xyz(fig, np.array(points3D_xyz), color="red", name=query)

    # Plot camera pose
    fig = viz_3d.plot_camera_colmap(fig, ret["cam_from_world"], camera, name=query + "_pose")

    print(f"[INFO] Visualized {len(points3D_xyz)} points and camera pose for {query}.")
    return fig
