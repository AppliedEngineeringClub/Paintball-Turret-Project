import pygame
import sys
import math

from typing import Tuple
sys.path.append("..")
from pymathlib import util
import colors
sys.path.remove("..")

H_FOV = 75 * (math.pi / 180) # radians
V_FOV = 60 * (math.pi / 180) # radians

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
        
        self.distance_of_max_view = 0.0

        if self.wall_width > self.wall_height:
            self.distance_of_max_view = math.tan(H_FOV) * self.wall_width
        else:
            self.distance_of_max_view = math.tan(V_FOV) * self.wall_height

        self.meters_per_pixel = (self.distance_of_max_view / self.distance) * (self.wall_width / self.canvas_width)

        print(self.meters_per_pixel)
        print((self.distance_of_max_view / self.distance) * (self.wall_height / self.canvas_height))


        # https://www.desmos.com/calculator/ehsfov4mqa

    def get_scale_ratio(self):
        return (self.distance_of_max_view / self.distance)

    def draw_wall(self, screen):
        width = (self.distance_of_max_view / self.distance) * self.wall_width
        height = (self.distance_of_max_view / self.distance) * self.canvas_height

        center = util.cartesian_to_native(0, 0)

        pygame.draw.rect(screen, self.wall_color, (center[0] - width / 2, center[1] - height / 2, width, height))

    def draw_paintball(self, screen, position: Tuple[int, int], color: Tuple[int, int, int]):
        radius_pixels = 0.02 * (1 / self.meters_per_pixel)

        native = util.cartesian_to_native(position[0], position[1])

        pygame.draw.circle(screen, color, native, radius_pixels)
