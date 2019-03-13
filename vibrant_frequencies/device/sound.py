import math
import sounddevice

from ..config.all import Config
import pyaudio


class SoundDevice:
    def __init__(self, config: Config):
        self.__pyaudio = pyaudio.PyAudio()

        device_name = config.sound.device_name
        # device = sounddevice.query_devices(config.sound.device_name)
        device_count = len(sounddevice.query_devices())

        device_id = None

        for i in range(0, device_count):
            device_info = sounddevice.query_devices(i)
            name = device_info['name']
            if name.startswith(device_name):
                device_id = i
                break

        if device_id is None:
            raise ValueError("Invalid device.")

        rate = config.sound.mic_rate
        channels = 1  # self.__config.sound.channels
        fps = config.video.fps

        ratio = rate / fps
        print(ratio)
        self.__frames_per_buffer = 2 ** int(math.log(rate / fps, 2))
        # self.__frames_per_buffer = int(rate / fps)
        # as_loopback=True
        self.__stream = \
            self.__pyaudio.open(format=pyaudio.paInt16,
                                channels=channels,
                                rate=rate,
                                input=True,
                                frames_per_buffer=self.__frames_per_buffer,
                                input_device_index=device_id)

    @property
    def pyaudio(self):
        return self.__pyaudio

    @property
    def stream(self):
        return self.__stream

    @property
    def frames_per_buffer(self):
        return self.__frames_per_buffer
