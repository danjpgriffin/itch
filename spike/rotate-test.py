import pygame

pygame.init()
screen = pygame.display.set_mode((700, 500))
pygame.display.set_caption("Rotate Test")

done = False
WHITE = (255, 255, 255)

image = pygame.image.load("cat.png")


rot = 0

clock = pygame.time.Clock()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(WHITE)

    pos_org = (300 - image.get_rect().width / 2,
               300 - image.get_rect().height / 2)

    target = pygame.transform.rotate(image, rot) #rotate image

    pos_new = (300 - target.get_rect().width / 2,
               300 - target.get_rect().height / 2)

    rot += 5 % 360
    rect = target.get_rect()
    orig_rect = image.get_rect()
    print(image.get_width())

    screen.blit(target, pos_new)
    pygame.draw.rect(screen, (0, 0, 0), rect, 1)
    pygame.draw.rect(screen, (255, 0, 0), orig_rect, 1)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()