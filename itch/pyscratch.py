import pygame
from itch.utils import read_mouse, Rotate
from itch.sched import Scheduler
from itch.sprite import Sprite

STAGE_WIDTH = 700
STAGE_HEIGHT = 500

default_scheduler = Scheduler()

sprite_list = []


def new_sprite(filename, x=0, y=0, scheduler=default_scheduler):
    sprite = Sprite(filename, x, y, scheduler)
    sprite_list.append(sprite)
    return sprite


def on(*receivers):
    def decorator(function):
        for receiver in receivers:
            receiver.register(function)

    return decorator


def wait_secs(secs):
    default_scheduler.wait(secs*1000)
    default_scheduler.schedule()


def mouse_x():
    return read_mouse()[0]


def mouse_y():
    return read_mouse()[1]


WHITE = (255, 255, 255)


def click_green_flag():

    pygame.init()
    screen = pygame.display.set_mode((STAGE_WIDTH, STAGE_HEIGHT))
    pygame.display.set_caption("Hello Itch")

    pygame.key.set_repeat(1, 5)

    for sprite in sprite_list:
        sprite.trigger_event("when_green_flag_clicked")

    done = False
    while not done:

        for event in pygame.event.get():
            for sprite in sprite_list:
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if sprite.hit_test(read_mouse()):
                        sprite.trigger_event("when_this_sprite_clicked")

                if event.type == pygame.KEYDOWN:
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
            sprite.run_tasks_until_reschedule()

        if not done:
            screen.fill(WHITE)

            for sprite in sprite_list:
                sprite.render_in(screen)

            pygame.display.flip()
            default_scheduler.sync_clock()
        else:
            pygame.quit()

