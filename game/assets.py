import logging

import pygame

from game.consts import ENTITY_SIZE_PIXELS, TILE_SIZE_PIXELS
from game.level.types import EntityType, TileType

logger = logging.getLogger(__name__)


class AssetManager:
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
        original_tileset = pygame.image.load(self.FILENAME)
        rows = original_tileset.get_height() // self.ORIGINAL_SIZE
        cols = original_tileset.get_width() // self.ORIGINAL_SIZE

        self.tileset = {
            category: pygame.transform.scale(
                original_tileset,
                (self.SIZES[category] * cols, self.SIZES[category] * rows),
            )
            for category in self.SIZES.keys()
        }

    def load(self, category, type_):
        sequence = self.MAPPING[category][type_]
        # XXX support sequences/animation
        r, c = sequence[0]

        size = self.SIZES[category]
        asset = self.tileset[category].subsurface(
            c * size,
            r * size,
            size,
            size,
        )
        return asset


ASSETS = AssetManager()
