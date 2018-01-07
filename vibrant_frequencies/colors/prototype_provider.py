import random
from math import floor


class PrototypeColorProvider:
    def __init__(self):
        self.__set = [(229 / 255, 244 / 255, 227 / 255),
                      (93 / 255, 169 / 255, 233 / 255),
                      (0 / 255, 63 / 255, 145 / 255),
                      (255 / 255, 255 / 255, 255 / 255),
                      (109 / 255, 50 / 255, 109 / 255)]

    def random(self):
        return random.choice(self.__set)

    def all(self):
        return self.__set
