from enum import Enum


class TileType(Enum):
    GROUND = 0
    WALL = 1
    HAZARD = 2


class EntityType(Enum):
    PLAYER = 3
    ENEMY = 4
    SIGN = 5
    TREE = 6


class EntityMode(Enum):
    IDLE = 0
    FIGHT = 1
