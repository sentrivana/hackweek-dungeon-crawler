import random

import pygame

from game.consts import (
    TILE_COLS,
    TILE_ROWS,
    TILE_SIZE_PIXELS,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)


class HUDOverlay:
    FONT_SIZE = 24

    def __init__(self, level):
        self.level = level

    @property
    def should_blink(self):
        return self.level.player.health <= 1

    def render(self, screen):
        font = pygame.font.SysFont("monaco", self.FONT_SIZE)
        if self.level.player.health > 1:
            color = (242, 211, 171)
        else:
            color = (200, 0, 0)
        font_surface = font.render(
            f"Energy left: {self.level.player.health}", False, color
        )

        screen.blit(font_surface, (10, 10))


class TextOverlay:
    FONT_SIZE = 16

    def __init__(self, color=None):
        self.color = color or "white"

    @property
    def width(self):
        return WINDOW_WIDTH - WINDOW_WIDTH // 2

    def set_text(self, text, small_text=None, color=None):
        self.text = text
        self.small_text = small_text
        self.color = color or "white"

    def dismiss(self):
        self.text = None
        self.small_text = None
        self.color = "white"

    def render(self, screen):
        font = pygame.font.SysFont("monaco", self.FONT_SIZE)

        font_surfaces = []
        for line in self.text.split("\n"):
            surface = font.render(line, False, self.color)
            font_surfaces.append(
                (
                    surface,
                    (
                        self.FONT_SIZE,
                        self.FONT_SIZE
                        + (self.FONT_SIZE // 2) * len(font_surfaces)
                        + self.FONT_SIZE * len(font_surfaces),
                    ),
                )
            )

        if self.small_text is not None:
            small_font_size = self.FONT_SIZE - self.FONT_SIZE // 4
            font = pygame.font.SysFont("monaco", small_font_size)
            surface = font.render(self.small_text, False, "white")
            font_surfaces.append(
                (
                    surface,
                    (
                        self.FONT_SIZE,
                        self.FONT_SIZE * 2
                        + (self.FONT_SIZE // 2) * len(font_surfaces)
                        + self.FONT_SIZE * len(font_surfaces),
                    ),
                )
            )

        overlay = pygame.Surface(
            (self.width, font_surfaces[-1][1][1] + 2 * self.FONT_SIZE)
        )
        overlay.blits(font_surfaces)

        screen.blit(
            overlay,
            (
                (WINDOW_WIDTH - self.width) // 2,
                (WINDOW_HEIGHT - overlay.get_height()) // 2,
            ),
        )


class TorchlightOverlay:
    def __init__(self):
        self.generate()

    def generate(self):
        # XXX make this better
        overlays = []

        max_dist = TILE_ROWS // 2
        for r in range(TILE_ROWS):
            for c in range(TILE_COLS):
                dist_to_center = max(abs(r - TILE_ROWS // 2), abs(c - TILE_COLS // 2))
                surface = pygame.Surface((TILE_SIZE_PIXELS, TILE_SIZE_PIXELS))
                degree = 255 // max_dist
                surface.set_alpha(degree * dist_to_center + random.randint(-10, 10))
                overlays.append(
                    (
                        surface,
                        (c * TILE_SIZE_PIXELS, r * TILE_SIZE_PIXELS),
                    )
                )

        self.overlays = overlays

    def render(self, screen):
        screen.blits(self.overlays)
