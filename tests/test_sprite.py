import unittest
from itch.stage import Stage
import itch.utils


class NoScheduler:
    def schedule(self):
        pass

    def wait(self, millis):
        pass

    def task(self, func, receiver):
        pass


class SpriteTestCase(unittest.TestCase):

    def test_direction_corresponds_to_scratch(self):

        unit = Stage(scheduler=NoScheduler()).create_sprite(-150, 100, "../resources/cat.png")

        self.assertEquals(unit.direction(), 90)

        unit.point_in_direction(0)
        self.assertEquals(unit.direction(), 0)

        unit.point_in_direction(-90)
        self.assertEquals(unit.direction(), -90)

        unit.point_in_direction(180)
        self.assertEquals(unit.direction(), 180)

    def test_rotation_around_limits(self):

        unit = Stage(scheduler=NoScheduler()).create_sprite(-150, 100, "../resources/cat.png")

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
        unit.turn_clockwise(1)
        self.assertEquals(unit.direction(), -179)

        unit.point_in_direction(-90)
        unit.turn_anti_clockwise(1)
        self.assertEquals(unit.direction(), -91)

        unit.point_in_direction(-90)
        unit.turn_clockwise(1)
        self.assertEquals(unit.direction(), -89)

    def test_conversion_of_scratch_direction_to_real_direction(self):

        unit = Stage(scheduler=NoScheduler()).create_sprite(-150, 100, "../resources/cat.png")
        self.assertEquals(90, itch.utils.scratch_dir_to_degrees(0))
        self.assertEquals(89, itch.utils.scratch_dir_to_degrees(1))
        self.assertEquals(1, itch.utils.scratch_dir_to_degrees(89))
        self.assertEquals(0, itch.utils.scratch_dir_to_degrees(90))
        self.assertEquals(359, itch.utils.scratch_dir_to_degrees(91))
        self.assertEquals(271, itch.utils.scratch_dir_to_degrees(179))
        self.assertEquals(270, itch.utils.scratch_dir_to_degrees(180))
        self.assertEquals(270, itch.utils.scratch_dir_to_degrees(-180))
        self.assertEquals(269, itch.utils.scratch_dir_to_degrees(-179))
        self.assertEquals(181, itch.utils.scratch_dir_to_degrees(-91))
        self.assertEquals(180, itch.utils.scratch_dir_to_degrees(-90))
        self.assertEquals(179, itch.utils.scratch_dir_to_degrees(-89))
        self.assertEquals(91, itch.utils.scratch_dir_to_degrees(-1))
