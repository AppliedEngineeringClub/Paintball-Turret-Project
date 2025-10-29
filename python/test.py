# Standard library imports
from pathlib import Path  # file paths (portable across OSes)
import json               # write small metadata sidecar
import csv                # optional human‑readable dump
import os                 # os seek
import numpy as np

print("---")

OUT_PATH = Path("image/out")
BIN_PATH = OUT_PATH / "pythonoutput.bin"
META_PATH = OUT_PATH / "meta.json"

with open(META_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
    width = data['width']
    height = data['height']
    num_pixels = width * height
    channels = data['channels']
    bytes = data['bytes']

    print(f"Width: {width}")
    print(f"Height: {height}")

print(f"Creating {width} x {height} x {channels} matrix...")
matrix = np.empty((width, height, channels))

with open(BIN_PATH, "rb") as f:

    # f.seek(0, os.SEEK_END)
    # num_bytes = f.tell()
    # num_pixels = round(num_bytes / 3)
    # f.seek(0, os.SEEK_SET)

    # print(f"Reading {num_bytes} bytes and {num_pixels} pixels")

    rgb = f.read(bytes)

    len(rgb)

    for w in range(width):
        for h in range(height):
            ith_pixel = (w + 1) * (h + 1)

            print(f"Reading {ith_pixel} pixel...")

            r = rgb[(3 * ith_pixel) + 0]
            g = rgb[(3 * ith_pixel) + 1]
            b = rgb[(3 * ith_pixel) + 2]


    for i in range(num_pixels):
        print(f"Reading {i + 1} pixel...")
        r = rgb[(3 * i) + 0]
        g = rgb[(3 * i) + 1]
        b = rgb[(3 * i) + 2]

        matrix[0][0]

        # print(f"Red:\t{r}")
        # print(f"Green:\t{g}")
        # print(f"Blue:\t{b}")

    print(bytes)

print("---")