import logging
import random

import pygame

from game.consts import ENTITY_SIZE_PIXELS, TILE_SIZE_PIXELS
from game.level.types import EntityType, TileType

logger = logging.getLogger(__name__)


class AssetManager:
    """
    Asset manager.

    Tileset from https://thedigitaldauber.itch.io/pocket-fables-fantasy-adventure-pack
    """

    FILENAME = "assets/tileset.png"
    MAPPING = {
        "entities": {
            EntityType.PLAYER: [15],
            EntityType.SIGN: [17],
            EntityType.ENEMY: [7, 9, 11, 12, 14, 16, 18, 20],
            EntityType.TREE: [1, 21],
            EntityType.KEY: [26],
            EntityType.DOOR: [27],
            EntityType.WIN: [28],
            EntityType.COFFEE: [29],
        },
        "tiles": {
            TileType.GROUND: [0, 8, 13],
            TileType.WALL: [3],
        },
    }
    SIZES = {
        "entities": ENTITY_SIZE_PIXELS,
        "tiles": TILE_SIZE_PIXELS,
    }
    ORIGINAL_SIZE = 16

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
        options = self.MAPPING[category][type_]

        size = self.SIZES[category]
        asset = self.tileset[category].subsurface(
            0,
            random.choice(options) * size,
            size,
            size,
        )
        return asset


class TextManager:
    FONT_FILENAME = "assets/m5x7.ttf"

    FILENAMES = {
        "intro": "text/intro.txt",
        "enemies": "text/enemies.txt",
        "signs": "text/signs.txt",
        "game_over": "text/game_over.txt",
        "level_cleared": "text/level_cleared.txt",
        "enemy_hit": "text/enemy_hit.txt",
        "player_hit": "text/player_hit.txt",
    }
    SPLIT = [
        "enemies",
        "signs",
        "game_over",
        "enemy_hit",
        "player_hit",
    ]

    def __init__(self):
        self.text = {}

        for category, filename in self.FILENAMES.items():
            with open(filename) as text_file:
                contents = "".join(text_file.readlines())
                if category in self.SPLIT:
                    contents = contents.split("\n\n")
                    contents.reverse()
                else:
                    contents = [contents]
                self.text[category] = [c.strip() for c in contents]

    def get_font(self, size):
        return pygame.font.Font(self.FONT_FILENAME, size)

    def get_text(self, category, exhaust=True):
        if exhaust:
            return self.text[category].pop()
        else:
            return random.choice(self.text[category])


class SoundManager:
    MUSIC_FILENAME = "assets/the-introvert-michael-kobrin-10959.mp3"

    def __init__(self):
        pygame.mixer.init()
        self.music = pygame.mixer.music.load(self.MUSIC_FILENAME)

    def play(self):
        pygame.mixer.music.play(loops=-1)


ASSETS = AssetManager()
TEXTS = TextManager()
SOUNDS = SoundManager()
