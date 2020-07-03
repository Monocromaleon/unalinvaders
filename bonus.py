from pygame import event, time

from random import randint

from bullet import Bullet
from character import Character
from player import Player
from sprite_sheet import SpriteSheet

from settings import (
    CUSTOM_EVENTS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)

class Bonus(Character):
    def __init__(self):
        sprites = SpriteSheet('bonus').load_strip((0, 0, 93, 49), 2)
        super(Bonus, self).__init__(sprites, (-93, SCREEN_HEIGHT * .1), 5, 5, 0)

    def kill(self, drop = True):
        super().kill()

        if drop:
            gun = BonusBullet((self.rect.centerx, self.rect.centery))

            event.post(event.Event(CUSTOM_EVENTS['ADD_BONUS_BULLET'], {
                'particle': gun
            }))
            pass

        time.set_timer(CUSTOM_EVENTS['ADD_BONUS'], randint(10000, 15000))

    def move(self):
        if self.rect.midleft[0] > SCREEN_WIDTH:
            self.kill(False)

        self.rect.centerx += self.speed


class BonusBullet(Bullet):
    def __init__(self, position):
        gun = SpriteSheet('bullets').load_strip((102, 0, 24, 22), 6)
        super(BonusBullet, self).__init__(gun, position, 10, 0, (0, 1))

    def move(self):
        super().move()
        print(self.rect.center)
        if self.rect.midbottom[1] >= SCREEN_HEIGHT * .9:
            self.speed = 0

    def hit(self, player):
        if isinstance(player, Player):
            player.life = player.max_life
            self.kill()
