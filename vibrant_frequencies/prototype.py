import random
import time

import numpy as np
import pyaudio
import pygame
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

def visualize():
    config = InteractiveConfigProvider().config

    sound = SoundDevice(config)
    video = VideoDevice(config)
    colors = PrototypeColorProvider().colors
    stream = sound.stream
    overflows = 0
    prev_ovf_time = time.time()

    visuals = [ProtoCircles(colors=colors,
                            video=video,
                            config=config),
               Band(colors=colors,
                    video=video,
                    config=config),
               Band(colors=colors,
                    video=video,
                    config=config,
                    rotation=True),
               Band(colors=colors,
                    video=video,
                    config=config,
                    rotation=True,
                    symmetry=True),
               Band(colors=colors,
                    video=video,
                    config=config,
                    rotation=True,
                    symmetry=True,
                    double_symmetry=True),
               Band(colors=colors,
                    video=video,
                    config=config,
                    rotation=True,
                    symmetry=True,
                    double_symmetry=True,
                    double_rotation=True),
               AnimatedProtoCircles(colors=colors,
                                    video=video,
                                    config=config),
               AnimatedProtoCircles(colors=colors,
                                    video=video,
                                    config=config,
                                    linear_waves=True)]

    def dim_reduction(y_set):
        ff = np.max(y_set)
        return ff

    visual_set = VisualSet(visuals=visuals,
                           dim_reduction=dim_reduction)

    events = EventHandler(visual_set=visual_set)

    while not events.should_quit:
        try:
            y = np.fromstring(
                stream.read(sound.frames_per_buffer,
                            exception_on_overflow=False),
                dtype=np.int16)
            y = y.astype(np.float32)
            # print(y)
            f = np.abs(np.fft.rfft(y))

            visual_set.apply(f)

            pygame.display.flip()

            events.poll()
        except IOError:
            overflows += 1
            if time.time() > prev_ovf_time + 1:
                prev_ovf_time = time.time()
                print('Audio buffer has overflowed {} times'.format(overflows))

    stream.stop_stream()
    stream.close()
    sound.pyaudio.terminate()
