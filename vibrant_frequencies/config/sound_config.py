from typing import Optional


class SoundConfig:
    def __init__(self, source: dict):
        self._device_name = source.get('deviceName')
        self._mic_rate = source.get('micRate')
        self._channels = source.get('channels')
        self._windows_loopback = source.get('windowsLoopback')

    @property
    def device_name(self) -> Optional[str]:
        return self._device_name

    @device_name.setter
    def device_name(self, value: str):
        self._device_name = value

    @property
    def mic_rate(self) -> Optional[int]:
        return self._mic_rate

    @mic_rate.setter
    def mic_rate(self, value: int):
        self._mic_rate = value

    @property
    def channels(self) -> Optional[int]:
        return self._channels

    @channels.setter
    def channels(self, value: int):
        self._channels = value

    @property
    def windows_loopback(self) -> Optional[bool]:
        return self._windows_loopback

    @windows_loopback.setter
    def windows_loopback(self, value: bool):
        self._windows_loopback = value

    def to_dict(self) -> dict:
        return {'deviceName': self._device_name,
                'micRate': self._mic_rate,
                'channels': self._channels,
                'windowsLoopback': self._windows_loopback}
