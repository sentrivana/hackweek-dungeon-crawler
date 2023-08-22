import enum
import logging
import random
import sys

import pygame

from game.consts import (
    GAME_TITLE,
    TILE_COLS,
    TILE_ROWS,
    TILE_SIZE_PIXELS,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from game.controls import MOVEMENT_CONTROLS
from game.events import EVENT_GENERATE_OVERLAY
from game.level.level import Level


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


class State(enum.Enum):
    RUNNING = 0
    OVERLAY = 1
    STOPPED = 2


def run():
    pygame.init()

    logger.debug("Setting window size to %d x %d", WINDOW_WIDTH, WINDOW_HEIGHT)

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()
    state = State.RUNNING
    darkness_overlay = get_darkness_overlay()

    level = Level("levels/001.map")

    pygame.time.set_timer(pygame.event.Event(EVENT_GENERATE_OVERLAY), 800)

    while state != State.STOPPED:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = state.STOPPED

            if state == State.RUNNING:
                if event.type == pygame.KEYDOWN:
                    if event.key in MOVEMENT_CONTROLS:
                        level.handle_movement(MOVEMENT_CONTROLS[event.key])
                elif event.type == EVENT_GENERATE_OVERLAY:
                    darkness_overlay = get_darkness_overlay()

            elif state == State.OVERLAY:
                pass

        screen.fill((0, 0, 0))

        level.render(screen)

        screen.blits(darkness_overlay)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


def get_darkness_overlay():
    # XXX make this better and move it someplace else
    overlays = []

    max_dist = TILE_ROWS // 2
    for r in range(TILE_ROWS):
        for c in range(TILE_COLS):
            dist_to_center = max(abs(r - TILE_ROWS // 2), abs(c - TILE_COLS // 2))
            surface = pygame.Surface((TILE_SIZE_PIXELS, TILE_SIZE_PIXELS))
            degree = 255 // max_dist
            # XXX
            surface.set_alpha(degree * dist_to_center + random.randint(-10, 10))
            overlays.append(
                (
                    surface,
                    (c * TILE_SIZE_PIXELS, r * TILE_SIZE_PIXELS),
                )
            )

    return overlays
