
import argparse
from sfm.match_features import main as match_features
from sfm.pairs_from_exhaustive import pairs_from_exhaustive
from sfm.config import model_dir, references, matcher_conf
from pathlib import Path

def match_features_to_ref(query: str, export_dir: str):
    """Generate pairs and match query image features to reference features."""
    print("\nMatching features to reference features...")
    export_path = Path(export_dir)
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--export_dir", required=True)

    args = parser.parse_args()
    match_features_to_ref(args.query, args.export_dir)