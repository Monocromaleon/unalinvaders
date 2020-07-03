from pygame import (
    display,
    event,
    image,
    mixer,
    key,
    QUIT,
    sprite,
    time,
    transform,
)

import math
from random import random
from threading import Thread

from settings import (
    FPS,
    CUSTOM_EVENTS,
    PLAY_MUSIC,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)

from aliens import load_aliens
from bonus import Bonus
from scene import Scene
from shield import Shield
from sprite_sheet import SpriteSheet
from particle import Particle
from player import Player

class Level1(Scene):
    def __init__(self, screen):
        super(Level1, self).__init__(screen)

        self.id = 1
        self.should_exit = False
        self.background = image.load("assets/background.png").convert_alpha()

        self.player = Player()
        self.players = sprite.Group([ self.player ] + self.load_shields())
        self.player_bullets = sprite.Group()
        self.aliens = sprite.Group(load_aliens())
        self.alien_bullets = sprite.Group()
        self.bonus = sprite.Group([ Bonus() ])

    def load_shields(self):
        sprites = SpriteSheet("shields").load_strip((0, 0, 87, 84), 4)

        return [ Shield([ sprites[i] ], (.20 * (i + 1) * SCREEN_WIDTH, SCREEN_HEIGHT * 0.75)) for i in range(len(sprites)) ]

    """Main sequence"""
    def run(self):
        threads = [
            Thread(target=self.control_player),
            Thread(target=self.run_aliens),
            Thread(target=self.run_bonus),
            Thread(target=self.run_players),
            Thread(target=self.run_player_bullets),
            Thread(target=self.run_alien_bullets),
        ]

        for thread in threads:
            thread.start()

        self.run_main()

        for thread in threads:
            thread.join()

    # Main controllers
    def run_main(self):
        if PLAY_MUSIC:
            mixer.music.load('./assets/en_batalla.ogg')
            mixer.music.play(loops=-1)

        while self.running:
            self.screen.fill((255, 255, 255))

            transform.scale(self.background,
                (SCREEN_WIDTH, SCREEN_HEIGHT), self.screen
            )

            self.check_events()
            self.check_collisions()
            self.draw()

            display.flip()
            self.clock.tick(2 * FPS)

            if len(self.aliens) == 0:
                self.running = False
            if not self.player.alive():
                self.running = False

        if PLAY_MUSIC:
            mixer.music.stop()

    # Player controller
    def control_player(self):
        while self.running:
            pressed_keys = key.get_pressed()
            self.players.update(pressed_keys)

            self.clock.tick(6 * FPS)

    # Aliens controller
    def run_aliens(self):
        while self.running:
            self.move_aliens()
            self.render_aliens()

    # Bonus controller
    def run_bonus(self):
        while self.running:
            self.move_bonus()
            self.render_bonus()

    # Player-related objects controller
    def run_players(self):
        while self.running:
            self.render_players()

    # Plater bullets controller
    def run_player_bullets(self):
        while self.running:
            self.move_player_bullets()
            self.render_player_bullets()

    # Alien bullets controller
    def run_alien_bullets(self):
        while self.running:
            self.move_alien_bullets()
            self.render_alien_bullets()


    def check_events(self):
        for evt in event.get():
            if evt.type == QUIT:
                self.should_exit = True
                self.running = False
            elif evt.type == CUSTOM_EVENTS['ADD_PLAYER_BULLET']:
                if len(self.player_bullets) < 2:
                    self.player_bullets.add(evt.particle)
            elif evt.type == CUSTOM_EVENTS['ADD_ALIEN_BULLET']:
                if len(self.alien_bullets) < 4:
                    self.alien_bullets.add(evt.particle)
            elif evt.type == CUSTOM_EVENTS['ADD_BONUS']:
                self.bonus.add(Bonus())
            elif evt.type == CUSTOM_EVENTS['ADD_BONUS_BULLET']:
                self.alien_bullets.add(evt.particle)


    def check_collisions(self):
        collided_aliens = sprite.groupcollide(self.aliens, self.player_bullets, False, False)
        collided_bonus = sprite.groupcollide(self.bonus, self.player_bullets, False, False)
        hit_players = sprite.groupcollide(self.players, self.alien_bullets, False, False)
        collided_players_with_aliens = sprite.groupcollide(self.players, self.aliens, False, False)

        for alien in collided_aliens:
            for bullet in collided_aliens[alien]:
                bullet.hit(alien)

        for bonus in collided_bonus:
            for bullet in collided_bonus[bonus]:
                bullet.hit(bonus)

        for player in hit_players:
            for bullet in hit_players[player]:
                bullet.hit(player)

        for player in collided_players_with_aliens:
            for alien in collided_players_with_aliens[player]:
                alien.hit(player)

    """Methods for movement"""
    # This function moves the aliens alongside the game grid.
    def move_aliens(self):
        for alien in self.aliens:
            if alien.alive():
                alien.move()
                alien.shoot()

    # This function moves the bonus over the game grid
    def move_bonus(self):
        for bonus in self.bonus:
            bonus.move()

    def move_player_bullets(self):
        for bullet in self.player_bullets:
            bullet.move()

    def move_alien_bullets(self):
        for bullet in self.alien_bullets:
            bullet.move()

    """Methods for rendering"""
    # This function renders aliens' surfaces into the parent surface (a.k.a. screen)
    def render_players(self):
        for player in self.players:
            player.render()

        self.clock.tick(FPS / 15)

    def render_aliens(self):
        for alien in self.aliens:
            alien.render()

        self.clock.tick(FPS / (5 * math.log(len(self.aliens) + 1) + 1))

    # This function renders bonus surface into the parent surface (a.k.a. screen)
    def render_bonus(self):
        for bonus in self.bonus:
            bonus.render()

        self.clock.tick(FPS)

    # This function renders particles' surfaces into the parent surface (a.k.a. screen)
    def render_player_bullets(self):
        for particle in self.player_bullets:
            particle.render()

        self.clock.tick(FPS / 2)

    # This function renders particles' surfaces into the parent surface (a.k.a. screen)
    def render_alien_bullets(self):
        for particle in self.alien_bullets:
            particle.render()

        self.clock.tick(FPS / 3)


    """Methods for drawing"""
    def draw_alien_bullets(self):
        try:
            self.alien_bullets.draw(self.screen)
        except:
            self.clock.tick(2 * FPS)
            self.draw_alien_bullets()

    def draw(self):
        self.bonus.draw(self.screen)
        self.draw_alien_bullets()
        self.aliens.draw(self.screen)
        self.player_bullets.draw(self.screen)
        self.players.draw(self.screen)
