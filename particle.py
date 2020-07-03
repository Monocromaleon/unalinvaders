from pygame import (
    sprite,
    Surface
)

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)

class Particle(sprite.Sprite):
    def __init__(self, sprites, position, initial_speed, life, damage):
        super(Particle, self).__init__()

        self.sprites = sprites
        self.speed = initial_speed
        self.max_life = life
        self.life = life
        self.damage = damage

        self.image = Surface((self.sprites[0].get_width(), self.sprites[0].get_height()))
        self.rect = self.image.get_rect()

        (x, y) = position
        self.rect.centerx = x
        self.rect.centery = y

        self.render()

    def move(self, move_vector):
        (x, y) = move_vector

        next_x = self.rect.centerx + x * self.speed
        next_y = self.rect.centery + y * self.speed

        if next_x < 0 or next_x > SCREEN_WIDTH or next_y < 0 or next_y > SCREEN_HEIGHT:
            self.kill()

        self.rect.centerx = next_x
        self.rect.centery = next_y

    def hit(self, other):
        other.life -= self.damage
        self.life -= other.damage

        if self.life <= 0:
            self.kill()

        if other.life <= 0:
            other.kill()

    def render(self):
        sprite = self.sprites[0]
        self.sprites = self.sprites[1:] + [ sprite ]

        self.image.fill((0,0,0,0))
        self.image.blit(sprite, (0, 0))
