from greenlet import greenlet


def schedule():
    greenlet.getcurrent().parent.switch()


class Task:

    def __init__(self, func, receiver):
        self.func = func
        self.greenlet = greenlet(self.event_handler)
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

