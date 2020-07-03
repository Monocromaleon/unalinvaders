from pygame import (
    Surface,
    sprite
)

from settings import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH
)

from particle import Particle

class Character(Particle):
    def __init__(self, sprites, position, initial_speed, life, damage):
        super(Character, self).__init__(sprites, position, initial_speed, life, damage)

    def move(self, vector):
        (x, y) = vector

        next_x = self.rect.centerx + x * self.speed
        next_y = self.rect.centery + y * self.speed

        if next_x - self.image.get_width() / 2 >= 0 and next_x + self.image.get_width() / 2 <= SCREEN_WIDTH:
            self.rect.centerx = next_x
        if next_y >= 0 - self.image.get_height() / 2 and next_y + self.image.get_height() / 2 <= SCREEN_HEIGHT:
            self.rect.centery = next_y

    def shoot(self):
        raise NotImplementedError()
