from pyscratch import *
cat = new_sprite("cat.png", -150, 100)
fish = new_sprite("fish.png", 150, 0)
fish2 = new_sprite("fish.png", -150, -100)

@script(cat)
def when_m_key_pressed(sprite):
    sprite.move_steps(10)

@script(cat)
def when_x_key_pressed(sprite):
    sprite.go_to_mouse_pointer()

@script(cat)
def when_l_key_pressed(sprite):
    sprite.turn_anti_clockwise(10)

@script(cat)
def when_r_key_pressed(sprite):
    sprite.turn_clockwise(10)


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


@script(fish)
def when_space_key_pressed(sprite):
    while True:
        sprite.move_steps(10)
        sprite.if_on_edge_bounce()

@script(fish2)
def when_green_flag_clicked(sprite):
    while True:
        sprite.move_steps(10)
        sprite.if_on_edge_bounce()

@script(cat)
def when_green_flag_clicked(sprite):
    while True:
        sprite.point_towards_mouse_pointer()
        sprite.move_steps(10)

click_green_flag()
