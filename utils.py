import pygame


def scratch_dir_to_degrees(sd):
    norm = sd % 360

    if sd > 180:
        norm -= 360

    if norm <= 0:
        norm = abs(norm)
    else:
        norm = 360 - norm
    return norm + 90


def to_real_coord(coords):

    (x, y) = coords
    cx = int(700/2)
    cy = int(500/2)

    return cx + x, cy - y


def to_scratch_coord(coords):
    (x, y) = coords
    cx = int(700/2)
    cy = int(500/2)

    return x - cx, cy - y


def read_mouse():
    return to_scratch_coord(pygame.mouse.get_pos())

