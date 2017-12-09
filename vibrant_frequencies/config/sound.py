class SoundConfig:
    __key_devicename = 'deviceName'
    __key_micrate = 'micRate'
    __key_channels = 'channels'

    def __init__(self):
        self.__config = {self.__key_devicename: 'Line In',
                         self.__key_micrate: 48000,
                         self.__key_channels: 1}

    @property
    def device_name(self) -> str:
        return self.__config[self.__key_devicename]

    @device_name.setter
    def device_name(self, value: str):
        self.__config[self.__key_devicename] = value

    @property
    def mic_rate(self) -> int:
        return self.__config[self.__key_micrate]

    @mic_rate.setter
    def mic_rate(self, value: int):
        self.__config[self.__key_micrate] = value

    @property
    def channels(self) -> int:
        return self.__config[self.__key_channels]

    @channels.setter
    def channels(self, value: int):
        self.__config[self.__key_channels] = value

    def as_dict(self) -> dict:
        return self.__config

    def from_dict(self, value: dict):
        self.__config = value
