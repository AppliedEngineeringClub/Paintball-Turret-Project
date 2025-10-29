import pygame
from pymathlib import util
from wall_sim.wall import Wall
from wall_sim.constants import *
import colors

screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
pygame.display.set_caption("Wall Simulation")

wall = Wall((WALL_WIDTH, WALL_HEIGHT), (CANVAS_WIDTH, CANVAS_HEIGHT), WALL_DISTANCE)

keep_alive = True
clock = pygame.time.Clock()

while keep_alive:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_alive = False

    screen.fill(BACKGROUND_COLOR)
    
    wall.draw_wall(screen)

    wall.draw_paintball(screen, (0, 0), colors.BLUE)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()