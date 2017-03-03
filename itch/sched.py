from greenlet import greenlet
import pygame


class Scheduler:

    def __init__(self):
        self._clock = pygame.time.Clock()

    def schedule(self):
        greenlet.getcurrent().parent.switch()

    def wait(self, millis):
        target = pygame.time.get_ticks() + millis
        while target > pygame.time.get_ticks():
            self.schedule()

    def task(self, func, receiver):
        return Task(func, receiver, self)

    def sync_clock(self):
        self._clock.tick(60)

    def fps(self):
        return int(self._clock.get_fps())


class Task:

    def __init__(self, func, receiver, scheduler):
        self.func = func
        self.greenlet = greenlet(self.event_handler)
        self.running = False
        self.receiver = receiver
        self._scheduler = scheduler

    def invoke(self):
        self.running = True

    def run_until_reschedule(self):
        self.greenlet.switch()

    def event_handler(self):
        while True:
            if self.running:
                self.func(self.receiver)

            self.running = False
            self._scheduler.schedule()
