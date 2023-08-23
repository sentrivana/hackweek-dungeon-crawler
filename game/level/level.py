import logging

from game.assets import TEXTS
from game.consts import TILE_COLS, TILE_ROWS
from game.controls import Direction
from game.events import CustomEvent
from game.level.entity import Door, Enemy, Player, Tree, Key, Sign
from game.level.tile import Tile
from game.level.types import EntityType, ItemType, TileType
from game.utils import post_event

logger = logging.getLogger(__name__)


class Level:
    def __init__(self, filename):
        self.map = []
        self.entities = {}
        self.player = None
        self.enemy_count = 0
        self.max_enemies = 0

        self._load_map(filename)

    @property
    def width(self):
        return len(self.map[0])

    @property
    def height(self):
        return len(self.map)

    @property
    def top_left(self):
        return (self.player.row - TILE_ROWS // 2, self.player.col - TILE_COLS // 2)

    def tile(self, row, col):
        if self._tile_exists(row, col):
            return self.map[row][col]
        return Tile(row, col, TileType.WALL)

    def render(self, screen):
        for row in range(self.top_left[0], self.top_left[0] + TILE_ROWS):
            for col in range(self.top_left[1], self.top_left[1] + TILE_COLS):
                self.tile(row, col).render(screen, self.top_left)

        for (row, col), entity in self.entities.items():
            if self._tile_visible(row, col):
                entity.render(screen, self.top_left)

        self.player.render(screen, self.top_left)

    def handle_movement(self, movement):
        target = self._target_tile(self.player, movement)
        target_entity = self.entities.get((target.row, target.col))
        if target_entity:
            target_entity.interact()

        elif self._can_move_to(target):
            self.player.row = target.row
            self.player.col = target.col

    def remove_entity(self, entity):
        row = entity.row
        col = entity.col
        if self.entities[(row, col)].type == EntityType.ENEMY:
            self.enemy_count -= 1
        elif self.entities[(row, col)].type == EntityType.KEY:
            self.player.inventory.append(ItemType.KEY)

        del self.entities[(row, col)]

        logger.debug("Entity at %d %d deleted", row, col)

        if self.enemy_count <= 0:
            post_event(CustomEvent.LEVEL_CLEARED, text=TEXTS.get_text("level_cleared"))

    def damage_received(self):
        self.player.health -= 1
        if self.player.health <= 0:
            post_event(CustomEvent.GAME_OVER, text=TEXTS.get_text("game_over"))

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

        return self.tile(new_row, new_col)

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
        self.enemy_count = 0

        with open(filename) as map_file:
            for row, line in enumerate(map_file):
                self.map.append([])
                for col, code in enumerate(line.strip()):
                    code = int(code)
                    try:
                        tile_type = TileType(code)
                    except ValueError:
                        tile_type = TileType(TileType.GROUND)

                    self.map[-1].append(Tile(row, col, tile_type))

                    try:
                        entity_type = EntityType(code)
                        if entity_type == EntityType.PLAYER:
                            self.player = Player(self, row, col, entity_type)
                        elif entity_type == EntityType.ENEMY:
                            self.enemy_count += 1
                            self.max_enemies += 1
                            self.entities[(row, col)] = Enemy(
                                self, row, col, entity_type
                            )
                        elif entity_type == EntityType.SIGN:
                            self.entities[(row, col)] = Sign(
                                self, row, col, entity_type
                            )
                        elif entity_type == EntityType.KEY:
                            self.entities[(row, col)] = Key(self, row, col, entity_type)
                        elif entity_type == EntityType.TREE:
                            self.entities[(row, col)] = Tree(
                                self, row, col, entity_type
                            )
                        elif entity_type == EntityType.DOOR:
                            self.entities[(row, col)] = Door(
                                self, row, col, entity_type
                            )
                    except ValueError:
                        pass
