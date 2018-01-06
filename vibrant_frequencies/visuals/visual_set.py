import logging


class VisualSet:
    def __init__(self, visuals, dim_reduction=None):
        self._visuals = visuals
        self._current_visual = 0
        self._dim_reduction = dim_reduction
        self._warned = False
        self._log = logging.getLogger(__name__)
        self._activate_visual = True

    def apply(self, y_set, dt):
        if not self._visuals:
            return

        visual = self._visuals[self._current_visual]

        if self._activate_visual:
            self._activate_visual = False
            visual.activate();

        if visual.dimensions == 1:
            if self._dim_reduction is None:
                if not self._warned:
                    self._log.warning("No reduction function provided - cannot "
                                      "display 1d visual.")
                    self._warned = True
            else:
                visual.apply(y=self._dim_reduction(y_set), dt=dt)
        elif visual.dimensions == 2:
            visual.apply(y_set=y_set, dt=dt)

    @property
    def empty(self):
        return len(self._visuals) == 0

    @property
    def current_visual(self):
        if not self._visuals:
            return None
        return self._visuals[self._current_visual]

    def prev(self):
        if not self._visuals:
            return
        self._activate_visual = True
        self._current_visual -= 1
        self._current_visual %= len(self._visuals)
        self._warned = False

    def next(self):
        if not self._visuals:
            return
        self._activate_visual = True
        self._current_visual += 1
        self._current_visual %= len(self._visuals)
        self._warned = False
