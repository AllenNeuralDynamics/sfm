import subprocess
from pathlib import Path
import sys
import argparse


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
        "--export_dir", export_dir,
        "--visualize"
    ], check=True, capture_output=True, text=True)

    if result.returncode != 0:
        print("Localization failed with error:")
        print(result.stderr)
        return None
    
    return result.stdout

def main():
    parser = argparse.ArgumentParser(description="Run the SFM pipeline steps.")
    parser.add_argument("--image_dir", required=True, help="Path to the directory containing the image.")
    parser.add_argument("--query", required=True, help="Query image filename.")
    parser.add_argument("--export_dir", required=True, help="Path to the output directory.")

    args = parser.parse_args()

    print("Running feature extraction...")
    run_feature_cli(args.image_dir, args.query, args.export_dir)

    print("Running matching...")
    run_match_cli(args.query, args.export_dir)

    print("Running localization...")
    result = run_localize_cli(args.query, args.export_dir)
    
    if result is not None:
        print("Localization result:")
        print(result)

if __name__ == "__main__":
    main()