import pygame

print("Hello World")
pygame.init()
screen = pygame.display.set_mode((700,500))
pygame.display.set_caption("Hello World")

pygame.key.set_repeat(1, 5)

WHITE = (255, 255, 255)

done = False
clock = pygame.time.Clock()

cat = pygame.image.load("cat.png")
catw = cat.get_bounding_rect().width
cath = cat.get_bounding_rect().height
catmx = int(catw/2)
catmy = int(cath/2)

def to_real_coord(coords, offx, offy):
    (x, y) = coords
    cx = int(700/2)
    cy = int(500/2)

    return (cx + x - offx, cy + y - offy)

def to_scratch_coord(coords):
    (x, y) = coords
    cx = int(700/2)
    cy = int(500/2)

    return (x - cx, y - cy)

def read_mouse():
    return to_scratch_coord(pygame.mouse.get_pos())

x = 0
y = 0

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            #print(event.key)
            if event.key == 275:
                x = x + 10
            if event.key == 276:
                x = x - 10
            if event.key == 273:
                y = y - 10
            if event.key == 274:
                y = y + 10

    screen.fill(WHITE)

    #player_position = read_mouse()

    screen.blit(cat, to_real_coord([x,y], catmx, catmy))
    pygame.display.flip()
    clock.tick(60)

