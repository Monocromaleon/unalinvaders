from random import randint

from pygame import (
    display,
    event,
    image,
    mixer,
    KEYDOWN,
    K_ESCAPE,
    K_RETURN,
    QUIT,
    sprite,
)

from settings import (
    PLAY_MUSIC,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)

from fonts import HeadingFont, PixelFont
from particle import Particle
from sprite_sheet import SpriteSheet
from scene import Scene

class OnNextScene(Scene):
    loop = True

    def __init__(self, screen, on_next, song):
        super(OnNextScene, self).__init__(screen)
        self.on_next = on_next
        self.song = song

    def run(self):
        if PLAY_MUSIC:
            mixer.music.load(self.song)
            mixer.music.play(loops=-1 if self.loop else 0)

        while self.running:
            for evt in event.get():
                if evt.type == QUIT:
                    return
                elif evt.type == KEYDOWN and evt.key == K_ESCAPE:
                    return
                elif evt.type == KEYDOWN and evt.key == K_RETURN:
                    self.running = False

            self.draw()

        if PLAY_MUSIC:
            mixer.music.stop()

        return self.on_next

    def draw(self):
        self.screen.fill((26, 35, 126))
        self.render()

        display.flip()
        self.clock.tick(6)

class OnWinScene(OnNextScene):
    def __init__(self, screen, on_next):
        super(OnWinScene, self).__init__(screen, on_next, './assets/ganar_nivel.ogg')
        self.loop = False

        mantillin_sprites = SpriteSheet("mantillin").load_strip((432, 0, 108, 121.5), 1)
        hearts_sprites = SpriteSheet("hearts_un").load_strip((0, 0, 51, 48), 6)

        self.mantillin = sprite.Group([
            Particle(mantillin_sprites, (SCREEN_WIDTH / 2 - mantillin_sprites[0].get_width() / 8, SCREEN_HEIGHT / 3 + mantillin_sprites[0].get_height()), 0, 0, 0),
            Particle(hearts_sprites, (SCREEN_WIDTH / 2 + 1.25 * hearts_sprites[0].get_width(), SCREEN_HEIGHT / 3 + 1.5 * hearts_sprites[0].get_height()), 0, 0, 0)
        ])

        self.text_title = HeadingFont(60).render("YOU WON", True, (3, 169, 244))
        self.text_continue = PixelFont(26).render("press enter to continue", True, (255, 255, 255))
        self.star = image.load("assets/star.png").convert_alpha()

    def render(self):
        for i in range(20):
            self.screen.blit(self.star, (randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT)))

        for mantillin in self.mantillin:
            mantillin.render()

        self.screen.blit(self.text_title, (SCREEN_WIDTH / 2 - self.text_title.get_width() / 2, SCREEN_HEIGHT / 4 + self.text_title.get_height() / 4))
        self.mantillin.draw(self.screen)
        self.screen.blit(self.text_continue, (SCREEN_WIDTH / 2 - self.text_continue.get_width() / 2, SCREEN_HEIGHT / 1.5 + self.text_continue.get_height() / 2))

class OnVictoryScene(OnNextScene):
    def __init__(self, screen, on_next):
        super(OnVictoryScene, self).__init__(screen, on_next, './assets/victoria.ogg')

        mantillin_sprites = SpriteSheet("mantillin").load_strip((432, 0, 108, 121.5), 1)
        hearts_sprites = SpriteSheet("hearts_un").load_strip((0, 0, 51, 48), 6)

        self.mantillin = sprite.Group([
            Particle(mantillin_sprites, (SCREEN_WIDTH / 2 - mantillin_sprites[0].get_width() / 8, SCREEN_HEIGHT / 3 + mantillin_sprites[0].get_height()), 0, 0, 0),
            Particle(hearts_sprites, (SCREEN_WIDTH / 2 + 1.25 * hearts_sprites[0].get_width(), SCREEN_HEIGHT / 3 + 1.5 * hearts_sprites[0].get_height()), 0, 0, 0)
        ])

        self.text_title = HeadingFont(60).render("VICTORY", True, (3, 169, 244))
        self.text_continue = PixelFont(26).render("press enter to continue", True, (255, 255, 255))
        self.star = image.load("assets/star.png").convert_alpha()

    def render(self):
        for i in range(20):
            self.screen.blit(self.star, (randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT)))

        for mantillin in self.mantillin:
            mantillin.render()

        self.screen.blit(self.text_title, (SCREEN_WIDTH / 2 - self.text_title.get_width() / 2, SCREEN_HEIGHT / 4 + self.text_title.get_height() / 4))
        self.mantillin.draw(self.screen)
        self.screen.blit(self.text_continue, (SCREEN_WIDTH / 2 - self.text_continue.get_width() / 2, SCREEN_HEIGHT / 1.5 + self.text_continue.get_height() / 2))

class OnLoseScene(OnNextScene):
    def __init__(self, screen, on_next):
        super(OnLoseScene, self).__init__(screen, on_next, './assets/muerte.ogg')

        mantillin_sprites = SpriteSheet("mantillin").load_strip((540, 0, 108, 121.5), 1)
        self.mantillin = sprite.Group([
            Particle(mantillin_sprites, (SCREEN_WIDTH / 2 - mantillin_sprites[0].get_width() / 8, SCREEN_HEIGHT / 2), 0, 0, 0)
        ])
        self.text_title = HeadingFont(60).render("GAME OVER", True, (233, 30, 99))
        self.text_continue = PixelFont(26).render("press enter to continue", True, (255, 255, 255))
        self.star = image.load("assets/star.png").convert_alpha()

    def render(self):
        for i in range(20):
            self.screen.blit(self.star, (randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT)))

        self.screen.blit(self.text_title, (SCREEN_WIDTH / 2 - self.text_title.get_width() / 2, SCREEN_HEIGHT / 4 + self.text_title.get_height() / 4))
        self.mantillin.draw(self.screen)
        self.screen.blit(self.text_continue, (SCREEN_WIDTH / 2 - self.text_continue.get_width() / 2, SCREEN_HEIGHT / 1.5 + self.text_continue.get_height() / 2))
