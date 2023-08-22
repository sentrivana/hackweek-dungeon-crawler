import logging
import random

import pygame

from game.consts import ENTITY_SIZE_PIXELS, TILE_SIZE_PIXELS
from game.level.types import EntityType, TileType

logger = logging.getLogger(__name__)


class AssetManager:
    """
    Asset/text manager.

    Tileset from https://thedigitaldauber.itch.io/pocket-fables-fantasy-adventure-pack
    """

    # XXX nice paths instead of hardcoded
    ASSETS_FILENAME = "assets/tileset2.png"
    ENEMY_BLURPS_FILENAME = "text/enemies.txt"
    SIGN_BLURPS_FILENAME = "text/signs.txt"
    GAME_OVER_BLURPS_FILENAME = "text/game_over.txt"

    MAPPING = {
        "entities": {
            EntityType.PLAYER: [15],
            EntityType.SIGN: [17],
            EntityType.ENEMY: [11, 12, 14, 18],
        },
        "tiles": {
            TileType.GROUND: [0, 8, 13],
            TileType.HAZARD: [22],
            TileType.WALL: [3],
        },
    }
    SIZES = {
        "entities": ENTITY_SIZE_PIXELS,
        "tiles": TILE_SIZE_PIXELS,
    }
    ORIGINAL_SIZE = 16

    def __init__(self):
        original_tileset = pygame.image.load(self.ASSETS_FILENAME)
        rows = original_tileset.get_height() // self.ORIGINAL_SIZE
        cols = original_tileset.get_width() // self.ORIGINAL_SIZE

        self.tileset = {
            category: pygame.transform.scale(
                original_tileset,
                (self.SIZES[category] * cols, self.SIZES[category] * rows),
            )
            for category in self.SIZES.keys()
        }

        with open(self.ENEMY_BLURPS_FILENAME) as text_file:
            contents = "".join(text_file.readlines())
        self.enemy_blurps = contents.split("\n\n")
        self.enemy_blurps.reverse()

        with open(self.SIGN_BLURPS_FILENAME) as text_file:
            contents = "".join(text_file.readlines())
        self.sign_blurps = contents.split("\n\n")
        self.sign_blurps.reverse()

        with open(self.GAME_OVER_BLURPS_FILENAME) as text_file:
            contents = "".join(text_file.readlines())
        self.game_over_blurps = contents.split("\n\n")

    def load(self, category, type_):
        options = self.MAPPING[category][type_]

        size = self.SIZES[category]
        asset = self.tileset[category].subsurface(
            0,
            random.choice(options) * size,
            size,
            size,
        )
        return asset


ASSETS = AssetManager()
