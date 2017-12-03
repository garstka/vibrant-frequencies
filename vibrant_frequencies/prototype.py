import time
import numpy as np
import pyaudio
import random
import pygame
import sounddevice as sd


# prototype based on:
# https://github.com/scottlawsonbc/audio-reactive-led-strip
# https://www.makeartwithpython.com/blog/video-synthesizer-in-python/
#
# apt-get install portaudio19-dev
# pip3 install pyaudio
# pip3 install pygame

def visualize():
    print(sd.query_devices())

    device = input("Which device to use? : ")
    p = pyaudio.PyAudio()
    info = p.get_device_info_by_index(int(device))
    print(info)

    if input("Enter to continue: ") != '':
        exit(0)

    device = int(device)

    screenWidth, screenHeight = 1920, 1080  # 800, 800
    screen = pygame.display.set_mode((screenWidth, screenHeight),
                                     pygame.HWSURFACE | pygame.FULLSCREEN)
    colors = [(229, 244, 227), (93, 169, 233), (0, 63, 145), (255, 255, 255),
              (109, 50, 109)]
    mic_rate = 44100
    # mic_rate = 48000
    fps = 60
    frames_per_buffer = int(mic_rate / fps)
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=mic_rate,
                    input=True,
                    frames_per_buffer=frames_per_buffer,
                    input_device_index=device)
    overflows = 0
    prev_ovf_time = time.time()
    pygame.init()
    scale = 0.5 / screenWidth;
    lastColor = random.choice(colors)
    lastRadius = 0;
    while True:
        try:
            y = np.fromstring(
                stream.read(frames_per_buffer, exception_on_overflow=False),
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

            if lastRadius > 0.4 * screenWidth and \
                    radius > 0.4 * screenWidth and \
                    np.random.uniform() < 0.9:
                pass  # big circles mostly keep their color
            elif radius < 5 and np.random.uniform() < 0.99:
                pass  # small circles almost always keep their color
            else:
                lastColor = random.choice(colors)

            finalWidth = 0
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
    p.terminate()
