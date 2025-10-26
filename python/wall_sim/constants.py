import sys
import math
sys.path.append("..")
from pymathlib import util
import colors
sys.path.remove("..")

CANVAS_WIDTH = 800 # pixels
CANVAS_HEIGHT = 600 # pixesl

util.width = CANVAS_WIDTH
util.height = CANVAS_HEIGHT

WALL_WIDTH = 2 # meters
WALL_HEIGHT = 2 # meters

PAINTBALL_RADIUS = 0.017272 # meters
PAINTBALL_SPLATTER_RADIUS = 0.02 # meters

WALL_DISTANCE = 5 # meters

BACKGROUND_COLOR = colors.BLACK
WALL_COLOR = colors.WHITE