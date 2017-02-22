import pygame
from sprite import Sprite
import utils

sprite_list = []


def new_sprite(filename, x=0, y=0):
    sprite = Sprite(filename, x, y)
    sprite_list.append(sprite)
    return sprite


def on(*receivers):
    def decorator(function):
        for receiver in receivers:
            receiver.event_handlers[function.__name__] = function

    return decorator


WHITE = (255, 255, 255)


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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if sprite.hit_test(utils.read_mouse()):
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
            for task in [val for val in sprite.event_tasks.values()]:
                task.run_until_reschedule()

        if not done:
            screen.fill(WHITE)

            for sprite in sprite_list:
                sprite.render_in(screen)


            pygame.display.flip()
            clock.tick(60)
        else:
            pygame.quit()

