import colorsys
from math import pi


def rgb_to_pygame(color):
    r, g, b = color
    return int(255 * r), int(255 * g), int(255 * b)


def rgb_rotate(color, rad):
    r, g, b = color
    h, l, s = colorsys.rgb_to_hls(r, g, b)

    h_rad = h * 2 * pi + rad

    while h_rad < 0:
        h_rad += 2 * pi
    while h_rad > 2 * pi:
        h_rad -= 2 * pi

    h = max(0.0, min(1.0, h_rad / (2 * pi)))

    return colorsys.hls_to_rgb(h, l, s)
