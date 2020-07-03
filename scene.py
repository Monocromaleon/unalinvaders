from pygame import time, Surface

class Scene:
    clock = time.Clock()
    running = True
    screen = Surface((0, 0))

    def __init__(self, screen):
        self.screen = screen
