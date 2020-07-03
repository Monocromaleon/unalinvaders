import pygame

class SpriteSheet:
    """Load the sheet."""
    def __init__(self, file):
        self.sheet = pygame.image.load("assets/{0}.png".format(file)).convert_alpha()

    """Load a specific image from a specific rectangle."""
    def image_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)

        return image

    """Load a whole bunch of images and return them as a list."""
    def images_at(self, rects):
        return [self.image_at(rect) for rect in rects]

    """Load a whole strip of images, and return them as a list."""
    def load_strip(self, rect, image_count):
        tups = [(rect[0] + x * rect[2], rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups)
