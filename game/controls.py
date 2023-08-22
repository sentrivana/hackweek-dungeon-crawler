from enum import Enum

import pygame


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


MOVEMENT_CONTROLS = {
    pygame.K_w: Direction.UP,
    pygame.K_UP: Direction.UP,
    pygame.K_s: Direction.DOWN,
    pygame.K_DOWN: Direction.DOWN,
    pygame.K_a: Direction.LEFT,
    pygame.K_LEFT: Direction.LEFT,
    pygame.K_d: Direction.RIGHT,
    pygame.K_RIGHT: Direction.RIGHT,
}

OTHER_CONTROLS = {
    pygame.K_RETURN: "",  # XXX
}

CONTROLS = MOVEMENT_CONTROLS | OTHER_CONTROLS
