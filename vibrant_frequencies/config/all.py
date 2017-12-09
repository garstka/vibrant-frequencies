import json
from pathlib import Path

from .video import VideoConfig
from .sound import SoundConfig


class Config:
    def __init__(self):
        self.__sound = SoundConfig()
        self.__video = VideoConfig()
        self.__config_file = 'config.json'

    @property
    def sound(self) -> SoundConfig:
        return self.__sound

    @sound.setter
    def sound(self, value: SoundConfig):
        self.__sound = value

    @property
    def video(self) -> VideoConfig:
        return self.__video

    @video.setter
    def video(self, value: VideoConfig):
        self.__video = value

    def as_dict(self) -> dict:
        return dict({'sound': self.__sound.as_dict(),
                     'video': self.__video.as_dict()})

    def from_dict(self, value: dict):
        self.__sound.from_dict(value['sound'])
        self.__video.from_dict(value['video'])

    def file_exists(self):
        return Path(self.__config_file).is_file()

    def save(self):
        with open(self.__config_file, 'w') as f:
            json.dump(self.as_dict(), f, sort_keys=True, indent=4)

    def load(self):
        result = dict()
        with open(self.__config_file, 'r') as f:
            self.from_dict(json.load(f))
