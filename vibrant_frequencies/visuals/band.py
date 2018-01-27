from math import cos, sin, pi

import numpy as np

from vibrant_frequencies.tools.color_tools import rgb_to_pygame, rgb_rotate
from ..device.video import VideoDevice


class Band:
    dimensions = 2

    def __init__(self, config, video: VideoDevice, colors,
                 symmetry=False,
                 rotation=False,
                 double_symmetry=False,
                 double_rotation=False,
                 rotate_colors=False):
        self._video = video
        self._colors = colors

        self._screen_width = config.video.screen_width
        self._screen_height = config.video.screen_height

        self._scale = 2.0 / self._screen_width
        self._origin = (int(self._screen_width / 2),
                        int(self._screen_height / 2))

        self._color = self._colors.random()
        self._width = 5
        self._background = (0, 0, 0)

        self._use_rotation = rotation
        self._rotation = 0.0
        self._rotate_step = 2 * pi / 100

        self._symmetry = symmetry
        self._double_symmetry = double_symmetry

        self._use_double_rotation = double_rotation
        self._double_rotation = 0.0

        self._rotate_colors = rotate_colors
        self._color_rotate_step = 2 * np.pi / 2000
        self._color_rotation = 0.0

        self._lines = []

    def activate(self):
        pass

    def apply(self, y_set, dt):
        self._color = self._colors.random()

        spectrum_length = len(y_set)
        step = 2 * pi / spectrum_length

        self._lines.clear()

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

        if self._rotate_colors:
            self._color_rotation += self._color_rotate_step * dt * (0.8 -
                                                                    np.random.uniform())
            while self._color_rotation > 2 * np.pi:
                self._color_rotation -= 2 * np.pi
            while self._color_rotation < 0:
                self._color_rotation += 2 * np.pi

        for (i, r) in enumerate(y_set):
            self._lines.append(self.__line(i=i,
                                           r=r,
                                           step=step,
                                           rotation=self._rotation))

            if self._double_symmetry:
                self._lines.append(
                    self.__line(i=i, r=r, step=step,
                                rotation=self._rotation +
                                         self._double_rotation + pi / 2))

    def draw(self):
        self._video.fill(self._background)

        for x1, y1, x2, y2 in self._lines:
            self.__draw(x1, y1, x2, y2)

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
        self._video.line(begin=(x1, y1),
                         end=(x2, y2),
                         color=self.__rotated(self._color),
                         width=self._width)

    def debug(self):
        pass

    def __rotated(self, c):
        if not self._rotate_colors:
            return c
        return rgb_rotate(c, self._color_rotation)
