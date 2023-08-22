import logging

from game.consts import TILE_COLS, TILE_ROWS
from game.controls import Direction
from game.level.entity import Entity
from game.level.tile import Tile
from game.level.types import EntityType, TileType

logger = logging.getLogger(__name__)


class Level:
    def __init__(self, filename):
        self.map = []
        self.entities = []
        self.player = None

        self._load_map(filename)

    @property
    def width(self):
        return len(self.map[0])

    @property
    def height(self):
        return len(self.map)

    @property
    def top_left(self):
        return (
            min(
                max(self.player.row - TILE_ROWS // 2, 0),
                self.height - TILE_ROWS,
            ),
            min(
                max(self.player.col - TILE_COLS // 2, 0),
                self.width - TILE_COLS,
            ),
        )

    def tile(self, row, col):
        if self._tile_exists(row, col):
            return self.map[row][col]
        return Tile(row, col, TileType.WALL)

    def render(self, screen):
        for row in range(self.top_left[0], self.top_left[0] + TILE_ROWS):
            for col in range(self.top_left[1], self.top_left[1] + TILE_COLS):
                self.tile(row, col).render(screen, self.top_left)

        for entity in self.entities:
            if self._tile_visible(row, col):
                entity.render(screen, self.top_left)

        self.player.render(screen, self.top_left)

    def handle_movement(self, movement):
        target = self._target_tile(self.player, movement)
        if target is not None and self._can_move_to(target):
            self.player.row = target.row
            self.player.col = target.col

    def dist_to_player(self, tile):
        return max(abs(tile.row - self.player.row), abs(tile.col - self.player.col))

    def _target_tile(self, origin, movement):
        if movement == Direction.UP:
            vec = (-1, 0)
        elif movement == Direction.RIGHT:
            vec = (0, 1)
        elif movement == Direction.DOWN:
            vec = (1, 0)
        elif movement == Direction.LEFT:
            vec = (0, -1)

        new_row = origin.row + vec[0]
        new_col = origin.col + vec[1]

        if not self._tile_exists(new_row, new_col):
            return None

        return self.map[new_row][new_col]

    def _can_move_to(self, target):
        return target and target.walkable

    def _tile_exists(self, row, col):
        return 0 <= row <= self.height - 1 and 0 <= col <= self.width - 1

    def _tile_visible(self, row, col):
        return (
            self.top_left[0] <= row <= self.top_left[0] + TILE_ROWS
            and self.top_left[1] <= col <= self.top_left[1] + TILE_COLS
        )

    def _load_map(self, filename):
        with open(filename) as map_file:
            level_read = False

            for row, line in enumerate(map_file):
                line = line.strip()

                if not line:
                    level_read = True
                    row_offset = row + 1

                if not level_read:
                    self.map.append([])
                    for col, code in enumerate(line.strip()):
                        self.map[-1].append(Tile(row, col, TileType(int(code))))

                else:
                    for col, code in enumerate(line.strip()):
                        entity_type = EntityType(int(code))
                        if entity_type == EntityType.EMPTY:
                            continue
                        elif entity_type == EntityType.PLAYER:
                            self.player = Entity(row - row_offset, col, entity_type)
                        else:
                            self.entities.append(
                                Entity(row - row_offset, col, entity_type)
                            )
