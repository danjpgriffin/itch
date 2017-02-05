from greenlet import greenlet


def schedule():
    greenlet.getcurrent().parent.switch()


def task(func):
    return greenlet(func)