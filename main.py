from pyscratch import *
cat = new_sprite("cat.png", -150, 100)
fish = new_sprite("fish.png", 150, 0)
fish2 = new_sprite("fish.png", -150, 0)


@script(cat)
def when_r_key_pressed(sprite):
    sprite.turn_degrees(10)


@script(cat)
def when_left_arrow_key_pressed(sprite):
    sprite.point_in_direction(-90)
    sprite.change_x_by(-10)


@script(cat)
def when_right_arrow_key_pressed(sprite):
    sprite.point_in_direction(90)
    sprite.change_x_by(10)


@script(cat)
def when_up_arrow_key_pressed(sprite):
    sprite.point_in_direction(0)
    sprite.change_y_by(10)


@script(cat)
def when_down_arrow_key_pressed(sprite):
    sprite.point_in_direction(180)
    sprite.change_y_by(-10)


@script(fish, fish2)
def when_space_key_pressed(sprite):
    while True:
        sprite.move_steps(10)
        sprite.if_on_edge_bounce()


click_green_flag()
