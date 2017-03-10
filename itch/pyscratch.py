import pygame

from itch.sched import Scheduler
import itch.stage
from itch.utils import read_mouse, Rotate

default_scheduler = Scheduler()

stage = itch.stage.Stage(scheduler=default_scheduler)
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
    screen = pygame.display.set_mode((itch.stage.STAGE_WIDTH, itch.stage.STAGE_HEIGHT))
    pygame.display.set_caption("Hello Itch")

    pygame.key.set_repeat(1, 5)

    stage.broadcast("when_green_flag_clicked")

    done = False
    while not done:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                stage.broadcast("mouse_clicked")
            if event.type == pygame.KEYDOWN:
                if (48 <= event.key <= 57) or (97 <= event.key <= 122):
                    stage.broadcast("when_" + chr(event.key) + "_key_pressed")
                if event.key == 32:
                    stage.broadcast("when_space_key_pressed")
                if event.key == 275:
                    stage.broadcast("when_right_arrow_key_pressed")
                if event.key == 276:
                    stage.broadcast("when_left_arrow_key_pressed")
                if event.key == 273:
                    stage.broadcast("when_up_arrow_key_pressed")
                if event.key == 274:
                    stage.broadcast("when_down_arrow_key_pressed")

        stage.run_all_tasks_until_reschedule()

        if not done:
            stage.render_in(screen)

            pygame.display.flip()
            default_scheduler.sync_clock()
        else:
            pygame.quit()

