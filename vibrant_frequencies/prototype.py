import random
import time

import numpy as np
import pyaudio
import pygame
import sounddevice as sd

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

    screenWidth = config.video.screen_width
    screenHeight = config.video.screen_height
    scale = 0.5 / screenWidth;
    lastColor = random.choice(colors)
    lastRadius = 0;
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

            radius = ff * scale;

            # bad attempt at autoscaling
            # if radius > screenWidth * 0.6:
            #    radius = screenWidth * 0.6
            #    scale = min(screenWidth * 0.6 / ff, scale)

            finalWidth = 0

            if lastRadius > 0.4 * screenWidth and \
                    radius > 0.4 * screenWidth and \
                    np.random.uniform() < 0.9:
                pass  # big circles mostly keep their color
            elif radius < 5 and np.random.uniform() < 0.99:
                pass  # small circles almost always keep their color
            # elif radius < 50 and np.random.uniform() < 0.8:
            #    finalWidth = radius * 0.5 * np.random.uniform()  # small circles not full
            else:
                lastColor = random.choice(colors)

            # some circles being circles instead of disks
            # if np.random.uniform() < 0.3:
            #    finalWidth = radius * 0.05 * np.random.uniform()

            origin_x, origin_y = int(screenWidth / 2), int(screenHeight / 2);

            pygame.draw.circle(screen, lastColor, (origin_x, origin_y),
                               int(radius),
                               int(finalWidth))

            pygame.display.flip()
            ev = pygame.event.poll()
            if ev.type == pygame.QUIT:
                break
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    break
                elif ev.key == pygame.K_UP:
                    scale *= 1.1
                elif ev.key == pygame.K_DOWN:
                    scale *= 0.9

            lastRadius = radius

        except IOError:
            overflows += 1
            if time.time() > prev_ovf_time + 1:
                prev_ovf_time = time.time()
                print('Audio buffer has overflowed {} times'.format(overflows))
    stream.stop_stream()
    stream.close()
    sound.pyaudio.terminate()
