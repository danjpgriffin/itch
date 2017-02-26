import math
import pygame
from sched import schedule, Task
from utils import scratch_dir_to_degrees, read_mouse, to_real_coord


class Sprite:

    class _DirectionDescriptor:

        def __set__(self, obj, val):
            setattr(obj, "_priv_direction", val)
            obj._transformed_image = pygame.transform.rotate(obj.image, scratch_dir_to_degrees(val))
            obj._mask = pygame.mask.from_surface(obj._transformed_image)

        def __get__(self, obj, objtype):
            return getattr(obj, "_priv_direction")

    direction = _DirectionDescriptor()

    def __init__(self, filename, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load(filename)
        self.direction = 90
        self.event_handlers = {}
        self.event_tasks = {}

    # Motion methods

    def move_steps(self, steps):
        self.x += self._cos_dir() * steps
        self.y += (self._sin_dir() * steps)
        schedule()

    def turn_clockwise(self, deg):
        self._turn_degrees(deg)
        schedule()

    def turn_anti_clockwise(self, deg):
        self._turn_degrees(-deg)
        schedule()

    def point_in_direction(self, deg):
        self.direction = deg % 360
        schedule()

    def point_towards_mouse_pointer(self):
        self._point_towards(read_mouse())

    def point_towards(self, other_sprite):
        self._point_towards((other_sprite.x, other_sprite.y))

    def go_to_x_y(self, x, y):
        self.x = x
        self.y = y
        schedule()

    def go_to_mouse_pointer(self):
        pos = read_mouse()
        self.x = pos[0]
        self.y = pos[1]
        schedule()

    # Missing Glide

    def change_x_by(self, amount):
        self.x = self.x + amount
        schedule()

    def set_x_to(self, x):
        self.x = x
        schedule()

    def change_y_by(self, amount):
        self.y = self.y + amount
        schedule()

    def set_y_to(self, y):
        self.y = y
        schedule()

    # Better implementation required
    def if_on_edge_bounce(self):
        if self._real_coords()[0] + self.image.get_bounding_rect().width > 700 and self.direction == 90:
            self.direction = 270

        if self._real_coords()[0] <= 0 and self.direction == 270:
            self.direction = 90

        schedule()

    # Set rotation style required

    def x_position(self):
        return self.x

    def y_position(self):
        return self.y

    # Expose direction cleanly

    # Sensing methods

    def touching_mouse_pointer(self):
        answer = self.hit_test(read_mouse())
        schedule()
        return answer

    # Non-scratch mapped public methods

    def render_in(self, screen):
        screen.blit(self._transformed_image, self._real_coords())

    def trigger_event(self, event_name):
        if event_name in self.event_handlers:
            self._queue_event(event_name)

    def hit_test(self, coords):
        r = self._bounding_box()
        (x, y) = to_real_coord(coords)
        if r.collidepoint(x, y) != 0:
            return self._mask.get_at((x - r.x, y - r.y))
        else:
            return False

    # Internal methods

    def _sin_dir(self):
        return math.sin(math.radians(scratch_dir_to_degrees(self.direction)))

    def _cos_dir(self):
        return math.cos(math.radians(scratch_dir_to_degrees(self.direction)))

    def _turn_degrees(self, deg):
        self.direction = (self.direction + deg) % 360
        schedule()

    def _queue_event(self, event_name):

        if event_name not in self.event_tasks:
            self.event_tasks[event_name] = Task(self.event_handlers[event_name], self)

        self.event_tasks[event_name].invoke()

    def _point_towards(self, coords):
        dx = coords[0] - self.x
        dy = coords[1] - self.y

        if dy == 0:
            self.direction = 90
        else:
            self.direction = (int(math.degrees(math.atan(dx/dy))))

        if dy < 0:
            self.direction += 180

        schedule()

    def _bounding_box(self):
        return self._transformed_image.get_rect().copy().move(self._real_coords())

    def _real_coords(self):
        offx = int(self._transformed_image.get_rect().width/2)
        offy = int(self._transformed_image.get_rect().height/2)

        real = to_real_coord((self.x, self.y))

        return real[0] - offx, real[1] - offy
