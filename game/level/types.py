from enum import Enum


class TileType(Enum):
    GROUND = 0
    WALL = 1


class EntityType(Enum):
    COFFEE = 2
    PLAYER = 3
    ENEMY = 4
    SIGN = 5
    TREE = 6
    KEY = 7
    DOOR = 8
    WIN = 9


class ItemType(Enum):
    KEY = 0


class EntityMode(Enum):
    IDLE = 0
    FIGHT = 1
