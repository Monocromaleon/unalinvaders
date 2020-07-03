from pygame import (
    event,
    draw,
    Surface,
    transform,
)

from bullet import Bullet
from random import random, randint
from character import Character
from sprite_sheet import SpriteSheet
from particle import Particle
from settings import (
    CUSTOM_EVENTS,
    FPS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)

class Alien(Character):
    def __init__(self, sprites, position, shoot_chance):
        super(Alien, self).__init__(sprites, position, 15, 5, 10)

        self.shoot_chance = shoot_chance
        self.movement_vectors = [
            (1, 0), (1, 0), (1, 0),
            (0, 1),
            (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0),
            (0, 1),
            (1, 0), (1, 0)
        ]

    def move(self):
        vector = self.movement_vectors[0]
        self.movement_vectors = self.movement_vectors[1:] + [ vector ]

        super().move(vector)

    def shoot(self):
        if not self.alive():
            return

        if random() < self.shoot_chance:
            event.post(event.Event(CUSTOM_EVENTS['ADD_ALIEN_BULLET'], {
                'particle': self.get_bullet()
            }))


class NormalAlien(Alien):
    def __init__(self, position):
        sprites = SpriteSheet("aliens").load_strip((0, 0, 66, 54), 4)
        super(NormalAlien, self).__init__(sprites, position, 0.15)

    def get_bullet(self):
        return AlienBullet(self.rect.center)


class AlienBullet(Bullet):
    def __init__(self, position):
        gun = SpriteSheet('bullets').load_strip((92, 0, 5, 22), 2)
        super(AlienBullet, self).__init__(gun, position, 10, 5, (0, 1))


class TennisAlien(Alien):
    def __init__(self, position):
        sprites = SpriteSheet("aliens").load_strip((264, 0, 70, 54), 4)
        super(TennisAlien, self).__init__(sprites, position, 0.25)

    def get_bullet(self):
        is_right = randint(0, 1)
        position = self.rect.bottomright if is_right else self.rect.bottomleft

        bullet = TennisBullet(position)
        if is_right:
            bullet.rotate()

        return bullet


class TennisBullet(Bullet):
    angle = 0

    def __init__(self, position):
        gun = SpriteSheet('bullets').load_strip((0, 0, 23, 22), 4)
        super(TennisBullet, self).__init__(gun, position, 10, 5, (-1, 1))
        self.life = 10

    def rotate(self):
        (x, y) = self.move_vector
        self.move_vector = (y, -x)
        self.angle = (self.angle + 90) % 360

    def move(self):
        print(self.rect.midleft, self.rect.midright, self.rect.midbottom, self.rect.midtop)

        if self.rect.midleft[0] <= 0:
            if self.angle == 180:
                self.rotate()
            self.rotate()

        if self.rect.midright[0] >= SCREEN_WIDTH:
            if self.angle == 90:
                self.rotate()
            self.rotate()

        if self.rect.midtop[1] <= 0:
            if self.angle == 270:
                self.rotate()
            self.rotate()

        if self.rect.midbottom[1] >= SCREEN_HEIGHT:
            if self.angle == 0:
                self.rotate()
            self.rotate()

        super().move()

    def render(self):
        super().render()
        rotated_surface = transform.rotate(self.image, self.angle)

        self.image.fill((0,0,0,0))
        self.image.blit(rotated_surface, (0, 0))

    def hit(self, other):
        self.rotate()
        super().hit(other)


class Pechatron(Alien):
    def __init__(self):
        sprites = SpriteSheet("pecha").load_strip((0, 0, 109, 85), 4)
        super(Pechatron, self).__init__(sprites, (SCREEN_WIDTH / 2, SCREEN_HEIGHT * .2), 0.1)

        self.movement_vectors = [(1, 0)]
        self.max_life = 100
        self.life = 100

    def move(self):
        if self.rect.midleft[0] <= SCREEN_WIDTH * .1 and self.movement_vectors[0] == (-1, 0):
            self.movement_vectors = [(1, 0)]
        elif self.rect.midright[0] >= SCREEN_WIDTH * .9 and self.movement_vectors[0] == (1, 0):
            self.movement_vectors = [(-1, 0)]

        super().move()


    def get_bullet(self):
        return PechaBullet(self.rect.midbottom)

    def render(self):
        sprite = self.sprites[0]
        self.sprites = self.sprites[1:] + [ sprite ]

        self.image.fill((0,0,0,0))
        self.image.blit(sprite, (0, 0))

        life_surface = Surface((25, 7.5))
        life_surface.fill((0, 0, 0))

        current_life_surface = Surface((life_surface.get_width() * self.life / self.max_life, life_surface.get_height()))
        current_life_surface.fill((62, 228, 116))

        self.image.blit(life_surface, (self.rect.width / 2 - life_surface.get_width() / 2, self.rect.height / 2 + life_surface.get_height()))
        self.image.blit(current_life_surface, (self.rect.width / 2 - life_surface.get_width() / 2, self.rect.height / 2 + life_surface.get_height()))


class PechaBullet(Bullet):
    def __init__(self, position):
        gun = SpriteSheet('pecha').load_strip((436, 0, 25, 59), 1)
        super(PechaBullet, self).__init__(gun, position, 15, 5, (0, 1))
        self.life = 10


def load_aliens(col = None, row = None):
    rows = 8
    cols = 4

    margin = 20

    row_size = rows * (70 + margin) - margin
    col_size = cols * (54 + margin) - margin

    start_x = SCREEN_WIDTH / 2 - row_size / 2.45
    start_y = SCREEN_HEIGHT / 2 - col_size

    if col != None and row != None:
        position = (
            start_x + row * (70 + margin),
            start_y + col * (54 + margin)
        )

        return NormalAlien(position) if randint(0, 1) else TennisAlien(position)

    aliens = []
    for row in range(rows):
        for col in range(cols):
            position = (
                start_x + row * (70 + margin),
                start_y + col * (54 + margin)
            )

            if col % 2:
                aliens.append(NormalAlien(position))
            else:
                aliens.append(TennisAlien(position))

    return aliens
