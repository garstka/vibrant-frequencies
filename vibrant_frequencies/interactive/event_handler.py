import pygame

from ..visuals.visual_set import VisualSet


class EventHandler:
    def __init__(self, visual_set: VisualSet):
        self._should_quit = False
        self._visual_set = visual_set

    def poll(self):
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            self._should_quit = True
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                self._should_quit = True
            elif ev.key == pygame.K_UP:
                if not self._visual_set.empty:
                    self._visual_set.current_visual.scale(times=1.1)
            elif ev.key == pygame.K_DOWN:
                if not self._visual_set.empty:
                    self._visual_set.current_visual.scale(times=0.9)
            elif ev.key == pygame.K_LEFT:
                self._visual_set.prev()
            elif ev.key == pygame.K_RIGHT:
                self._visual_set.next()
            elif ev.key == pygame.K_0:
                if not self._visual_set.empty:
                    self._visual_set.current_visual.debug()

    @property
    def should_quit(self):
        return self._should_quit
