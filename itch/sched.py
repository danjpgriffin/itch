from greenlet import greenlet
import pygame
import inspect


class Scheduler:

    def __init__(self):
        self._clock = pygame.time.Clock()

    def schedule(self):
        parent = greenlet.getcurrent().parent
        if parent:
            parent.switch()

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

    def stop_this_script(self):
        raise StopThisScriptException


class Task:

    def __init__(self, func, receiver, scheduler):
        self.func = func
        self.send_receiver = len(inspect.signature(self.func).parameters) == 1
        self.greenlet = greenlet(self.event_handler)
        self.running = False
        self.receiver = receiver
        self.scheduler = scheduler

    def invoke(self):
        self.running = True

    def run_until_reschedule(self):
        self.greenlet.switch()

    def event_handler(self):
        while True:
            try:
                if self.running:
                    if self.send_receiver:
                        self.func(self.receiver)
                    else:
                        self.func()
            except StopThisScriptException:
                pass

            self.running = False
            self.scheduler.schedule()


class StopThisScriptException(Exception):
    pass
