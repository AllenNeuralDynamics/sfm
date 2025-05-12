from pathlib import Path
from typing import List

def pairs_from_exhaustive(output: Path, image: str, ref_list: List[str]) -> None:
    """Write pairings of a single image to all references."""
    with open(output, "w") as f:
        for ref in ref_list:
            f.write(f"{image} {ref}\n")