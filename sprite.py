import math
import pygame
from sched import schedule, wait, Task
from utils import scratch_dir_to_degrees, read_mouse, to_real_coord, to_real_coord2


class Sprite:
    def __init__(self, filename, x, y):
        self.x = x
        self.y = y
        self.direction = 90
        self.image = pygame.image.load(filename)
        self.event_handlers = {}
        self.event_tasks = {}

    def queue_event(self, event_name):

        if event_name not in self.event_tasks:
            self.event_tasks[event_name] = Task(self.event_handlers[event_name], self)

        self.event_tasks[event_name].invoke()

    def trigger_event(self, event_name):
        if event_name in self.event_handlers:
            self.queue_event(event_name)

    def change_x_by(self, amount):
        self.x = self.x + amount
        schedule()

    def change_y_by(self, amount):
        self.y = self.y + amount
        schedule()

    def move_steps(self, steps):

        self.x = (math.cos(math.radians(scratch_dir_to_degrees(self.direction))) * steps) + self.x
        self.y = (math.sin(math.radians(scratch_dir_to_degrees(self.direction))) * steps) + self.y

        schedule()

    def if_on_edge_bounce(self):
        if to_real_coord(self.image, (self.x, self.y))[0] + self.image.get_bounding_rect().width > 700 and self.direction == 90:
            self.direction = 270

        if to_real_coord(self.image, (self.x, self.y))[0] <= 0 and self.direction == 270:
            self.direction = 90

        schedule()

    def turn_degrees(self, deg):
        self.direction = (self.direction + deg) % 360
        schedule()

    def turn_clockwise(self, deg):
        self.turn_degrees(deg)
        schedule()

    def turn_anti_clockwise(self, deg):
        self.turn_degrees(-deg)
        schedule()

    def point_in_direction(self, deg):
        self.direction = deg % 360
        schedule()

    def go_to_x_y(self, x, y):
        self.x = x
        self.y = y
        schedule()

    def set_x_to(self, x):
        self.x = x
        schedule()

    def set_y_to(self, y):
        self.y = y
        schedule()

    def point_towards_mouse_pointer(self):
        (mx, my) = read_mouse()

        dx = mx - self.x
        dy = my - self.y

        if dy == 0:
            self.direction = 90
        else:
            self.direction = (int(math.degrees(math.atan(dx/dy))))

        if dy < 0:
            self.direction = 180 + self.direction

        schedule()

    def point_towards(self, other_sprite):
        (mx, my) = (other_sprite.x, other_sprite.y)

        dx = mx - self.x
        dy = my - self.y

        if dy == 0:
            self.direction = 90
        else:
            self.direction = (int(math.degrees(math.atan(dx/dy))))

        if dy < 0:
            self.direction = 180 + self.direction

        schedule()

    def go_to_mouse_pointer(self):
        pos = read_mouse()
        self.x = pos[0]
        self.y = pos[1]
        schedule()

    def wait_secs(self, secs):
        wait(secs*1000)
        schedule()

    def hit_test(self, coords):
        transformed = pygame.transform.rotate(self.image, scratch_dir_to_degrees(self.direction))
        r = transformed.get_rect().copy().move(to_real_coord(transformed, (self.x, self.y)))
        (x, y) = to_real_coord2(coords)
        if r.collidepoint(x, y) != 0:
            mask = pygame.mask.from_surface(transformed)
            return mask.get_at((x - r.x, y - r.y))
        else:
            return False


    def render_in(self, screen):
        transformed = pygame.transform.rotate(self.image, scratch_dir_to_degrees(self.direction))
        # r = transformed.get_rect().copy().move(to_real_coord(transformed, (self.x, self.y)))
        # mask = pygame.mask.from_surface(transformed)
        # pygame.draw.rect(screen, (0,0,0), r, 1)
        # (x, y) = to_real_coord2(read_mouse())
        #
        #
        # olist = mask.outline()
        # pygame.draw.polygon(screen,(200,150,150),olist,0)
        # pygame.draw.line(screen, (0,0,0), (x - r.x, y - r.y), (x - r.x, y - r.y), 2)

        screen.blit(transformed, to_real_coord(transformed, (self.x, self.y)))