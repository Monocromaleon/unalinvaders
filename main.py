import pygame

from random import randint
from os import getcwd, path
from pygame import (
    display,
    mixer,
    font,
    sprite,
)

from level_1 import Level1
from level_2 import Level2
from on_next import OnWinScene, OnLoseScene, OnVictoryScene

from particle import Particle
from fonts import HeadingFont, PixelFont
from scene import Scene
from sprite_sheet import SpriteSheet

from settings import (
    FPS,
    PLAY_MUSIC,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)

class StartScene(Scene):
    level = 1

    def __init__(self, screen):
        super(StartScene, self).__init__(screen)

        mantillin_sprites = SpriteSheet("mantillin").load_strip((0, 0, 108, 121.5), 4)

        self.text_title = HeadingFont(45).render("UNAL", True, (3, 169, 244))
        self.text_subtitle = HeadingFont(60).render("INVADERS", True, (233, 30, 99))
        self.text_start = PixelFont(26).render("press enter to start", True, (255, 255, 255))
        self.star = pygame.image.load("assets/star.png").convert_alpha()

        self.mantillin = sprite.Group([
            Particle(mantillin_sprites, (SCREEN_WIDTH / 2 - mantillin_sprites[0].get_width() / 8, SCREEN_HEIGHT / 3 + 2 * self.text_subtitle.get_height()), 0, 0, 0)
        ])


    def run(self, next=None):
        if PLAY_MUSIC:
            mixer.music.load('./assets/pantalla_inicial.ogg')
            mixer.music.play(loops=-1)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.running = False

            self.draw()
            self.clock.tick(3)

        self.running = True

        if PLAY_MUSIC:
            mixer.music.stop()

        self.run_level()

    def run_level(self):
        if self.level == 1:
            level = Level1(self.screen)
        elif self.level == 2:
            level = Level2(self.screen)

        level.run()
        self.after_level(level)

    def after_level(self, level):
        if level.should_exit:
            return

        if level.player.alive():
            if self.level == 1:
                self.level += 1
                on_next_scene = OnWinScene(self.screen, self.run_level)
            else:
                self.level = 1
                on_next_scene = OnVictoryScene(self.screen, self.run)
        else:
            self.level = 1
            on_next_scene = OnLoseScene(self.screen, self.run)

        next = on_next_scene.run()

        if next != None:
            next()

    def draw(self):
        self.screen.fill((26, 35, 126))

        for mantillin in self.mantillin:
            mantillin.render()

        for i in range(20):
            self.screen.blit(self.star, (randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT)))

        self.screen.blit(self.text_title, (SCREEN_WIDTH / 2 - self.text_title.get_width() / 2, SCREEN_HEIGHT / 4 - self.text_title.get_height()))
        self.screen.blit(self.text_subtitle, (SCREEN_WIDTH / 2 - self.text_subtitle.get_width() / 2, SCREEN_HEIGHT / 4 + self.text_subtitle.get_height() / 4))
        self.mantillin.draw(self.screen)
        self.screen.blit(self.text_start, (SCREEN_WIDTH / 2 - self.text_start.get_width() / 2, SCREEN_HEIGHT / 1.5 + self.text_start.get_height() / 2))

        display.flip()


if __name__ == "__main__":
    pygame.init()
    mixer.init()
    font.init()

    screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    StartScene(screen).run()

    font.quit()
    mixer.quit()
    pygame.quit()
