# Adapted from Hierarchical-Localization:
# https://github.com/cvg/Hierarchical-Localization

from collections import defaultdict
from pathlib import Path
from typing import List

import numpy as np
import pycolmap
import logging


from .utils.io import get_keypoints, get_matches
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class QueryLocalizer:
    def __init__(self, reconstruction, config=None):
        self.reconstruction = reconstruction
        self.config = config or {}

    def localize(self, points2D_all, points2D_idxs, points3D_id, query_camera):
        points2D = points2D_all[points2D_idxs]
        points3D = [self.reconstruction.points3D[j].xyz for j in points3D_id]
        if pycolmap.__version__ == "0.6.1":
            ret = pycolmap.absolute_pose_estimation(  #pycolmap 0.6.1
            points2D,
            points3D,
            query_camera,
            estimation_options=self.config.get("estimation", {}),
            refinement_options=self.config.get("refinement", {}),
        )
        else:
            ret = pycolmap.estimate_and_refine_absolute_pose(  #pycolmap 3.11
            points2D,
            points3D,
            query_camera,
            estimation_options=self.config.get("estimation", {}),
            refinement_options=self.config.get("refinement", {}),
        )
        return ret


def pose_from_cluster(
    localizer: QueryLocalizer,
    qname: str,
    query_camera: pycolmap.Camera,
    db_ids: List[int],
    features_path: Path,
    matches_path: Path,
    **kwargs,
):
    kpq = get_keypoints(features_path, qname)
    kpq += 0.5  # COLMAP coordinates

    kp_idx_to_3D = defaultdict(list)
    kp_idx_to_3D_to_db = defaultdict(lambda: defaultdict(list))
    num_matches = 0
    for i, db_id in enumerate(db_ids):
        image = localizer.reconstruction.images[db_id]
        if image.num_points3D == 0:
            logger.debug(f"No 3D points found for {image.name}.")
            continue
        points3D_ids = np.array(
            [p.point3D_id if p.has_point3D() else -1 for p in image.points2D]
        )

        matches, _ = get_matches(matches_path, qname, image.name)
        matches = matches[points3D_ids[matches[:, 1]] != -1]
        num_matches += len(matches)
        for idx, m in matches:
            id_3D = points3D_ids[m]
            kp_idx_to_3D_to_db[idx][id_3D].append(i)
            # avoid duplicate observations
            if id_3D not in kp_idx_to_3D[idx]:
                kp_idx_to_3D[idx].append(id_3D)

    idxs = list(kp_idx_to_3D.keys())
    mkp_idxs = [i for i in idxs for _ in kp_idx_to_3D[i]]
    mp3d_ids = [j for i in idxs for j in kp_idx_to_3D[i]]
    ret = localizer.localize(kpq, mkp_idxs, mp3d_ids, query_camera, **kwargs)
    if ret is not None:
        ret["camera"] = query_camera

    # mostly for logging and post-processing
    mkp_to_3D_to_db = [
        (j, kp_idx_to_3D_to_db[i][j]) for i in idxs for j in kp_idx_to_3D[i]
    ]
    log = {
        "db": db_ids,
        "PnP_ret": ret,
        "keypoints_query": kpq[mkp_idxs],
        "points3D_ids": mp3d_ids,
        "points3D_xyz": None,  # we don't log xyz anymore because of file size
        "num_matches": num_matches,
        "keypoint_index_to_db": (mkp_idxs, mkp_to_3D_to_db),
    }
    return ret, log