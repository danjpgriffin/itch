import pygame

from itch.sched import Scheduler
from itch.sprite import Sprite
from itch.stage import Stage
from itch.utils import read_mouse, Rotate

STAGE_WIDTH = 480
STAGE_HEIGHT = 360

default_scheduler = Scheduler()

stage = Stage(scheduler=default_scheduler)


def create_sprite(x=0, y=0, *image_sources):
    return stage.create_sprite(x, y, *image_sources)


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

    for receiver in stage.receivers():
        receiver.trigger_event("when_green_flag_clicked")

    done = False
    while not done:

        for event in pygame.event.get():
            for receiver in stage.receivers():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    under = stage.receiver_at(read_mouse())
                    if isinstance(under, Sprite):
                        under.trigger_event("when_this_sprite_clicked")
                    else:
                        under.trigger_event("when_stage_clicked")

                if event.type == pygame.KEYDOWN:
                    if (48 <= event.key <= 57) or (97 <= event.key <= 122):
                        receiver.trigger_event("when_" + chr(event.key) + "_key_pressed")
                    if event.key == 32:
                        receiver.trigger_event("when_space_key_pressed")
                    if event.key == 275:
                        receiver.trigger_event("when_right_arrow_key_pressed")
                    if event.key == 276:
                        receiver.trigger_event("when_left_arrow_key_pressed")
                    if event.key == 273:
                        receiver.trigger_event("when_up_arrow_key_pressed")
                    if event.key == 274:
                        receiver.trigger_event("when_down_arrow_key_pressed")

        for receiver in stage.receivers():
            receiver.run_tasks_until_reschedule()

        if not done:
            screen.fill(WHITE)
            stage.render_in(screen)

            pygame.display.flip()
            default_scheduler.sync_clock()
        else:
            pygame.quit()

