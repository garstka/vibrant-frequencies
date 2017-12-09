import logging

from ..config.all import Config
import pygame


class VideoDevice:
    def __init__(self, config: Config):
        log = logging.getLogger(__name__)
        conf = config.video

        dimensions = (conf.screen_width, conf.screen_height)
        flags = 0

        if conf.vsync:
            flags = flags | pygame.HWSURFACE | pygame.DOUBLEBUF
            if not conf.fullscreen:
                log.warning("VSync may not work in windowed mode.")

        if conf.fullscreen:
            flags = flags | pygame.FULLSCREEN

        self.__screen = pygame.display.set_mode(dimensions, flags)
        pygame.init()

    @property
    def screen(self):
        return self.__screen
