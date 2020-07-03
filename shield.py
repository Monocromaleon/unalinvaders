from pygame import Surface

from character import Character
from sprite_sheet import SpriteSheet

class Shield(Character):
    def __init__(self, sprites, position):
        super(Character, self).__init__(sprites, position, 0, 150, 1)

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
