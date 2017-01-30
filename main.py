from pyscratch import *
cat = new_sprite("cat.png", -150, 100)
fish = new_sprite("fish.png", 150, 0)


@script(cat, fish)
def when_left_arrow_key_pressed(sprite):
    sprite.change_x_by(-10)


@script(cat, fish)
def when_right_arrow_key_pressed(sprite):
    sprite.change_x_by(10)


@script(cat, fish)
def when_up_arrow_key_pressed(sprite):
    sprite.change_y_by(10)


@script(cat, fish)
def when_down_arrow_key_pressed(sprite):
    sprite.change_y_by(-10)


@script(fish)
def when_space_key_pressed(sprite):
    sprite.move_steps(10)
    sprite.if_on_edge_bounce()


click_green_flag()
