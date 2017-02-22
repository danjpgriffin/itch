from pyscratch import *
cat = new_sprite("cat.png", -150, 100)
fish = new_sprite("fish.png", 150, 0)
fish2 = new_sprite("fish.png", -150, -100)


@on(cat)
def when_m_key_pressed(sprite):
    sprite.move_steps(10)


@on(cat)
def when_w_key_pressed(sprite):
    for x in range(0, 10):
        sprite.wait_secs(1)
        sprite.move_steps(10)


@on(cat)
def when_m_key_pressed(sprite):
    sprite.go_to_mouse_pointer()


@on(cat)
def when_c_key_pressed(sprite):
    sprite.go_to_x_y(0, 0)


@on(cat)
def when_x_key_pressed(sprite):
    sprite.set_x_to(150)


@on(cat)
def when_y_key_pressed(sprite):
    sprite.set_y_to(0)


@on(cat)
def when_l_key_pressed(sprite):
    sprite.turn_anti_clockwise(10)


@on(cat)
def when_r_key_pressed(sprite):
    sprite.turn_clockwise(10)


@on(cat)
def when_left_arrow_key_pressed(sprite):
    sprite.point_in_direction(-90)
    sprite.change_x_by(-10)


@on(cat)
def when_right_arrow_key_pressed(sprite):
    sprite.point_in_direction(90)
    sprite.change_x_by(10)


@on(cat)
def when_up_arrow_key_pressed(sprite):
    sprite.point_in_direction(0)
    sprite.change_y_by(10)


@on(cat)
def when_down_arrow_key_pressed(sprite):
    sprite.point_in_direction(180)
    sprite.change_y_by(-10)


@on(fish)
def when_space_key_pressed(sprite):
    while True:
        sprite.move_steps(10)
        sprite.if_on_edge_bounce()


@on(fish2)
def when_green_flag_clicked(sprite):
    while True:
        sprite.move_steps(10)
        sprite.if_on_edge_bounce()


@on(cat)
def when_this_sprite_clicked(sprite):
    sprite.change_x_by(50)


@on(fish)
def when_this_sprite_clicked(sprite):
    while True:
        sprite.point_towards(cat)
        sprite.move_steps(2)

click_green_flag()
