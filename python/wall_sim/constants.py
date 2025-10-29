import sys
import math
sys.path.append("..")
from pymathlib import util
import colors
sys.path.remove("..")

CANVAS_WIDTH = 1200 # pixels
CANVAS_HEIGHT = 1000 # pixesl

util.width = CANVAS_WIDTH
util.height = CANVAS_HEIGHT

WALL_WIDTH = 2 # meters
WALL_HEIGHT = 2 # meters

PAINTBALL_RADIUS = 0.017272 # meters
PAINTBALL_SPLATTER_RADIUS = 0.02 # meters

VIEW_DISTANCE = 3 # meters
WALL_DISTANCE = 5 # meters

H_FOV = 75 * (math.pi / 180) # radians

METERS_PER_PIXEL = 2 * (WALL_DISTANCE - VIEW_DISTANCE) * math.tan(H_FOV / 2) / CANVAS_WIDTH
PIXELS_PER_METER = 1 / METERS_PER_PIXEL

V_FOV = 2 * math.atan((CANVAS_HEIGHT * METERS_PER_PIXEL / (2 * (WALL_DISTANCE - VIEW_DISTANCE)))) # radians

BACKGROUND_COLOR = colors.BLACK
WALL_COLOR = colors.WHITE