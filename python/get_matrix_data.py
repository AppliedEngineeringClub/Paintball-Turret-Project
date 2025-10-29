"""
get_matrix_data.py

Reads a hard‑coded image file (./image/image.png), walks every pixel one‑by‑one,
collects raw RGB bytes in row‑major order, and writes them to a binary file that
C++ can load with a single read(...) into a std::vector<uint8_t>.

Also emits small sidecar files with metadata and a human‑readable CSV snapshot.

No command‑line args and no `if __name__ == "__main__":` guard — the file executes
on import/run exactly as requested.
"""

# Standard library imports
from pathlib import Path  # file paths (portable across OSes)
import json               # write small metadata sidecar
import csv                # optional human‑readable dump

# Third‑party import (Pillow) for image I/O
from PIL import Image

# -----------------------------
# Hard‑coded I/O locations
# -----------------------------
# Input image path (relative to repo root). You can change this to match your repo.
IN_PATH = Path("image/image.png")

# Output directory where all derived files are written.
OUT_DIR = Path("image/out")

# Derived outputs (created inside OUT_DIR). We keep names stable so C++ can look them up.
BIN_PATH  = OUT_DIR / "pythonoutput.bin"     # raw RGB bytes: width*height*3 bytes
META_PATH = OUT_DIR / "meta.json"            # JSON with width/height/channels/format
CSV_PATH  = OUT_DIR / "matrix_preview.csv"   # small CSV preview (truncated for huge imgs)

# -----------------------------
# Helper: ensure output directory exists
# -----------------------------
OUT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Load the image (fail early with a clear message)
# -----------------------------
if not IN_PATH.exists():
    raise FileNotFoundError(f"Input image not found at: {IN_PATH.resolve()}")

img = Image.open(IN_PATH)
img = img.convert("RGB")
width, height = img.size
CHANNELS = 3

# -----------------------------
# Walk every pixel in row‑major order and collect raw bytes
# -----------------------------
a = bytearray()
px = img.load()

for y in range(height):
    for x in range(width):
        r, g, b = px[x, y]
        a.append(r & 0xFF)
        a.append(g & 0xFF)
        a.append(b & 0xFF)

# -----------------------------
# Write raw bytes to the .bin file
# -----------------------------
with open(BIN_PATH, "wb") as f:
    f.write(a)

# -----------------------------
# Write metadata sidecar (JSON)
# -----------------------------
meta = {
    "width": width,
    "height": height,
    "channels": CHANNELS,
    "layout": "row-major RGB",
    "pixel_order": "R,G,B",
    "source": str(IN_PATH),
    "bytes": len(a),
}

with open(META_PATH, "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2)

# -----------------------------
# Optional: write a small CSV preview for humans
# -----------------------------
MAX_PREVIEW_W = 64
MAX_PREVIEW_H = 64

preview_w = min(width, MAX_PREVIEW_W)
preview_h = min(height, MAX_PREVIEW_H)

with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["x", "y", "R", "G", "B"])

    for y in range(preview_h):
        for x in range(preview_w):
            r, g, b = px[x, y]
            writer.writerow([x, y, r, g, b])

# -----------------------------
# Console summary
# -----------------------------
print("get_matrix_data.py: done")
print(f"  input : {IN_PATH}")
print(f"  size  : {width} x {height} x {CHANNELS} (W x H x C)")
print(f"  wrote : {BIN_PATH}  ({len(a)} bytes)")
print(f"  meta  : {META_PATH}")
print(f"  csv   : {CSV_PATH}  (preview up to {preview_w}x{preview_h})")
