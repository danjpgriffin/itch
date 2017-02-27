import math

import pygame
from itch import pyscratch
from itch.utils import scratch_dir_to_degrees, read_mouse, to_real_coord, Rotate

from itch.sched import schedule, Task


class Sprite:

    class _DirectionDescriptor:

        def __set__(self, obj, val):
            setattr(obj, "_priv_direction", val)
            print(val)
            if obj._rotation_style == Rotate.all_around:
                obj._transformed_image = pygame.transform.rotate(obj._image, scratch_dir_to_degrees(val))
            elif obj._rotation_style == Rotate.left_right and val < 0:
                obj._transformed_image = pygame.transform.flip(obj._image, True, False)
            else:
                obj._transformed_image = obj._image

            obj._mask = pygame.mask.from_surface(obj._transformed_image)

        def __get__(self, obj, objtype):
            return getattr(obj, "_priv_direction")

    _direction = _DirectionDescriptor()

    def __init__(self, filename, x, y):
        self._x = x
        self._y = y
        self._event_handlers = {}
        self._event_tasks = {}
        self._rotation_style = pyscratch.Rotate.all_around
        self._image = pygame.image.load(filename)
        self._direction = 90

    # Motion methods

    def move_steps(self, steps):
        self._x += self._cos_dir() * steps
        self._y += (self._sin_dir() * steps)
        schedule()

    def turn_clockwise(self, deg):
        self._turn_degrees(deg)
        schedule()

    def turn_anti_clockwise(self, deg):
        self._turn_degrees(-deg)
        schedule()

    def point_in_direction(self, deg):
        self._direction = deg % 360
        schedule()

    def point_towards_mouse_pointer(self):
        self._point_towards(read_mouse())

    def point_towards(self, other_sprite):
        self._point_towards((other_sprite.x_position(), other_sprite.y_position()))

    def go_to_x_y(self, x, y):
        self._x = x
        self._y = y
        schedule()

    def go_to_mouse_pointer(self):
        pos = read_mouse()
        self._x = pos[0]
        self._y = pos[1]
        schedule()

    # Missing Glide

    def change_x_by(self, amount):
        self._x = self._x + amount
        schedule()

    def set_x_to(self, x):
        self._x = x
        schedule()

    def change_y_by(self, amount):
        self._y = self._y + amount
        schedule()

    def set_y_to(self, y):
        self._y = y
        schedule()

    # Better implementation required
    def if_on_edge_bounce(self):
        if self._real_coords()[0] + self._image.get_bounding_rect().width > 700 and self._direction == 90:
            self._direction = -90

        if self._real_coords()[0] <= 0 and self._direction == -90:
            self._direction = 90

        schedule()

    # Set rotation style required
    def set_rotation_style(self, style):
        self._rotation_style = style

    def x_position(self):
        return self._x

    def y_position(self):
        return self._y

    # Expose direction cleanly

    # Sensing methods

    def touching_mouse_pointer(self):
        answer = self.hit_test(read_mouse())
        schedule()
        return answer

    # Non-scratch mapped public methods

    def render_in(self, screen):
        screen.blit(self._transformed_image, self._real_coords())

    def register(self, function):
        self._event_handlers[function.__name__] = function

    def trigger_event(self, event_name):
        if event_name in self._event_handlers:
            self._queue_event(event_name)

    def run_tasks_until_reschedule(self):
        for task in [val for val in self._event_tasks.values()]:
            task.run_until_reschedule()

    def hit_test(self, coords):
        r = self._bounding_box()
        (x, y) = to_real_coord(coords)
        if r.collidepoint(x, y) != 0:
            return self._mask.get_at((x - r.x, y - r.y))
        else:
            return False

    # Internal methods

    def _sin_dir(self):
        return math.sin(math.radians(scratch_dir_to_degrees(self._direction)))

    def _cos_dir(self):
        return math.cos(math.radians(scratch_dir_to_degrees(self._direction)))

    def _turn_degrees(self, deg):
        self._direction = (self._direction + deg) % 360
        schedule()

    def _queue_event(self, event_name):

        if event_name not in self._event_tasks:
            self._event_tasks[event_name] = Task(self._event_handlers[event_name], self)

        self._event_tasks[event_name].invoke()

    def _point_towards(self, coords):
        dx = coords[0] - self._x
        dy = coords[1] - self._y

        if dy == 0:
            self._direction = 90
        else:
            self._direction = (int(math.degrees(math.atan(dx/dy))))

        if dy < 0:
            self._direction += 180

        schedule()

    def _bounding_box(self):
        return self._transformed_image.get_rect().copy().move(self._real_coords())

    def _real_coords(self):
        offx = int(self._transformed_image.get_rect().width/2)
        offy = int(self._transformed_image.get_rect().height/2)

        real = to_real_coord((self._x, self._y))

        return real[0] - offx, real[1] - offy