from itch.stage import Stage
from itch.sched import Scheduler
from itch.utils import read_mouse, Rotate

import pygame

default_scheduler = Scheduler()

stage = Stage(scheduler=default_scheduler)
data = stage.data_container


def create_sprite(x=0, y=0, *image_sources):
    return stage.create_sprite(x, y, *image_sources)


def create_data(name, value):
    return stage.create_data(name, value)


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


def click_green_flag():

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((Stage.STAGE_WIDTH, Stage.STAGE_HEIGHT))
    pygame.display.set_caption("Hello Itch")

    pygame.key.set_repeat(1, 5)

    stage.system_broadcast("when_green_flag_clicked")

    done = False
    while not done:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                stage.system_broadcast("mouse_clicked")
            if event.type == pygame.KEYDOWN:
                if (48 <= event.key <= 57) or (97 <= event.key <= 122):
                    stage.system_broadcast("when_" + chr(event.key) + "_key_pressed")
                if event.key == 32:
                    stage.system_broadcast("when_space_key_pressed")
                if event.key == 275:
                    stage.system_broadcast("when_right_arrow_key_pressed")
                if event.key == 276:
                    stage.system_broadcast("when_left_arrow_key_pressed")
                if event.key == 273:
                    stage.system_broadcast("when_up_arrow_key_pressed")
                if event.key == 274:
                    stage.system_broadcast("when_down_arrow_key_pressed")

        stage.fire_all_events()
        stage.run_all_tasks_until_reschedule()

        if not done:
            stage.render_in(screen)

            pygame.display.flip()
            default_scheduler.sync_clock()
        else:
            pygame.quit()
