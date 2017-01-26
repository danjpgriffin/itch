from pyscratch import *
cat = new_sprite()


@script(cat)
def when_left_arrow_key_pressed(sprite):
    sprite.change_x_by(-10)


@script(cat)
def when_right_arrow_key_pressed(sprite):
    sprite.change_x_by(10)


@script(cat)
def when_up_arrow_key_pressed(sprite):
    sprite.change_y_by(-10)


@script(cat)
def when_down_arrow_key_pressed(sprite):
    sprite.change_y_by(10)


click_green_flag()
