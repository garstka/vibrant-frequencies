import os
from pathlib import Path
from typing import Any

import sounddevice
from screeninfo import get_monitors

from vibrant_frequencies.config.config import Config
from vibrant_frequencies.config.save_config import load_config, save_config

CONFIG_FILE = 'config.json'


class InteractiveConfigProvider:
    def __init__(self):

        if Path(CONFIG_FILE).is_file():
            if input("Enter to use existing config : ") == '':
                self._config = load_config(CONFIG_FILE)
                return

        self._config = Config(source={})

        print("===============================")
        print("Devices: ")
        print(sounddevice.query_devices())

        while True:
            if os.name == 'nt':
                print("Choose WASAPI device with only output channels"
                      " for loopback.")

            device_id = int(input("Which device to use? : "))
            info = sounddevice.query_devices(int(device_id))
            print(info)

            if input("Press enter to use this device: ") != '':
                continue

            self._config.sound.device_name = info['name']
            self._config.sound.mic_rate = int(info['default_samplerate'])

            if info['max_input_channels'] == 0:
                if os.name != 'nt':
                    print("This doesn't seem to be an input device.")
                else:
                    print("Will try to use this device as loopback device.")

            self._config.sound.channels = 1  # info['max_input_channels']

            if self._config.sound.mic_rate < 48000:
                if input(("Press enter to use a higher"
                          " mic rate than default (recommended): ")) == '':
                    self._config.sound.mic_rate = 48000

            self._config.sound.windows_loopback = (
                os.name == 'nt' and info['max_input_channels'] == 0)
            break

        default_screen_width = get_monitors()[0].width
        default_screen_height = get_monitors()[0].height
        default_fps = 60
        default_fullscreen = 'y'
        default_vsync = 'y'

        def ask(label: str, default: Any) -> Any:
            print("{label} [{default}]: ".format(label=label,
                                                 default=default), end='')
            result = input()
            return result if result else default

        screen_width = ask("Screen width", default_screen_width)
        screen_height = ask("Screen height", default_screen_height)
        fps = ask("FPS", default_fps)
        fullscreen = ask("Fullscreen", default_fullscreen)
        vsync = ask("Vsync", default_vsync)

        self._config.video.screen_width = int(screen_width)
        self._config.video.screen_height = int(screen_height)
        self._config.video.fps = int(fps)
        self._config.video.fullscreen = fullscreen == 'y'
        self._config.video.vsync = vsync == 'y'

        save_config(config=self._config, file=CONFIG_FILE)

    @property
    def config(self):
        return self._config
