import random
import time

import numpy as np
import pyaudio
import pygame
import sounddevice as sd

from .visuals.proto_circles import ProtoCircles
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
    screen = video.screen
    colors = PrototypeColorProvider().colors
    stream = sound.stream
    overflows = 0
    prev_ovf_time = time.time()

    visual = ProtoCircles(colors=colors,
                          video=video,
                          config=config)

    while True:
        try:
            y = np.fromstring(
                stream.read(sound.frames_per_buffer,
                            exception_on_overflow=False),
                dtype=np.int16)
            y = y.astype(np.float32)
            # print(y)
            f = np.abs(np.fft.rfft(y))
            ff = np.max(f)
            print(ff)

            visual.apply(ff)

            pygame.display.flip()

            ev = pygame.event.poll()
            if ev.type == pygame.QUIT:
                break
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    break
                elif ev.key == pygame.K_UP:
                    visual.scale(times=1.1)
                elif ev.key == pygame.K_DOWN:
                    visual.scale(times=0.9)

        except IOError:
            overflows += 1
            if time.time() > prev_ovf_time + 1:
                prev_ovf_time = time.time()
                print('Audio buffer has overflowed {} times'.format(overflows))
    stream.stop_stream()
    stream.close()
    sound.pyaudio.terminate()
