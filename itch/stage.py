from itch.costume import Costume
from itch.event_receiver import EventReceiver


class Stage(EventReceiver):

    def __init__(self, *image_sources, scheduler):
        super().__init__(scheduler)
        self._costume = None
        self.load_backdrops(*image_sources)

    def load_backdrops(self, *image_sources):
        self._costume = Costume(image_sources)

    def render_in(self, screen):
        if self._costume.current_image():
            screen.blit(self._costume.current_image(), (0, 0))
