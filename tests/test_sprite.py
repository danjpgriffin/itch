import unittest
from itch.stage import Stage


class NoScheduler:
    def schedule(self):
        pass

    def wait(self, millis):
        pass

    def task(self, func, receiver):
        pass


class SpriteTestCase(unittest.TestCase):

    def test_direction_corresponds_to_scratch(self):

        unit = Stage(scheduler=NoScheduler()).create_sprite(-150, 100, "resources/cat.png")

        self.assertEquals(unit.direction(), 90)

        unit.point_in_direction(0)
        self.assertEquals(unit.direction(), 0)

        unit.point_in_direction(-90)
        self.assertEquals(unit.direction(), -90)

        unit.point_in_direction(180)
        self.assertEquals(unit.direction(), 180)

    def test_rotation_around_limits(self):

        unit = Stage(scheduler=NoScheduler()).create_sprite(-150, 100, "resources/cat.png")

        unit.point_in_direction(0)
        unit.turn_anti_clockwise(1)
        self.assertEquals(unit.direction(), -1)

        unit.point_in_direction(0)
        unit.turn_clockwise(1)
        self.assertEquals(unit.direction(), 1)

        unit.point_in_direction(90)
        unit.turn_anti_clockwise(1)
        self.assertEquals(unit.direction(), 89)

        unit.point_in_direction(90)
        unit.turn_clockwise(1)
        self.assertEquals(unit.direction(), 91)

        unit.point_in_direction(180)
        unit.turn_anti_clockwise(1)
        self.assertEquals(unit.direction(), 179)

        unit.point_in_direction(180)
        print(unit.direction())
        unit.turn_clockwise(1)
        self.assertEquals(unit.direction(), -179)

        unit.point_in_direction(-90)
        unit.turn_anti_clockwise(1)
        self.assertEquals(unit.direction(), -91)

        unit.point_in_direction(-90)
        print(unit.direction())
        unit.turn_clockwise(1)
        self.assertEquals(unit.direction(), -89)

