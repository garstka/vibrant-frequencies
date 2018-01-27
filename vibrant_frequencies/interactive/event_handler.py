import pyglet

from ..visuals.visual_set import VisualSet


class EventHandler:
    def __init__(self, visual_set: VisualSet, window):
        self._visual_set = visual_set

        event_handler = self

        @window.event
        def on_key_press(symbol, modifiers):
            import pyglet.window.key as key
            if symbol == key.ESCAPE:
                pyglet.app.exit()
            elif symbol == key.UP:
                if not event_handler._visual_set.empty:
                    event_handler._visual_set.current_visual.scale(times=1.1)
            elif symbol == key.DOWN:
                if not event_handler._visual_set.empty:
                    event_handler._visual_set.current_visual.scale(times=0.9)
            elif symbol == key.LEFT:
                event_handler._visual_set.prev()
            elif symbol == key.RIGHT:
                event_handler._visual_set.next()
            elif symbol == key._0:
                if not event_handler._visual_set.empty:
                    event_handler._visual_set.current_visual.debug()
            else:
                return pyglet.event.EVENT_UNHANDLED
            return pyglet.event.EVENT_HANDLED
