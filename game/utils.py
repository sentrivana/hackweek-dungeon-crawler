import logging

import pygame

logger = logging.getLogger(__name__)


def post_event(custom_event, **kwargs):
    pygame.event.post(pygame.event.Event(custom_event.value, **kwargs))
    logger.debug("Posted event %s", custom_event)
