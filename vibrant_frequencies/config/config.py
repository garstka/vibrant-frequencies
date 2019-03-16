from vibrant_frequencies.config.sound_config import SoundConfig
from vibrant_frequencies.config.video_config import VideoConfig


class Config:
    def __init__(self, source: dict):
        self._sound = SoundConfig(source=source.get('sound', {}))
        self._video = VideoConfig(source=source.get('video', {}))

    @property
    def sound(self) -> SoundConfig:
        return self._sound

    @property
    def video(self) -> VideoConfig:
        return self._video

    def to_dict(self) -> dict:
        return dict({'sound': self._sound.to_dict(),
                     'video': self._video.to_dict()})
