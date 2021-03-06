import time

import datetime
from contextlib import ExitStack

import numpy as np
import pygame

from vibrant_frequencies.helper.on_exit import on_exit
from vibrant_frequencies.visuals.combo import Combo
from .visuals.band import Band
from .interactive.event_handler import EventHandler
from .visuals.visual_set import VisualSet
from .visuals.proto_circles import ProtoCircles, AnimatedProtoCircles
from .device.sound import SoundDevice
from .device.video import VideoDevice
from .interactive.config_provider import \
    InteractiveConfigProvider
from .colors.prototype_provider import PrototypeColorProvider


def visualize():
    config = InteractiveConfigProvider().config

    sound = SoundDevice(config)
    video = VideoDevice(config)
    colors = PrototypeColorProvider()
    stream = sound.stream
    overflows = 0
    prev_ovf_time = time.time()

    def dim_reduction(y_set):
        ff = np.percentile(y_set, 99.0)
        return ff

    debug = False
    visuals = []
    if debug:
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
                   Band(colors=colors,
                        video=video,
                        config=config,
                        rotation=True,
                        symmetry=True,
                        double_symmetry=True,
                        double_rotation=True,
                        rotate_colors=True),
                   AnimatedProtoCircles(colors=colors,
                                        video=video,
                                        config=config),
                   AnimatedProtoCircles(colors=colors,
                                        video=video,
                                        config=config,
                                        linear_waves=True),
                   AnimatedProtoCircles(colors=colors,
                                        video=video,
                                        config=config,
                                        linear_waves=True,
                                        rotate_colors=True),
                   AnimatedProtoCircles(colors=colors,
                                        video=video,
                                        config=config,
                                        rotate_colors=True)]

    visuals.append(Combo(colors=colors,
                         video=video,
                         config=config,
                         dim_reduction=dim_reduction))

    visual_set = VisualSet(visuals=visuals,
                           dim_reduction=dim_reduction)

    events = EventHandler(visual_set=visual_set)

    time_scale = 1.0
    t0 = datetime.datetime.now()
    with ExitStack() as stack:
        stack.enter_context(on_exit(lambda: sound.pyaudio.terminate()))
        stack.enter_context(on_exit(lambda: stream.close()))
        stack.enter_context(on_exit(lambda: stream.stop_stream()))

        while not events.should_quit:
            try:
                t1 = datetime.datetime.now()
                y = np.fromstring(
                    stream.read(sound.frames_per_buffer,
                                exception_on_overflow=False),
                    dtype=np.int16)
                y = y.astype(np.float32)
                # print(y)
                f = np.abs(np.fft.rfft(y))

                visual_set.apply(f,
                                 dt=(
                                        t1 - t0).microseconds / 1000000.0 * time_scale)

                pygame.display.flip()

                events.poll()

                t0 = t1
            except IOError:
                overflows += 1
                if time.time() > prev_ovf_time + 1:
                    prev_ovf_time = time.time()
                    print('Audio buffer has overflowed {} times'.format(
                        overflows))
