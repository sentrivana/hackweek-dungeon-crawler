from game.assets import ASSETS
from game.consts import TILE_SIZE_PIXELS
from game.level.types import TileType


class Tile:
    def __init__(self, row, col, type_):
        self.row = row
        self.col = col
        self.type = type_

        self.asset = ASSETS.load("tiles", self.type)

    @property
    def pos(self):
        return (self.row, self.col)

    @property
    def walkable(self):
        return self.type not in {TileType.WALL}

    def render(self, screen, top_left):
        if self.asset is None:
            return

        rect = (
            (self.col - top_left[1]) * TILE_SIZE_PIXELS,
            (self.row - top_left[0]) * TILE_SIZE_PIXELS,
        )
        screen.blit(self.asset, rect)
