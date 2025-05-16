from pathlib import Path
from sfm.localization_pipeline import extract_features, match_features_to_ref, localize
images_dir = Path(r"C:\Users\hanna.lee\Documents\00_Parallax\002_TestCode\000_ReticleImages")
query = "queries/22433200_20250424-153426.png"
export_path = Path(r"C:\Users\hanna.lee\Documents\sfm_output")

def main(images_dir: Path=images_dir, query: str=query, export_path: Path=export_path, visualize: bool = False):
    print("Sfm localization started...")
    #extract_and_match_features(images_dir, query, export_path)

    extract_features(images_dir, query, export_path)
    match_features_to_ref(query, export_path)
    result = localize(export_path, query, visualize)
    return result

if __name__ == "__main__":
    main()
