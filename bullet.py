from particle import Particle

class Bullet(Particle):
    def __init__(self, sprites, position, speed, damage, move_vector):
        super(Bullet, self).__init__(sprites, position, speed, 1, damage)
        self.move_vector = move_vector

    def move(self):
        super().move(self.move_vector)
