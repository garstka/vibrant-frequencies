import datetime
import numpy as np
import pygame
import pygame.gfxdraw

from vibrant_frequencies.tools.color_tools import rgb_to_pygame, rgb_rotate


class ProtoCircleProvider:
    dimensions = 1

    def __init__(self,
                 colors,
                 screen_width,
                 screen_height):
        self._colors = colors

        self._screen_width = screen_width
        self._screen_height = screen_height
        self._scale = 1.0 / self._screen_width

        self._last_color = colors.random()
        self._last_radius = 0
        self._last_width = 0

    def next(self, y):

        radius = y * self._scale

        # bad attempt at autoscaling
        # if radius > screenWidth * 0.6:
        #    radius = screenWidth * 0.6
        #    scale = min(screenWidth * 0.6 / ff, scale)

        if self._last_radius > 0.4 * self._screen_width and \
            radius > 0.4 * self._screen_width and \
            np.random.uniform() < 0.9:
            pass  # big circles mostly keep their color
        elif radius < 5 and np.random.uniform() < 0.99:
            pass  # small circles almost always keep their color
        # elif radius < 50 and np.random.uniform() < 0.8:
        #    finalWidth = radius * 0.5 * np.random.uniform()  # small circles not full
        else:
            self._last_color = self._colors.random()

        self._last_radius = int(radius)
        # some circles being circles instead of disks
        # if np.random.uniform() < 0.3:
        #    finalWidth = radius * 0.05 * np.random.uniform()

    def scale(self, times: float):
        self._scale *= times

    @property
    def color(self):
        return self._last_color

    @property
    def colors(self):
        return self._colors

    @property
    def radius(self):
        return self._last_radius

    @property
    def width(self):
        return self._last_width


class ProtoCircles:
    dimensions = 1

    def __init__(self, config, video, colors):
        self._provider = \
            ProtoCircleProvider(colors=colors,
                                screen_width=config.video.screen_width,
                                screen_height=config.video.screen_height)

        self._screen = video.screen

        self._origin = (int(config.video.screen_width / 2),
                        int(config.video.screen_height / 2))

        self._background = (0.0, 0.0, 0.0)

        self._provider.scale(2.0)

    def activate(self):
        self._screen.fill(rgb_to_pygame(self._provider.color))

    def apply(self, y, dt):
        self._provider.next(y)

        pygame.draw.circle(self._screen,
                           rgb_to_pygame(self._provider.color),
                           self._origin,
                           self._provider.radius,
                           self._provider.width)

    def scale(self, times: float):
        self._provider.scale(times)


class AnimatedProtoCircles(ProtoCircles):
    dimensions = 1

    def __init__(self, config, video, colors, linear_waves=False,
                 rotate_colors=False):
        super().__init__(config, video, colors)

        screen_width = config.video.screen_width
        screen_height = config.video.screen_height
        self._max_radius = np.sqrt(screen_width ** 2 + screen_height ** 2) / 2

        self._layers = list()
        self._width = 0
        self._background = self._provider.color
        self._velocity = 0.01
        self._last_radius = self._max_radius

        self._linear_waves = linear_waves
        self._linear_velocity = int(screen_width / 200)

        self._rotate_colors = rotate_colors
        self._color_rotate_step = 2 * np.pi / 1000
        self._color_rotation = 0.0

    def apply(self, y, dt, y2=None):
        self._provider.next(y)

        color = self._provider.color
        radius = self._provider.radius

        if radius > self._max_radius:
            self._background = color
            self._layers = []
        else:
            self._layers = [(self.__scale_up(r, dt), c)
                            for r, c in self._layers
                            if r > radius]

            while self._layers:
                r, c = self._layers[0]
                if r > self._max_radius:
                    self._background = c
                    del self._layers[0]
                else:
                    break

            self._layers.extend([(radius, color)])

        if self._rotate_colors:
            self._color_rotation += self._color_rotate_step * (
                np.random.uniform()) * (0.2 + np.sin(
                datetime.datetime.now().microsecond / 1000000.0))
            while self._color_rotation > 2 * np.pi:
                self._color_rotation -= 2 * np.pi
            while self._color_rotation < 0:
                self._color_rotation += 2 * np.pi

        self._screen.fill(rgb_to_pygame(self.__rotated(self._background)))

        for r, c in self._layers:
            self.__circle(r, c)

        self._last_radius = radius

    def __scale_up(self, radius, dt):
        if self._linear_waves:
            return radius + self._linear_velocity * dt
        else:
            return radius * (1.0 + self._velocity * dt)

    def __circle(self, r, c, w=0):
        pygame.draw.circle(self._screen,
                           rgb_to_pygame(self.__rotated(c)),
                           self._origin,
                           int(r),
                           0)

    def __gfxcircle(self, r, c, w=0):
        pygame.gfxdraw.filled_circle(self._screen,
                                     self._origin[0],
                                     self._origin[1],
                                     int(r),
                                     rgb_to_pygame(self.__rotated(c)))

    def __rotated(self, c):
        if not self._rotate_colors:
            return c
        return rgb_rotate(c, self._color_rotation)

    def debug(self):
        print([self.__rotated(c) for c in self._provider.colors.all()])
