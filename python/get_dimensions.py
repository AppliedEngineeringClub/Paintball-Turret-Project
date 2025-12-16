#!/usr/bin/env python3
"""
Loads the image at hard-coded path 'image/image.png',
then writes its width and height in pixels to the file
'pythonoutput.txt' (so the C++ code can read from it).
"""

from PIL import Image  # Requires Pillow library
from pathlib import Path
import sys

# Resolve repo root relative to this script so it works regardless of CWD
ROOT = Path(__file__).resolve().parents[1]
image_path = ROOT / "image" / "image.png"

try:
    img = Image.open(image_path)
    width, height = img.size  # width = number of columns, height = number of rows
except Exception as e:
    print(f"Error opening image '{image_path}': {e}", file=sys.stderr)
    sys.exit(1)

# Write the dimensions to repo-root file (read by C++)
out_path = ROOT / "pythonoutput.txt"
with open(out_path, "w") as f:
    f.write(f"{width} {height}")
