from itch.pyscratch import *
cat = create_sprite(-150, 100, ("cat-a", "resources/cat.png"), ("cat-b", "resources/cat2.png"))
fish = create_sprite(150, 0, "resources/fish.png")
fish2 = create_sprite(-150, -100, "resources/fish.png")

cat2 = create_sprite(150, 100, ("cat-a", "resources/cat.png"), ("cat-b", "resources/cat2.png"))
stage.load_backdrops(("party", "resources/party.png"), ("sea", "resources/underwater1.png"))


@on(stage)
def when_stage_clicked():
    stage.next_backdrop()


@on(stage)
def when_0_key_pressed():
    stage.switch_backdrop_to("party")


@on(stage)
def when_9_key_pressed():
    stage.switch_backdrop_to("sea")


@on(cat2)
def when_o_key_pressed(sprite):
    sprite.switch_costume_to("cat-a")


@on(cat2)
def when_p_key_pressed(sprite):
    sprite.switch_costume_to("cat-b")


@on(cat2)
def when_g_key_pressed(sprite):
    sprite.glide_secs_to_x_y(1, mouse_x(), mouse_y())


@on(cat2)
def when_s_key_pressed(sprite):
    sprite.show()


@on(cat2)
def when_h_key_pressed(sprite):
    sprite.hide()


@on(cat2)
def when_this_sprite_clicked(sprite):
    print("Hello")


@on(cat)
def when_f_key_pressed(sprite):
    sprite.move_steps(10)
    sprite.next_costume()
    sprite.if_on_edge_bounce()


@on(cat)
def when_b_key_pressed(sprite):
    sprite.move_steps(-10)
    sprite.if_on_edge_bounce()


@on(cat)
def when_k_key_pressed(sprite):
    sprite.set_rotation_style(Rotate.all_around)


@on(cat)
def when_j_key_pressed(sprite):
    sprite.set_rotation_style(Rotate.left_right)


@on(cat)
def when_w_key_pressed(sprite):
    for x in range(0, 10):
        wait_secs(1)
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
def when_y_key_pressed(sprite):
        sprite.move_steps(10)
        sprite.if_on_edge_bounce()


@on(fish)
def when_space_key_pressed(sprite):
    while True:
        sprite.move_steps(10)
        sprite.if_on_edge_bounce()


# @on(fish2)
def when_green_flag_clicked(sprite):
    while True:
        sprite.move_steps(10)
        sprite.if_on_edge_bounce()


@on(cat)
def when_green_flag_clicked(sprite):

    # cat.set_rotation_style(Rotate.left_right)
    fish2.set_rotation_style(Rotate.left_right)

    fish2.point_in_direction(20)

    while True:
        if sprite.touching_mouse_pointer():
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
