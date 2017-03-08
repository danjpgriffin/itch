from itch.event_receiver import EventReceiver
import pygame


class DataView(EventReceiver):

    GREY = (193, 196, 199)
    WHITE = (255, 255, 255)
    ORANGE = (238, 125, 22)
    BLACK = (0, 0, 0)

    def __init__(self, x, y, name, data_container, scheduler):
        super().__init__(scheduler)
        self.x = x
        self.y = y
        self.name = name
        self.data_container = data_container

    def render_in(self, screen):
        font = pygame.font.SysFont("Arial", 26, True)
        val = str(getattr(self.data_container, self.name))
        img = font.render(self.name + ": " + val, True, DataView.BLACK)
        r = pygame.Rect(self.x, self.y, img.get_rect().width, img.get_rect().height)
        pygame.draw.rect(screen, DataView.GREY, r, 0)
        screen.blit(img, (self.x, self.y))