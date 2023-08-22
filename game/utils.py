import pygame


def post_event(custom_event, **kwargs):
    pygame.event.post(pygame.event.Event(custom_event.value, **kwargs))
