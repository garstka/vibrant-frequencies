import logging

import math

from ..config.all import Config
import pyglet
import pyglet.gl as gl


class VideoDevice:
    def __init__(self, config: Config):
        log = logging.getLogger(__name__)
        conf = config.video

        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        screen = display.get_default_screen()

        template = gl.Config(sample_buffers=1, samples=4, depth_size=16,
                             double_buffer=True)
        try:
            gl_config = screen.get_best_config(template)
        except pyglet.window.NoSuchConfigException:
            template = gl.Config()
            gl_config = screen.get_best_config(template)

        self.__window = pyglet.window.Window(width=conf.screen_width,
                                             height=conf.screen_height,
                                             fullscreen=conf.fullscreen,
                                             vsync=conf.vsync,
                                             resizable=False,
                                             config=gl_config)

    @property
    def window(self):
        return self.__window

    @property
    def screen(self):
        return None

    def clear(self):
        self.window.clear()

    def filled_circle(self, origin, radius, color):
        inner_radius = 0.0
        x, y = origin
        r, g, b = color
        res = min(int(round(2 * math.pi * radius)), 255)

        gl.glPushMatrix()
        gl.glColor3f(r, g, b)
        gl.glTranslatef(x, y, 0.0)
        quadric = gl.gluNewQuadric()
        gl.gluDisk(quadric, inner_radius, radius, res, 1)
        gl.glPopMatrix()

    def fill(self, color):
        r, g, b = color
        gl.glClearColor(r, g, b, 1.0)
        self.clear()

    def line(self, begin, end, color, width):
        x1, y1 = begin
        x2, y2 = end
        r, g, b = color

        gl.glPushMatrix()
        gl.glColor3f(r, g, b)
        gl.glLineWidth(width)
        pyglet.graphics.draw(2, gl.GL_LINES, ('v2f', (x1, y1, x2, y2)))
        gl.glPopMatrix()
