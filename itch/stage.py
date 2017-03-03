from itch.costume import Costume


class Stage:

    def __init__(self, *image_sources):
        self._costume = None
        self.load_backdrops(*image_sources)

    def load_backdrops(self, *image_sources):
        self._costume = Costume(image_sources)

    def render_in(self, screen):
        if self._costume.current_image():
            screen.blit(self._costume.current_image(), (0, 0))
