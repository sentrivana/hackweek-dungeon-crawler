import logging
import math

import random

import pygame

from game.consts import WINDOW_HEIGHT, WINDOW_WIDTH
from game.events import CustomEvent
from game.utils import post_event


logger = logging.getLogger(__name__)


class Minigame:
    PADDING = 5
    MAX_JITTER = 30

    def __init__(self, enemy, difficulty):
        self.enemy = enemy
        self.difficulty = difficulty

        self.started = False
        self.jitters = 0

        self.surface_with_padding = pygame.surface.Surface((self.width, self.height))
        self.surface_with_padding.fill("white")

        self.surface = self.surface_with_padding.subsurface(
            self.PADDING,
            self.PADDING,
            self.surface_with_padding.get_width() - self.PADDING * 2,
            self.surface_with_padding.get_height() - self.PADDING * 2,
        )

        logger.debug("Minigame for enemy %s at %d %d created", enemy.type, *enemy.pos)

    @property
    def width(self):
        return WINDOW_WIDTH // 4

    @property
    def height(self):
        return WINDOW_HEIGHT // 4

    @property
    def color1(self):
        return (39, 39, 68)

    @property
    def color2(self):
        return (139, 109, 156)

    @property
    def bg(self):
        return (242, 211, 171)

    def start(self):
        self.started = True
        logger.debug("Minigame started")

    def render(self, screen, dt):
        self.surface.fill(self.bg)
        self._render(dt)
        left = (WINDOW_WIDTH - self.width) // 2
        top = (WINDOW_HEIGHT - self.height) // 2
        if self.jitters > 0:
            top += random.randint(-self.MAX_JITTER, self.MAX_JITTER)
            left += random.randint(-self.MAX_JITTER, self.MAX_JITTER)
            self.jitters -= 1

        screen.blit(self.surface_with_padding, (left, top))

    def input(self):
        raise NotImplementedError


class PrecisionMinigame(Minigame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pos = 0
        self.surface_width = self.surface.get_width()
        self.target_width = math.ceil(self.surface_width / 100 * self.difficulty)

    def _render(self, dt):
        pygame.draw.rect(
            self.surface,
            self.color2,
            (
                (self.surface_width - self.target_width) // 2,
                0,
                self.target_width,
                self.surface.get_height(),
            ),
        )
        pygame.draw.rect(
            self.surface, self.color1, (self.pos, 0, 3, self.surface.get_height())
        )

        self.pos = (self.pos + 2) % self.surface_width

    def input(self):
        if (
            (self.surface_width - self.target_width) // 2
            <= self.pos
            <= (self.surface_width - self.target_width) // 2 + self.target_width
        ):
            post_event(
                CustomEvent.ENEMY_DEFEATED, row=self.enemy.row, col=self.enemy.col
            )
        else:
            post_event(CustomEvent.DAMAGE_RECEIVED)


MINIGAMES = [PrecisionMinigame]
