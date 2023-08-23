import logging
import random

from game.assets import ASSETS, TEXTS
from game.consts import ENTITY_SIZE_PIXELS, TILE_SIZE_PIXELS
from game.events import CustomEvent
from game.level.types import EntityMode, EntityType
from game.minigame import MINIGAMES
from game.utils import post_event


logger = logging.getLogger(__name__)


class Entity:
    def __init__(self, row, col, type_):
        self.row = row
        self.col = col
        self.type = type_

        self.asset = ASSETS.load("entities", self.type)

        self.mode = EntityMode.IDLE

        self.text = None
        self.color = None
        if self.type == EntityType.ENEMY:
            self.text = TEXTS.get_text("enemies")
            self.color = random.choice(["magenta", "green", "cyan", "violet"])
        elif self.type == EntityType.SIGN:
            self.text = TEXTS.get_text("signs")

        self.minigame = None
        if self.type == EntityType.ENEMY:
            self.minigame = random.choice(MINIGAMES)(self, random.randint(5, 25))

        self.health = 3

        logger.debug("Spawned %s at %d %d", self.type, row, col)

    @property
    def pos(self):
        return (self.row, self.col)

    def render(self, screen, top_left):
        if self.mode == EntityMode.IDLE:
            screen.blit(
                self.asset,
                (
                    (self.col - top_left[1]) * TILE_SIZE_PIXELS
                    + (TILE_SIZE_PIXELS - ENTITY_SIZE_PIXELS) // 2,
                    (self.row - top_left[0]) * TILE_SIZE_PIXELS
                    + (TILE_SIZE_PIXELS - ENTITY_SIZE_PIXELS) // 2,
                ),
            )

    def interact(self):
        logger.debug("Interacting with %s at %d %d", self.type, self.row, self.col)

        if self.type == EntityType.ENEMY:
            if self.mode == EntityMode.IDLE:
                self.mode = EntityMode.FIGHT

                post_event(CustomEvent.SHOW_TEXT, text=self.text, color=self.color)
                post_event(
                    CustomEvent.INITIALIZE_MINIGAME,
                    minigame=self.minigame,
                    enemy=self,
                )

        if self.type == EntityType.SIGN:
            post_event(CustomEvent.SHOW_TEXT, text=self.text)

    def damage_received(self):
        self.health -= 1
        if self.health <= 0:
            post_event(CustomEvent.ENEMY_DEFEATED, enemy=self)
            return
        self.minigame.flashes = 3

    def player_hit(self):
        if self.minigame is not None:
            self.minigame.jitters = 3
