import enum
import logging
import random
import sys

import pygame

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

    level = Level("levels/001.map")
    hud_overlay = HUDOverlay(level)

    pygame.time.set_timer(
        pygame.event.Event(CustomEvent.REGENERATE_TORCHLIGHT.value), 800
    )

    # XXX put this somewhere
    from textwrap import dedent

    text = dedent(
        """\
        Another day,
        another bug squashing mission.

        Never seen this codebase before.

        Hope there's at least some
        documentation.

        Oh hey I already see some
        comments!
    """
    )
    pygame.event.post(pygame.event.Event(CustomEvent.SHOW_TEXT.value, text=text))

    while state != State.STOPPED:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = state.STOPPED
            elif event.type == CustomEvent.INITIALIZE_MINIGAME.value:
                minigame = event.minigame(event.enemy)
            elif event.type == CustomEvent.ENEMY_DEFEATED.value:
                level.remove_enemy(event.row, event.col)
                minigame = None
                state = State.RUNNING
            elif event.type == CustomEvent.DAMAGE_RECEIVED.value:
                level.damage_received()
            elif event.type == CustomEvent.GAME_OVER.value:
                state = State.GAME_OVER
                text_overlay.set_text("GAME OVER\n\n" + event.text)
            elif event.type == CustomEvent.LEVEL_CLEARED.value:
                state = State.LEVEL_CLEARED
                text_overlay.set_text("LEVEL CLEARED!\n\n" + event.text)

            if state == State.RUNNING:
                if event.type == pygame.KEYDOWN:
                    if event.key in MOVEMENT_CONTROLS:
                        level.handle_movement(MOVEMENT_CONTROLS[event.key])

                elif event.type == CustomEvent.REGENERATE_TORCHLIGHT.value:
                    torchlight_overlay.generate()

                elif event.type == CustomEvent.SHOW_TEXT.value:
                    state = State.OVERLAY
                    text_overlay.set_text(event.text, getattr(event, "color", None))

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

        screen.fill((0, 0, 0))

        level.render(screen)

        torchlight_overlay.render(screen)

        if state in (State.OVERLAY, State.GAME_OVER, State.LEVEL_CLEARED):
            text_overlay.render(screen)

        elif state == State.MINIGAME:
            minigame.render(screen, dt)

        hud_overlay.render(screen)

        pygame.display.flip()

        dt = clock.tick(60) / 1000

    pygame.quit()
