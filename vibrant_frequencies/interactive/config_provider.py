from ..config.all import Config
import sounddevice


class InteractiveConfigProvider:
    def __init__(self):

        self.__config = Config()

        if self.config.file_exists():
            if input("Enter to use existing config : ") == '':
                self.__config.load()
                return

        print("===============================")
        print("Devices: ")
        print(sounddevice.query_devices())

        while True:
            device_id = int(input("Which device to use? : "))
            info = sounddevice.query_devices(int(device_id))
            print(info)

            if input("Press enter to use this device: ") != '':
                continue

            self.__config.sound.device_name = info['name']
            self.__config.sound.mic_rate = int(info['default_samplerate'])

            if info['max_input_channels'] == 0:
                print("This doesn't seem to be an input device.")
                # continue

            self.__config.sound.channels = 1  # info['max_input_channels']

            if self.__config.sound.mic_rate < 48000:
                if input(("Press enter to use a higher"
                          " mic rate than default (recommended): ")) == '':
                    self.__config.sound.mic_rate = 48000

            break

        self.__config.save()

    @property
    def config(self):
        return self.__config
