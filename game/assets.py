import logging

import pygame

from game.consts import ENTITY_SIZE_PIXELS, TILE_SIZE_PIXELS
from game.level.types import EntityType, TileType

logger = logging.getLogger(__name__)


class Assets:
    """
    Asset manager.

    Tileset from https://opengameart.org/content/dungeon-crawl-32x32-tiles
    """

    # XXX nice paths instead of hardcoded
    FILENAME = "assets/tileset.png"
    MAPPING = {
        "entities": {
            EntityType.PLAYER: [(84, 41)],
            EntityType.LOOT: [(2, 4)],
            EntityType.ENEMY: [(2, 5)],
        },
        "tiles": {
            TileType.GROUND: [(7, 3)],
            TileType.HAZARD: [(2, 7)],
            TileType.WALL: [(7, 21)],
        },
    }
    SIZES = {
        "entities": ENTITY_SIZE_PIXELS,
        "tiles": TILE_SIZE_PIXELS,
    }
    ORIGINAL_SIZE = 32

    def __init__(self):
        self.tileset = pygame.image.load("assets/tileset.png")

    def load(self, category, type_):
        sequence = self.MAPPING[category][type_]
        # XXX support seqs
        r, c = sequence[0]

        asset = self.tileset.subsurface(
            c * self.ORIGINAL_SIZE,
            r * self.ORIGINAL_SIZE,
            self.ORIGINAL_SIZE,
            self.ORIGINAL_SIZE,
        )
        size = self.SIZES[category]
        asset = pygame.transform.scale(asset, (size, size))

        return asset


ASSETS = Assets()
