from pathlib import Path
from sfm.localization_pipeline import extract_features, match_features_to_ref, localize

TEST = False
images_dir = Path(r"C:\Users\hanna.lee\Documents\00_Parallax\002_TestCode\000_ReticleImages")
#query = "queries/22433200_20250424-153426.png"
#query = "queries_masked/22433200_20250424-153426.png"
query = "mapping/22433200_20250424-134845.png"
export_path = Path(r"C:\Users\hanna.lee\Documents\sfm_output")
#1 0.20920463758524413 0.94466390580817239 -0.11330123184761914 0.22584586677175925 -0.73678254795573261 0.37132402196349584 76.715119333643457 1 mapping/22433200_20250424-134845.png

import argparse

"""
def main(images_dir: Path=images_dir, query: str=query, export_path: Path=export_path, visualize: bool = False):
    print("Sfm localization started...")
    #extract_features(images_dir, query, export_path)
    #match_features_to_ref(query, export_path)
    print("-0.73678254795573261 0.37132402196349584 76.715119333643457")
    result = localize(export_path, query, visualize)
    return result
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    if TEST:
        parser.add_argument("--images_dir", default=images_dir)
        parser.add_argument("--query", default=query)
        parser.add_argument("--export_path", default=export_path)
    else:
        parser.add_argument("--image_path", required=True)
        parser.add_argument("--image_name", required=True)
        parser.add_argument("--export_dir", required=True)

    args = parser.parse_args()

    extract_features(args.image_path, args.image_name, args.export_dir)
    match_features_to_ref(args.image_name, args.export_dir)
    localize(args.export_dir, args.image_name)
