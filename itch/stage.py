import itch.costume
from itch.event_receiver import EventReceiver
import itch.sprite
import pygame

STAGE_WIDTH = 480
STAGE_HEIGHT = 360


class Stage(EventReceiver):

    WHITE = (255, 255, 255)

    def __init__(self, *image_sources, scheduler):
        super().__init__(scheduler)
        self._costume = None
        self.load_backdrops(*image_sources)
        self.sprite_list = []

    def load_backdrops(self, *image_sources):
        self._costume = itch.costume.Costume(image_sources)

    def render_in(self, screen):
        screen.fill(Stage.WHITE)
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
        sprite = itch.sprite.Sprite(image_sources, x, y, self, self._scheduler)
        self.sprite_list.append(sprite)
        return sprite

    def receiver_at(self, coords):
        underneath = list(filter(lambda s: s.hit_test(coords), self.sprite_list))
        if len(underneath) > 0:
            return underneath[-1]
        else:
            return self

    def bring_to_front(self, sprite):
        self.sprite_list.remove(sprite)
        self.sprite_list.append(sprite)
        self._schedule()

    def send_back_layers(self, sprite, number):
        current = self.sprite_list.index(sprite)
        new_pos = max(0, current - number)
        self.sprite_list.remove(sprite)
        self.sprite_list.insert(new_pos, sprite)
        self._schedule()

    def mask_without_sprite_filtered_by_color(self, no_render_sprite, color):
        target = (0, 0, 0, 255)
        threshold = (8, 8, 8, 0)

        render_surface = pygame.Surface((itch.stage.STAGE_WIDTH, itch.stage.STAGE_HEIGHT), pygame.SRCALPHA)
        threshold_surface = pygame.Surface((itch.stage.STAGE_WIDTH, itch.stage.STAGE_HEIGHT), pygame.SRCALPHA)

        if self._costume.current_image():
            render_surface.blit(self._costume.current_image(), (0, 0))

        for sprite in self.sprite_list:
            if sprite != no_render_sprite:
                sprite.render_in(render_surface)

        pygame.transform.threshold(threshold_surface, render_surface, list(color) + [0], threshold, target, True)
        mask = pygame.mask.from_surface(threshold_surface)
        mask.invert()

        return mask
