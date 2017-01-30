import pygame

from threading import Thread, Condition

sprite_list = []
event_lock = Condition()


def new_sprite(filename, x=0, y=0):
    sprite = Sprite(filename, x, y, event_lock)
    sprite_list.append(sprite)
    return sprite


def script(*receivers):
    def decorator(function):
        for receiver in receivers:
            receiver.event_handlers[function.__name__] = function

    return decorator


class Sprite:
    def __init__(self, filename, x, y, lock):
        self.x = x
        self.y = y
        self.direction = 90
        self.image = pygame.image.load(filename)
        self.centre_x = int(self.image.get_bounding_rect().width/2)
        self.centre_y = int(self.image.get_bounding_rect().height/2)
        self.event_handlers = {}
        self.event_threads = {}
        self.lock = lock

    def queue_event(self, event_name):

        if event_name in self.event_threads:
            return

        def event_handler():
            with self.lock:
                self.event_handlers[event_name](self)

                me = self.event_threads[event_name]
                print(me)
                del self.event_threads[event_name]
                del me

        thread = Thread(target=event_handler, daemon=True)
        self.event_threads[event_name] = thread
        thread.start()

    def trigger_event(self, event_name):
        if event_name in self.event_handlers:
            self.queue_event(event_name)

    def change_x_by(self, amount):
        self.x = self.x + amount
        self.lock.wait()

    def change_y_by(self, amount):
        self.y = self.y + amount
        self.lock.wait()

    def move_steps(self, steps):
        if self.direction == 90:
            self.x = self.x + steps

        if self.direction == 180:
            self.x = self.x - steps

        self.lock.wait()

    def if_on_edge_bounce(self):
        if to_real_coord((self.x, self.y), self.centre_x, self.centre_y)[0] + self.image.get_bounding_rect().width > 700 and self.direction == 90:
            self.direction = 180

        if to_real_coord((self.x, self.y), self.centre_x, self.centre_y)[0] <= 0 and self.direction == 180:
            self.direction = 90

        self.lock.wait()

def to_real_coord(coords, offx, offy):
    (x, y) = coords
    cx = int(700/2)
    cy = int(500/2)

    return cx + x - offx, cy - y - offy


def to_scratch_coord(coords):
    (x, y) = coords
    cx = int(700/2)
    cy = int(500/2)

    return x - cx, y - cy


def read_mouse():
    return to_scratch_coord(pygame.mouse.get_pos())


WHITE = (255, 255, 255)


def click_green_flag():

    pygame.init()
    screen = pygame.display.set_mode((700, 500))
    pygame.display.set_caption("Hello World")

    pygame.key.set_repeat(1, 5)
    clock = pygame.time.Clock()

    done = False
    while not done:

        with event_lock:
            for event in pygame.event.get():
                for sprite in sprite_list:
                    if event.type == pygame.QUIT:
                        done = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == 32:
                            sprite.trigger_event("when_space_key_pressed")
                        if event.key == 275:
                            sprite.trigger_event("when_right_arrow_key_pressed")
                        if event.key == 276:
                            sprite.trigger_event("when_left_arrow_key_pressed")
                        if event.key == 273:
                            sprite.trigger_event("when_up_arrow_key_pressed")
                        if event.key == 274:
                            sprite.trigger_event("when_down_arrow_key_pressed")

        with event_lock:
            if not done:
                screen.fill(WHITE)

                for sprite in sprite_list:
                    screen.blit(sprite.image, to_real_coord([sprite.x, sprite.y], sprite.centre_x, sprite.centre_y))

                pygame.display.flip()
                clock.tick(60)
            else:
                pygame.quit()

            event_lock.notify_all()