from itch import *

cat = create_sprite(-150, 100, ("cat-a", "resources/cat.png"), ("cat-b", "resources/cat2.png"))
cat2 = create_sprite(-150, -100, ("cat-a", "resources/cat.png"), ("cat-b", "resources/cat2.png"))
cat.set_rotation_style(Rotate.left_right)
cat2.set_rotation_style(Rotate.left_right)


@on(cat2)
def when_green_flag_clicked(sprite):
    while True:
        sprite.move_steps(10)
        sprite.if_on_edge_bounce()


@on(cat)
def when_green_flag_clicked():
    stage.broadcast("go_running")


@on(cat)
def when_i_receive_go_running():
    while not cat.touching_edge():
        cat.move_steps(10)

    cat.broadcast("hit_edge")


@on(cat)
def when_i_receive_hit_edge():
    cat.turn_clockwise(180)
    cat.move_steps(10)

    cat.broadcast("go_running")


click_green_flag()
