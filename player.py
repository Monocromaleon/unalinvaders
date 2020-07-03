from pygame import (
    event, Surface, draw,
    K_LEFT, K_RIGHT, K_SPACE
)

from bullet import Bullet
from particle import Particle
from sprite_sheet import SpriteSheet
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    CUSTOM_EVENTS
)
from character import Character

class Player(Character):
    def __init__(self):
        sprites = SpriteSheet("ship").load_strip((0, 0, 87, 100), 4)
        super(Character, self).__init__(sprites, (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.9), 1, 25, 5)

    def update(self, key):
        if key[K_LEFT]:
            self.move((-1, 0))
        elif key[K_RIGHT]:
            self.move((1, 0))
        elif key[K_SPACE]:
            gun = PlayerBullet((self.rect.centerx, self.rect.y - 30))

            event.post(event.Event(CUSTOM_EVENTS['ADD_PLAYER_BULLET'], {
                'particle': gun
            }))

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


class PlayerBullet(Bullet):
    def __init__(self, position):
        gun_surface = Surface((5, 10))
        gun_surface.fill((255, 255, 45))
        draw.rect(gun_surface, (0, 0, 0), [0, 0, 5, 1])
        draw.rect(gun_surface, (0, 0, 0), [0, 9, 10, 1])
        draw.rect(gun_surface, (0, 0, 0), [0, 0, 1, 5])
        draw.rect(gun_surface, (0, 0, 0), [4, 0, 1, 10])

        super(PlayerBullet, self).__init__([ gun_surface ], position, 15, 5, (0, -1))

