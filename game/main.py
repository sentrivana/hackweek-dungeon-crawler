import enum
import logging
import sys

import pygame

from game.assets import TEXTS
from game.consts import GAME_TITLE, WINDOW_HEIGHT, WINDOW_WIDTH
from game.controls import MOVEMENT_CONTROLS
from game.events import CustomEvent
from game.level.level import Level
from game.overlay import HUDOverlay, TextOverlay, TorchlightOverlay


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


class State(enum.Enum):
    RUNNING = 0
    OVERLAY = 1
    MINIGAME = 2
    STOPPED = 3
    GAME_OVER = 4
    LEVEL_CLEARED = 5


def run():
    pygame.init()

    logger.debug("Setting window size to %d x %d", WINDOW_WIDTH, WINDOW_HEIGHT)

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()
    state = State.RUNNING
    torchlight_overlay = TorchlightOverlay()
    text_overlay = TextOverlay()
    minigame = None

    level = Level("levels/001.map", "levels/001.ene")
    hud_overlay = HUDOverlay(level)
    hud_blink = False
    bob = False

    pygame.time.set_timer(
        pygame.event.Event(CustomEvent.REGENERATE_TORCHLIGHT.value), 800
    )
    pygame.time.set_timer(pygame.event.Event(CustomEvent.HUD_BLINK.value), 500)
    pygame.time.set_timer(pygame.event.Event(CustomEvent.ENTITY_BOB.value), 500)
    pygame.time.set_timer(
        pygame.event.Event(CustomEvent.COLOR_MINIGAME_ADD_ITEM.value), 500
    )

    pygame.event.post(
        pygame.event.Event(CustomEvent.SHOW_TEXT.value, text=TEXTS.get_text("intro"))
    )

    while state != State.STOPPED:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = state.STOPPED

            elif event.type == CustomEvent.INITIALIZE_MINIGAME.value:
                minigame = event.minigame

            elif event.type == CustomEvent.ENEMY_HIT.value:
                event.enemy.damage_received()

            elif event.type == CustomEvent.ENEMY_DEFEATED.value:
                level.remove_entity(event.enemy)
                minigame = None
                state = State.RUNNING

            elif event.type == CustomEvent.DAMAGE_RECEIVED.value:
                level.damage_received()
                event.enemy.player_hit()

            elif event.type == CustomEvent.IFRAMES_DONE.value:
                level.player.invulnerable = False
                pygame.time.set_timer(
                    pygame.event.Event(CustomEvent.IFRAMES_DONE.value), 0
                )

            elif event.type == CustomEvent.GAME_OVER.value:
                state = State.GAME_OVER
                text_overlay.set_text("GAME OVER\n\n" + event.text, color="red")

            elif event.type == CustomEvent.LEVEL_CLEARED.value:
                state = State.LEVEL_CLEARED
                text_overlay.set_text("LEVEL CLEARED!\n\n" + event.text, color="green")

            elif event.type == CustomEvent.HUD_BLINK.value:
                hud_blink = not hud_blink

            elif event.type == CustomEvent.ENTITY_BOB.value:
                bob = not bob

            if state == State.RUNNING:
                if event.type == pygame.KEYDOWN:
                    if event.key in MOVEMENT_CONTROLS:
                        level.handle_movement(MOVEMENT_CONTROLS[event.key])

                elif event.type == CustomEvent.REGENERATE_TORCHLIGHT.value:
                    torchlight_overlay.generate()

                elif event.type == CustomEvent.SHOW_TEXT.value:
                    state = State.OVERLAY
                    text_overlay.set_text(
                        event.text,
                        color=getattr(event, "color", None),
                    )

                elif event.type == CustomEvent.KEY_PICKED_UP.value:
                    level.remove_entity(event.entity)

                elif event.type == CustomEvent.COFFEE_PICKED_UP.value:
                    level.remove_entity(event.entity)
                    level.player.replenish_health()

                elif event.type == CustomEvent.DOOR_OPENED.value:
                    level.remove_entity(event.entity)

            elif state == State.OVERLAY:
                if event.type == pygame.KEYDOWN:
                    state = State.RUNNING
                    text_overlay.dismiss()

                    if minigame is not None and not minigame.started:
                        state = State.MINIGAME
                        minigame.start()

            elif state == State.MINIGAME:
                if event.type == pygame.KEYDOWN:
                    minigame.input()
                elif event.type == CustomEvent.COLOR_MINIGAME_ADD_ITEM.value:
                    minigame.add_item()

        if state == State.MINIGAME:
            minigame.update()

        screen.fill((0, 0, 0))

        level.render(screen, bob=bob)

        torchlight_overlay.render(screen)

        if state in (State.OVERLAY, State.GAME_OVER, State.LEVEL_CLEARED):
            text_overlay.render(screen)

        elif state == State.MINIGAME:
            minigame.render(screen)

        if not hud_blink or not hud_overlay.should_blink:
            hud_overlay.render(screen)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
