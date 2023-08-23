import enum

import pygame


class CustomEvent(enum.Enum):
    REGENERATE_TORCHLIGHT = pygame.USEREVENT + 0
    SHOW_TEXT = pygame.USEREVENT + 1
    INTERACT_WITH_ENTITY = pygame.USEREVENT + 2
    ENEMY_DEFEATED = pygame.USEREVENT + 3
    GAME_OVER = pygame.USEREVENT + 4
    INITIALIZE_MINIGAME = pygame.USEREVENT + 5
    START_MINIGAME = pygame.USEREVENT + 6
    DAMAGE_RECEIVED = pygame.USEREVENT + 7
    LEVEL_CLEARED = pygame.USEREVENT + 8
    HUD_BLINK = pygame.USEREVENT + 9
