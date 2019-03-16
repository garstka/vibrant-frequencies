import json

from vibrant_frequencies.config.config import Config


def save_config(config: Config,
                file: str):
    with open(file, 'w') as file:
        json.dump(config.to_dict(), file, sort_keys=True, indent=4)


def load_config(file: str) -> Config:
    with open(file, 'r') as f:
        return Config(source=json.load(f))
