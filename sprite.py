import math
import pygame
from greenlet import greenlet
from utils import scratch_dir_to_degrees, read_mouse

class Sprite:
    def __init__(self, filename, x, y):
        self.x = x
        self.y = y
        self.direction = 90
        self.image = pygame.image.load(filename)
        self.event_handlers = {}
        self.event_greenlets = {}

    def queue_event(self, event_name):

        if event_name in self.event_greenlets:
            return

        def event_handler():
            self.event_handlers[event_name](self)
            del self.event_greenlets[event_name]

        g = greenlet(event_handler)
        self.event_greenlets[event_name] = g

    def trigger_event(self, event_name):
        if event_name in self.event_handlers:
            self.queue_event(event_name)

    def change_x_by(self, amount):
        self.x = self.x + amount
        greenlet.getcurrent().parent.switch()

    def change_y_by(self, amount):
        self.y = self.y + amount
        greenlet.getcurrent().parent.switch()

    def move_steps(self, steps):

        self.x = (math.cos(math.radians(scratch_dir_to_degrees(self.direction))) * steps) + self.x
        self.y = (math.sin(math.radians(scratch_dir_to_degrees(self.direction))) * steps) + self.y

        greenlet.getcurrent().parent.switch()

    def if_on_edge_bounce(self):
        if self.to_real_coord((self.x, self.y))[0] + self.image.get_bounding_rect().width > 700 and self.direction == 90:
            self.direction = 270

        if self.to_real_coord((self.x, self.y))[0] <= 0 and self.direction == 270:
            self.direction = 90

        greenlet.getcurrent().parent.switch()

    def turn_degrees(self, deg):
        self.direction = (self.direction + deg) % 360
        greenlet.getcurrent().parent.switch()

    def turn_clockwise(self, deg):
        self.turn_degrees(deg)

    def turn_anti_clockwise(self, deg):
        self.turn_degrees(-deg)

    def point_in_direction(self, deg):
        self.direction = deg % 360
        greenlet.getcurrent().parent.switch()

    def go_to_x_y(self, x, y):
        self.x = x
        self.y = y
        greenlet.getcurrent().parent.switch()

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

        greenlet.getcurrent().parent.switch()

    def go_to_mouse_pointer(self):
        pos = read_mouse()
        self.x = pos[0]
        self.y = pos[1]
        greenlet.getcurrent().parent.switch()

    def to_real_coord(self, coords):
        offx = int(self.image.get_bounding_rect().width/2)
        offy = int(self.image.get_bounding_rect().height/2)

        (x, y) = coords
        cx = int(700/2)
        cy = int(500/2)

        return cx + x - offx, cy - y - offy

    def to_real_coord_img(self, image, coords):
        offx = int(image.get_rect().width/2)
        offy = int(image.get_rect().height/2)

        (x, y) = coords
        cx = int(700/2)
        cy = int(500/2)

        return cx + x - offx, cy - y - offy