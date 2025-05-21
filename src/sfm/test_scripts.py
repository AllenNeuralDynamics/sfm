import subprocess
from pathlib import Path
import sys
#from sfm.localization_pipeline import match_features_to_ref
from sfm.cli_localize import localize
print("Start")
image_dir=r"C:\Users\hanna.lee\Documents\00_Parallax\002_TestCode\000_ReticleImages\test"
query="22433200_20250424-134845.png"
export_dir=r"C:\Users\hanna.lee\Documents\sfm_output"

def run_feature_cli(image_dir, image_name, export_dir):
    subprocess.run([
        sys.executable,
        str(Path(__file__).parent / "cli_feature.py"),
        "--image_dir", image_dir,
        "--query", image_name,
        "--export_dir", export_dir
    ], check=True)
  
def run_match_cli(image_name, export_dir):
    subprocess.run([
        sys.executable,
        str(Path(__file__).parent / "cli_match.py"),
        "--query", image_name,
        "--export_dir", export_dir
    ], check=True)

def run_localize_cli(image_name, export_dir):
    result = subprocess.run([
        sys.executable,
        str(Path(__file__).parent / "cli_localize.py"),
        "--query", image_name,
        "--export_dir", export_dir
    ], check=True, capture_output=True, text=True)
    #  option: "--visualize"

    if result.returncode != 0:
        print("Localization failed with error:")
        print(result.stderr)
        return None
    
    return result.stdout

print("Running feature extraction...")
run_feature_cli(image_dir, query, export_dir)

print("Running matching...")
run_match_cli(query, export_dir)

print("Running localization...")
result = run_localize_cli(query, export_dir)
if result is not None:
    print(result)
