import pygame
import math
from greenlet import greenlet

sprite_list = []


def new_sprite(filename, x=0, y=0):
    sprite = Sprite(filename, x, y)
    sprite_list.append(sprite)
    return sprite


def script(*receivers):
    def decorator(function):
        for receiver in receivers:
            receiver.event_handlers[function.__name__] = function

    return decorator


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


def to_scratch_coord(coords):
    (x, y) = coords
    cx = int(700/2)
    cy = int(500/2)

    return x - cx, cy - y


def read_mouse():
    return to_scratch_coord(pygame.mouse.get_pos())


WHITE = (255, 255, 255)


def scratch_dir_to_degrees(sd):
    norm = sd % 360

    if sd > 180:
        norm = norm - 360

    if norm <= 0:
        norm = abs(norm)
    else:
        norm = 360 - norm
    return norm + 90

def click_green_flag():

    pygame.init()
    screen = pygame.display.set_mode((700, 500))
    pygame.display.set_caption("Hello Itch")

    pygame.key.set_repeat(1, 5)
    clock = pygame.time.Clock()

    for sprite in sprite_list:
        sprite.trigger_event("when_green_flag_clicked")

    done = False
    while not done:

        for event in pygame.event.get():
            for sprite in sprite_list:
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    #print(event.key)
                    if 97 <= event.key <= 122:
                        sprite.trigger_event("when_" + chr(event.key) + "_key_pressed")
                    if event.key == 32:
                        sprite.trigger_event("when_space_key_pressed")
                    if event.key == 275:
                        sprite.trigger_event("when_right_arrow_key_pressed")
                    if event.key == 276:
                        sprite.trigger_event("when_left_arrow_key_pressed")
                    if event.key == 273:
                        sprite.trigger_event("when_up_arrow_key_pressed")
                    if event.key == 274:
                        sprite.trigger_event("when_down_arrow_key_pressed")

        for sprite in sprite_list:
            for g in [v for v in sprite.event_greenlets.values()]:
                g.switch()

        if not done:
            screen.fill(WHITE)

            for sprite in sprite_list:

                transformed = pygame.transform.rotate(sprite.image, scratch_dir_to_degrees(sprite.direction))

                screen.blit(transformed, sprite.to_real_coord_img(transformed, (sprite.x, sprite.y)))

            pygame.display.flip()
            clock.tick(60)
        else:
            pygame.quit()

