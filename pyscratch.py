import pygame
import builtins


def script(receiver):
    def decorator(function):
        receiver.event_handlers[function.__name__] = function

    return decorator

builtins.script = script


class Sprite:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = pygame.image.load("cat.png")
        self.centre_x = int(self.image.get_bounding_rect().width/2)
        self.centre_y = int(self.image.get_bounding_rect().height/2)
        self.event_handlers = {}

    def change_x_by(self, amount):
        self.x = self.x + amount

    def change_y_by(self, amount):
        self.y = self.y + amount

builtins.Sprite = Sprite

pygame.init()
screen = pygame.display.set_mode((700,500))
pygame.display.set_caption("Hello World")

pygame.key.set_repeat(1, 5)

WHITE = (255, 255, 255)

done = False
clock = pygame.time.Clock()


def to_real_coord(coords, offx, offy):
    (x, y) = coords
    cx = int(700/2)
    cy = int(500/2)

    return cx + x - offx, cy + y - offy


def to_scratch_coord(coords):
    (x, y) = coords
    cx = int(700/2)
    cy = int(500/2)

    return x - cx, y - cy


def read_mouse():
    return to_scratch_coord(pygame.mouse.get_pos())

from main import cat


while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == 275:
                cat.event_handlers["when_right_arrow_key_pressed"](cat)

            if event.key == 276:
                cat.event_handlers["when_left_arrow_key_pressed"](cat)
            if event.key == 273:
                cat.event_handlers["when_up_arrow_key_pressed"](cat)
            if event.key == 274:
                cat.event_handlers["when_down_arrow_key_pressed"](cat)

    screen.fill(WHITE)

    # player_position = read_mouse()

    screen.blit(cat.image, to_real_coord([cat.x, cat.y], cat.centre_x, cat.centre_y))
    pygame.display.flip()
    clock.tick(60)
