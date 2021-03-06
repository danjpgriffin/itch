import math

from itch.costume import Costume
import itch
from itch.event_receiver import EventReceiver
from itch.utils import scratch_dir_to_degrees, read_mouse, to_real_coord


class Sprite(EventReceiver):

    class _DirectionDescriptor:

        def __set__(self, obj, val):
            norm = val % 360

            if norm > 180:
                norm -= 360

            setattr(obj, "_priv_direction", norm)
            getattr(obj, "_costume").rotate(scratch_dir_to_degrees(norm))

        def __get__(self, obj, objtype):
            return getattr(obj, "_priv_direction")

    _direction = _DirectionDescriptor()

    def __init__(self, image_sources, x, y, stage, scheduler):
        super().__init__(scheduler)
        self._x = x
        self._y = y
        self._costume = Costume(image_sources)
        self._direction = 90
        self._visible = True
        self._stage = stage

    # Motion methods

    def move_steps(self, steps):
        self._x = round(self._x + self._cos_dir() * steps)
        self._y = round(self._y + self._sin_dir() * steps)
        self._schedule()

    def turn_clockwise(self, deg):
        self._turn_degrees(deg)
        self._schedule()

    def turn_anti_clockwise(self, deg):
        self._turn_degrees(-deg)
        self._schedule()

    def point_in_direction(self, deg):
        self._direction = deg
        self._schedule()

    def point_towards_mouse_pointer(self):
        self._point_towards(read_mouse())

    def point_towards(self, other_sprite):
        self._point_towards((other_sprite.x_position(), other_sprite.y_position()))

    def go_to_x_y(self, x, y):
        self._x = x
        self._y = y
        self._schedule()

    def go_to_mouse_pointer(self):
        pos = read_mouse()
        self._x = pos[0]
        self._y = pos[1]
        self._schedule()

    def glide_secs_to_x_y(self, secs, x, y):
        steps = self._scheduler.fps() * secs
        ox = self._x
        oy = self._y
        dx = (x - ox) / steps
        dy = (y - oy) / steps

        for step in range(1, steps+1):
            self.go_to_x_y(ox + dx * step, oy + dy * step)

    def change_x_by(self, amount):
        self._x = self._x + amount
        self._schedule()

    def set_x_to(self, x):
        self._x = x
        self._schedule()

    def change_y_by(self, amount):
        self._y = self._y + amount
        self._schedule()

    def set_y_to(self, y):
        self._y = y
        self._schedule()

    def if_on_edge_bounce(self):
        (rx, ry) = self._real_coords()

        if rx + self._costume.width > itch.Stage.STAGE_WIDTH:
            self._direction = -self._direction

        if rx <= 0:
            self._direction = -self._direction

        if ry + self._costume.height > itch.Stage.STAGE_HEIGHT:
            self._direction = - self._direction + 180

        if ry <= 0:
            self._direction = - self._direction + 180

        self._schedule()

    def set_rotation_style(self, style):
        self._costume.set_rotation_style(style)
        self._schedule()

    def x_position(self):
        return self._x

    def y_position(self):
        return self._y

    def direction(self):
        return self._direction

    # Looks methods

    def show(self):
        self._visible = True
        self._schedule()

    def hide(self):
        self._visible = False
        self._schedule()

    def switch_costume_to(self, costume_name):
        self._costume.select_named(costume_name)
        self._schedule()

    def next_costume(self):
        self._costume.next_costume()
        self._schedule()

    def go_to_front(self):
        self._stage.bring_to_front(self)

    def go_back_layers(self, number):
        self._stage.send_back_layers(self, number)

    # Events

    def broadcast(self, event_name):
        self._stage.broadcast(event_name)

    # Sensing methods

    def touching_mouse_pointer(self):
        return self._schedule(self.hit_test(read_mouse()))

    def touching_color(self, color):
        mask = self._stage.mask_without_sprite_filtered_by_color(self, color)
        return self._schedule(mask.overlap_area(self._costume.mask, self._real_coords()) > 0)

    def touching_edge(self):
        (rx, ry) = self._real_coords()
        return self._schedule(rx + self._costume.width > itch.Stage.STAGE_WIDTH
                              or rx <= 0
                              or ry + self._costume.height > itch.Stage.STAGE_HEIGHT
                              or ry <= 0)

    # Non-scratch mapped public methods

    def render_in(self, screen):
        if self._visible:
            screen.blit(self._costume.current_image(), self._real_coords())
        # pygame.draw.rect(screen, (0,0,0), self._transformed_image.get_rect().move(self._real_coords()), 1)

    def hit_test(self, coords):
        if not self._visible:
            return False

        r = self._bounding_box()
        (x, y) = to_real_coord(coords)
        if r.collidepoint(x, y) != 0:
            return self._costume.mask_at((x - r.x, y - r.y))
        else:
            return False

    def stop_this_script(self):
        self._scheduler.stop_this_script()

    # Internal methods

    def _sin_dir(self):
        return math.sin(math.radians(scratch_dir_to_degrees(self._direction)))

    def _cos_dir(self):
        return math.cos(math.radians(scratch_dir_to_degrees(self._direction)))

    def _turn_degrees(self, deg):
        self._direction += deg
        self._schedule()

    def _point_towards(self, coords):
        dx = coords[0] - self._x
        dy = coords[1] - self._y

        if dy == 0:
            if dx > 0:
                self._direction = 90
            else:
                self._direction = -90
        else:
            self._direction = (int(math.degrees(math.atan(dx/dy))))

        if dy < 0:
            self._direction += 180

        self._schedule()

    def _bounding_box(self):
        return self._costume.bounding_box_at(self._real_coords())

    def _real_coords(self):
        offx = int(self._costume.width/2)
        offy = int(self._costume.height/2)

        real = to_real_coord((self._x, self._y))

        return real[0] - offx, real[1] - offy
