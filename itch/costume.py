import pygame
from itch.pyscratch import Rotate


class Costume:

    def __init__(self, filename):
        self._image = pygame.image.load(filename)
        self.rotation_style = Rotate.all_around
        self.rotate(90)

    def rotate(self, degrees):
        if self.rotation_style == Rotate.all_around:
            self._transformed_image = pygame.transform.rotate(self._image, degrees)
        elif self.rotation_style == Rotate.left_right and degrees < 0:
            self._transformed_image = pygame.transform.flip(self._image, True, False)
        else:
            self._transformed_image = self._image

        self._mask = pygame.mask.from_surface(self._transformed_image)

    @property
    def width(self):
        return self._transformed_image.get_rect().width

    @property
    def height(self):
        return self._transformed_image.get_rect().height

    def bounding_box_at(self, coords):
        return self._transformed_image.get_rect().copy().move(coords)

    def current_image(self):
        return self._transformed_image

    def mask_at(self, coords):
        return self._mask.get_at(coords)