import pygame
from itch.pyscratch import Rotate


class Costume:

    def __init__(self, image_sources):

        self._image_collection = []

        for source in image_sources:
            if isinstance(source, tuple):
                self._image_collection.append((source[0], pygame.image.load(source[1])))
            else:
                self._image_collection.append((None, pygame.image.load(source)))

        self._selected = 0
        self._rotation = 90
        self._image = None
        self._transformed_image = None
        self._mask = None
        self.rotation_style = Rotate.all_around
        self.prepare_image()

    def prepare_image(self):
        self._image = self._image_collection[self._selected][1]
        self.rotate(self._rotation)

    def rotate(self, degrees):
        self._rotation = degrees

        if self.rotation_style == Rotate.all_around:
            self._transformed_image = pygame.transform.rotate(self._image, degrees)
        elif self.rotation_style == Rotate.left_right and degrees < 0:
            self._transformed_image = pygame.transform.flip(self._image, True, False)
        else:
            self._transformed_image = self._image

        self._mask = pygame.mask.from_surface(self._transformed_image)

    def select_named(self, costume_name):
        self._selected = [item[0] for item in self._image_collection].index(costume_name)
        self.prepare_image()

    def next_costume(self):
        self._selected = (self._selected + 1) % len(self._image_collection)
        self.prepare_image()

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