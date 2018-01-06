import random
from math import cos, sin, pi

import numpy as np
import pygame

from ..device.video import VideoDevice


class Band:
    dimensions = 2

    def __init__(self, config, video: VideoDevice, colors,
                 symmetry=False,
                 rotation=False,
                 double_symmetry=False,
                 double_rotation=False):
        self._screen = video.screen
        self._colors = colors

        self._screen_width = config.video.screen_width
        self._screen_height = config.video.screen_height

        self._scale = 0.5 / self._screen_width
        self._origin = (int(self._screen_width / 2),
                        int(self._screen_height / 2))

        self._color = random.choice(self._colors)
        self._width = 5
        self._background = (0, 0, 0)

        self._use_rotation = rotation
        self._rotation = 0.0
        self._rotate_step = 2 * pi / 60

        self._symmetry = symmetry
        self._double_symmetry = double_symmetry

        self._use_double_rotation = double_rotation
        self._double_rotation = 0.0

    def activate(self):
        pass

    def apply(self, y_set, dt):
        self._screen.fill(self._background)

        self._color = random.choice(self._colors)

        spectrum_length = len(y_set)
        step = 2 * pi / spectrum_length

        if self._use_rotation:
            self._rotation += self._rotate_step * (0.5 - np.random.uniform()) \
                              * dt
            if self._rotation > 2 * pi:
                self._rotation = 0.0

            if self._double_symmetry and self._use_double_rotation:
                self._double_rotation += \
                    self._rotate_step * (0.5 - np.random.uniform()) * dt
                if self._double_rotation > 2 * pi:
                    self._double_rotation = 0.0

        for (i, r) in enumerate(y_set):
            x1, y1, x2, y2 = self.__line(i=i,
                                         r=r,
                                         step=step,
                                         rotation=self._rotation)
            self.__draw(x1, y1, x2, y2)
            if self._double_symmetry:
                x3, y3, x4, y4 = \
                    self.__line(i=i, r=r, step=step,
                                rotation=self._rotation +
                                         self._double_rotation + pi / 2)
                self.__draw(x3, y3, x4, y4)

    def scale(self, times: float):
        self._scale *= times

    def __components(self, i, r, rotation, step):
        r *= self._scale
        x_comp = r * sin(rotation + i * step)
        y_comp = r * cos(rotation + i * step)
        return x_comp, y_comp

    def __line(self, i, r, step, rotation):

        ox, oy = self._origin
        x_comp, y_comp = self.__components(i, r,
                                           rotation,
                                           step)
        x1, y1 = ox + x_comp, oy + y_comp
        if self._symmetry:
            x2, y2 = ox - x_comp, oy - y_comp
        else:
            x2, y2 = ox, oy

        return x1, y1, x2, y2

    def __draw(self, x1, y1, x2, y2):
        pygame.draw.line(self._screen,
                         self._color,
                         (x1, y1),
                         (x2, y2),
                         self._width)
