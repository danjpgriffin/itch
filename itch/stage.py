from itch.costume import Costume
from itch.event_receiver import EventReceiver
from itch.sprite import Sprite


class Stage(EventReceiver):

    def __init__(self, *image_sources, scheduler):
        super().__init__(scheduler)
        self._costume = None
        self.load_backdrops(*image_sources)
        self.sprite_list = []

    def load_backdrops(self, *image_sources):
        self._costume = Costume(image_sources)

    def render_in(self, screen):
        if self._costume.current_image():
            screen.blit(self._costume.current_image(), (0, 0))

        for sprite in self.sprite_list:
            sprite.render_in(screen)

    def switch_backdrop_to(self, name):
        self._costume.select_named(name)
        self._schedule()

    def next_backdrop(self):
        self._costume.next_costume()
        self._schedule()

    def receivers(self):
        return [self] + self.sprite_list

    def create_sprite(self, x=0, y=0, *image_sources):
        sprite = Sprite(image_sources, x, y, self._scheduler)
        self.sprite_list.append(sprite)
        return sprite

    def receiver_at(self, coords):
        underneath = list(filter(lambda s: s.hit_test(coords), self.sprite_list))
        if len(underneath) > 0:
            return underneath[-1]
        else:
            return self
