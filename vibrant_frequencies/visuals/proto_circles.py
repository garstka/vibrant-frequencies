import random

import numpy as np
import pygame


class ProtoCircles:
    def __init__(self, config, video, colors):
        self._screen = video.screen
        self._colors = colors

        self._screen_width = config.video.screen_width
        self._screen_height = config.video.screen_height
        self._scale = 0.5 / self._screen_width

        self._last_color = random.choice(colors)
        self._last_radius = 0

        self._origin = (int(self._screen_width / 2),
                        int(self._screen_height / 2))

    def apply(self, y):

        radius = y * self._scale

        # bad attempt at autoscaling
        # if radius > screenWidth * 0.6:
        #    radius = screenWidth * 0.6
        #    scale = min(screenWidth * 0.6 / ff, scale)

        final_width = 0

        if self._last_radius > 0.4 * self._screen_width and \
                radius > 0.4 * self._screen_width and \
                np.random.uniform() < 0.9:
            pass  # big circles mostly keep their color
        elif radius < 5 and np.random.uniform() < 0.99:
            pass  # small circles almost always keep their color
        # elif radius < 50 and np.random.uniform() < 0.8:
        #    finalWidth = radius * 0.5 * np.random.uniform()  # small circles not full
        else:
            self._last_color = random.choice(self._colors)

        self._last_radius = int(radius)
        # some circles being circles instead of disks
        # if np.random.uniform() < 0.3:
        #    finalWidth = radius * 0.05 * np.random.uniform()

        pygame.draw.circle(self._screen,
                           self._last_color,
                           self._origin,
                           self._last_radius,
                           int(final_width))

    def scale(self, times: float):
        self._scale *= times
