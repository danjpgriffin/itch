class EventReceiver:

    def __init__(self, scheduler):
        self._event_handlers = {}
        self._event_tasks = {}
        self._scheduler = scheduler

    def register(self, function):
        self._event_handlers[function.__name__] = function

    def trigger_event(self, event_name):
        if event_name in self._event_handlers:
            self.queue_event(event_name)

    def run_tasks_until_reschedule(self):
        for task in [val for val in self._event_tasks.values()]:
            task.run_until_reschedule()

    def queue_event(self, event_name):

        if event_name not in self._event_tasks:
            self._event_tasks[event_name] = self._scheduler.task(self._event_handlers[event_name], self)

        self._event_tasks[event_name].invoke()

    def _schedule(self, answer=None):
        self._scheduler.schedule()
        return answer

