# Standard library imports
from pathlib import Path  # file paths (portable across OSes)
import json               # write small metadata sidecar
import csv                # optional human‑readable dump
import os                 # os seek
import numpy as np
import time

# Program Start
print("---")

OUT_PATH = Path("image/out")
BIN_PATH = OUT_PATH / "pythonoutput.bin"
META_PATH = OUT_PATH / "meta.json"

start = time.perf_counter()

with open(META_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
    width = data['width']
    height = data['height']
    num_pixels = width * height
    channels = data['channels']
    bytes = data['bytes']

    print(f"Width: {width}")
    print(f"Height: {height}")
    print(f"Pixels: {num_pixels}")

print(f"Creating {width} x {height} x {channels} matrix...", end="")
matrix = np.empty((width, height, channels))
print("done")

with open(BIN_PATH, "rb") as f:

    # f.seek(0, os.SEEK_END)
    # num_bytes = f.tell()
    # num_pixels = round(num_bytes / 3)
    # f.seek(0, os.SEEK_SET)

    # print(f"Reading {num_bytes} bytes and {num_pixels} pixels")

    print(f"Reading {bytes} bytes...", end="")
    rgb = f.read(bytes)
    print("done")

    for w in range(width):
        for h in range(height):
            ith_pixel = (w * height) + h

            r = rgb[(3 * ith_pixel) + 0]
            g = rgb[(3 * ith_pixel) + 1]
            b = rgb[(3 * ith_pixel) + 2]

            matrix[w][h][0] = r
            matrix[w][h][1] = g
            matrix[w][h][2] = b

    print(f"Matrix Reconstruction took {time.perf_counter() - start:.4f} seconds")

# Program End
print("---")