import unittest
from itch.pyscratch import new_sprite


class NoScheduler:
    def schedule(self):
        pass

    def wait(self, millis):
        pass

    def task(self, func, receiver):
        pass


class SpriteTestCase(unittest.TestCase):

    def test_direction_corresponds_to_scratch(self):

        unit = new_sprite("../resources/cat.png", -150, 100, NoScheduler())
        self.assertEquals(unit.direction(), 90)

        unit.point_in_direction(0)
        self.assertEquals(unit.direction(), 0)
