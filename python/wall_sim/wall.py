# Standard library imports
from pathlib import Path  # file paths (portable across OSes)
import json               # write small metadata sidecar
import csv                # optional human‑readable dump
import os                 # os seek
import numpy as np
import time

import pygame             # for wall rendering
import sys                # import handling
from wall_sim.constants import *
from typing import Tuple

sys.path.append("..")
from pymathlib import util
import colors
sys.path.remove("..")

class Wall:

    
    def __init__(self, wall_dimensions: Tuple[float, float], canvas_dimensions: Tuple[int, int], distance: float, wall_color = colors.WHITE):
        """
        Creates a Wall object to represent the wall to be painted

        Args:
            wall_dimensions: The width and height of the wall in meters -> Tuple[float, float]
            canvas_dimensions: The width and height of the canvas in pixels -> Tuple[int, int]
            distance: The distance of the center of the wall to the "camera" in meters -> float
            wall_color: color to paint the wall in RGB -> Tuple[int, int, int]
        """
        self.wall_width = wall_dimensions[0]
        self.wall_height = wall_dimensions[1]

        self.canvas_width = canvas_dimensions[0]
        self.canvas_height = canvas_dimensions[1]

        self.distance = distance

        self.wall_color = wall_color
    
    def draw_wall(self, screen):
        width = PIXELS_PER_METER * self.wall_width
        height = PIXELS_PER_METER * self.wall_height

        center = util.cartesian_to_native(0, 0)

        pygame.draw.rect(screen, self.wall_color, (center[0] - width / 2, center[1] - height / 2, width, height))

    def draw_paintball(self, screen, position: Tuple[int, int], color: Tuple[int, int, int]):
        radius_pixels = PAINTBALL_SPLATTER_RADIUS * PIXELS_PER_METER

        native = util.cartesian_to_native(position[0], position[1])

        pygame.draw.circle(screen, color, native, radius_pixels)
