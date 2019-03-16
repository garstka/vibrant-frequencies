from typing import Optional


class VideoConfig:
    def __init__(self, source: dict):
        self._fps = source.get('framesPerSecond')
        self._screen_width = source.get('screenWidth')
        self._screen_height = source.get('screenHeight')
        self._fullscreen = source.get('fullscreen')
        self._vsync = source.get('vsync')

    @property
    def fps(self) -> Optional[int]:
        return self._fps

    @fps.setter
    def fps(self, value: int):
        self._fps = value

    @property
    def screen_width(self) -> Optional[int]:
        return self._screen_width

    @screen_width.setter
    def screen_width(self, value: int):
        self._screen_width = value

    @property
    def screen_height(self) -> Optional[int]:
        return self._screen_height

    @screen_height.setter
    def screen_height(self, value: int):
        self._screen_height = value

    @property
    def fullscreen(self) -> Optional[bool]:
        return self._fullscreen

    @fullscreen.setter
    def fullscreen(self, value: bool):
        self._fullscreen = value

    @property
    def vsync(self) -> Optional[bool]:
        return self._vsync

    @vsync.setter
    def vsync(self, value: bool):
        self._vsync = value

    def to_dict(self) -> dict:
        return {'framesPerSecond': self._fps,
                'screenWidth': self._screen_width,
                'screenHeight': self._screen_height,
                'fullscreen': self._fullscreen,
                'vsync': self._vsync}
