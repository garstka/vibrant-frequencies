import random
import time

import datetime
import numpy as np
import pyaudio
import pygame
import pyglet
import sounddevice as sd

from .visuals.band import Band
from .interactive.event_handler import EventHandler
from .visuals.visual_set import VisualSet
from .visuals.proto_circles import ProtoCircles, AnimatedProtoCircles
from .device.sound import SoundDevice
from .device.video import VideoDevice
from .interactive.config_provider import \
    InteractiveConfigProvider
from .colors.prototype_provider import PrototypeColorProvider


# prototype based on:
# https://github.com/scottlawsonbc/audio-reactive-led-strip
# https://www.makeartwithpython.com/blog/video-synthesizer-in-python/
#
# apt-get install portaudio19-dev
# pip3 install pyaudio
# pip3 install pygame

class Prototype:
    def __init__(self):
        self.config = InteractiveConfigProvider().config

        self.sound = SoundDevice(self.config)
        self.video = VideoDevice(self.config)
        self.window = self.video.window
        self.colors = PrototypeColorProvider()
        self.stream = self.sound.stream
        self.overflows = 0
        self.prev_ovf_time = time.time()

        self.visuals = [ProtoCircles(colors=self.colors,
                                     video=self.video,
                                     config=self.config),
                        Band(colors=self.colors,
                             video=self.video,
                             config=self.config),
                        Band(colors=self.colors,
                             video=self.video,
                             config=self.config,
                             rotation=True),
                        Band(colors=self.colors,
                             video=self.video,
                             config=self.config,
                             rotation=True,
                             symmetry=True),
                        Band(colors=self.colors,
                             video=self.video,
                             config=self.config,
                             rotation=True,
                             symmetry=True,
                             double_symmetry=True),
                        Band(colors=self.colors,
                             video=self.video,
                             config=self.config,
                             rotation=True,
                             symmetry=True,
                             double_symmetry=True,
                             double_rotation=True),
                        Band(colors=self.colors,
                             video=self.video,
                             config=self.config,
                             rotation=True,
                             symmetry=True,
                             double_symmetry=True,
                             double_rotation=True,
                             rotate_colors=True),
                        AnimatedProtoCircles(colors=self.colors,
                                             video=self.video,
                                             config=self.config),
                        AnimatedProtoCircles(colors=self.colors,
                                             video=self.video,
                                             config=self.config,
                                             linear_waves=True),
                        AnimatedProtoCircles(colors=self.colors,
                                             video=self.video,
                                             config=self.config,
                                             linear_waves=True,
                                             rotate_colors=True),
                        AnimatedProtoCircles(colors=self.colors,
                                             video=self.video,
                                             config=self.config,
                                             rotate_colors=True)]

        def dim_reduction(y_set):
            ff = np.max(y_set)
            return ff

        self.visual_set = VisualSet(visuals=self.visuals,
                                    dim_reduction=dim_reduction)

        self.events = EventHandler(visual_set=self.visual_set,
                                   window=self.video.window)

        self.time_scale = 50.0
        self.t0 = datetime.datetime.now()

        self.fps_display = pyglet.clock.ClockDisplay()

        prototype = self

        @self.video.window.event
        def on_draw():
            prototype.draw()

        def update(dt):
            prototype.update(dt)

        pyglet.clock.schedule_interval(update, 1 / self.config.video.fps)

        pyglet.app.run()

        self.stream.stop_stream()
        self.stream.close()
        self.sound.pyaudio.terminate()

    def update(self, dt):
        try:
            y = np.fromstring(
                self.stream.read(self.sound.frames_per_buffer,
                                 exception_on_overflow=False),
                dtype=np.int16)
            y = y.astype(np.float32)
            f = np.abs(np.fft.rfft(y))

            self.visual_set.apply(f,
                                  dt=dt * self.time_scale)

        except IOError:
            self.overflows += 1
            if time.time() > self.prev_ovf_time + 1:
                self.prev_ovf_time = time.time()
                print('Audio buffer has overflowed {} times'.format(
                    self.overflows))

    def draw(self):
        self.visual_set.draw()
        if self.config.video.display_fps:
            self.fps_display.draw()
