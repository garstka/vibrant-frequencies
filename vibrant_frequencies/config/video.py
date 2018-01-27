class VideoConfig:
    __key_fps = 'framesPerSecond'
    __key_width = 'screenWidth'
    __key_height = 'screenHeight'
    __key_fullscreen = 'fullscreen'
    __key_vsync = 'vSync'
    __key_display_fps = 'displayFps'

    def __init__(self):
        self.__config = {self.__key_fps: 60,
                         self.__key_width: 1920,
                         self.__key_height: 1080,
                         self.__key_fullscreen: True,
                         self.__key_vsync: True,
                         self.__key_display_fps: False}

    @property
    def fps(self) -> int:
        return self.__config[self.__key_fps]

    @fps.setter
    def fps(self, value: int):
        self.__config[self.__key_fps] = value

    @property
    def screen_width(self) -> int:
        return self.__config[self.__key_width]

    @screen_width.setter
    def screen_width(self, value: int):
        self.__config[self.__key_width] = value

    @property
    def screen_height(self):
        return self.__config[self.__key_height]

    @screen_height.setter
    def screen_height(self, value):
        self.__config[self.__key_height] = value

    @property
    def fullscreen(self) -> bool:
        return self.__config[self.__key_fullscreen]

    @fullscreen.setter
    def fullscreen(self, value: bool):
        self.__config[self.__key_fullscreen] = value

    @property
    def vsync(self) -> bool:
        return self.__config[self.__key_vsync]

    @vsync.setter
    def vsync(self, value: bool):
        self.__config[self.__key_vsync] = value

    @property
    def display_fps(self) -> bool:
        return self.__config[self.__key_display_fps]

    @display_fps.setter
    def display_fps(self, value: bool):
        self.__config[self.__key_display_fps] = value

    def as_dict(self) -> dict:
        return self.__config

    def from_dict(self, value: dict):
        self.__config.update(value)
