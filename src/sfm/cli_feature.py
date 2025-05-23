from sfm.extract_features import main as extract_features_main
from sfm.config import feature_conf
from pathlib import Path
import argparse

def extract_features(image_dir: str, query: str, export_dir: str):
    """Extract features for a query image."""
    image_path = Path(image_dir)
    export_path = Path(export_dir)
    extract_features_main(
        conf=feature_conf,
        image_dir=image_path,
        image=query,
        export_path=export_path / "features.h5"
    )
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_dir", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--export_dir", required=True)

    args = parser.parse_args()
    extract_features(args.image_dir, args.query, args.export_dir)