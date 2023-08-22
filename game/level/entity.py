import logging

from game.assets import ASSETS
from game.consts import ENTITY_SIZE_PIXELS, TILE_SIZE_PIXELS


logger = logging.getLogger(__name__)


class Entity:
    def __init__(self, row, col, type_):
        self.row = row
        self.col = col
        self.type = type_

        self.asset = ASSETS.load("entities", self.type)

        logger.debug("Spawned %s at %d %d", self.type, row, col)

    @property
    def pos(self):
        return (self.row, self.col)

    def render(self, screen, top_left):
        if self.asset is None:
            return

        screen.blit(
            self.asset,
            (
                (self.col - top_left[1]) * TILE_SIZE_PIXELS
                + (TILE_SIZE_PIXELS - ENTITY_SIZE_PIXELS) // 2,
                (self.row - top_left[0]) * TILE_SIZE_PIXELS
                + (TILE_SIZE_PIXELS - ENTITY_SIZE_PIXELS) // 2,
            ),
        )
