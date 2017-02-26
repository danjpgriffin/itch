from greenlet import greenlet
import pygame


def schedule():
    greenlet.getcurrent().parent.switch()


def wait(millis):
    target = pygame.time.get_ticks() + millis
    while target > pygame.time.get_ticks():
        schedule()


def wait_secs(secs):
    wait(secs*1000)
    schedule()


class Task:

    def __init__(self, func, receiver):
        self.func = func
        self.greenlet = greenlet(self.event_handler)
        self.greenlet.itch_task = self
        self.running = False
        self.receiver = receiver

    def invoke(self):
        self.running = True

    def run_until_reschedule(self):
        self.greenlet.switch()

    def event_handler(self):
        while True:
            if self.running:
                self.func(self.receiver)

            self.running = False
            schedule()
