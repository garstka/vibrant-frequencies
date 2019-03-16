from vibrant_frequencies.visuals.band import Band
from vibrant_frequencies.visuals.proto_circles import AnimatedProtoCircles
from vibrant_frequencies.device.video import VideoDevice


class Combo:
    dimensions = 2

    def __init__(self, config, video: VideoDevice, colors,
                 dim_reduction):
        self._screen = video.screen
        self._colors = colors
        self._dim_reduction = dim_reduction

        self._circles = AnimatedProtoCircles(colors=colors,
                                             video=video,
                                             config=config)
        self._band = Band(colors=colors,
                          video=video,
                          config=config,
                          rotation=True,
                          symmetry=True,
                          double_symmetry=True,
                          double_rotation=True,
                          no_clear_at_begin=True,
                          no_random_colors=True)
        self._band.scale(3.0)

    def activate(self):
        self._circles.activate()

    def apply(self, y_set, dt):
        self._circles.apply(self._dim_reduction(y_set), dt)
        self._band.apply(y_set, dt)

    def scale(self, times: float):
        self._circles.scale(times)
        self._band.scale(times)
