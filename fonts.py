from pygame import font, Surface

class PixelFont(font.Font):
    def __init__(self, size):
        super(PixelFont, self).__init__("./assets/press_start_2p.ttf", size)

class HeadingFont(PixelFont):
    def _hollow(self, message, antialias, color):
        notcolor = [c^0xFF for c in color]
        base = super().render(message, antialias, color, notcolor)

        size = base.get_width() + 2, base.get_height() + 2
        img = Surface(size, 16)

        img.fill(notcolor)
        base.set_colorkey(0)
        img.blit(base, (0, 0))
        img.blit(base, (3, 0))
        img.blit(base, (0, 3))
        img.blit(base, (3, 3))

        base.set_colorkey(0)
        base.set_palette_at(1, notcolor)
        img.blit(base, (1, 1))
        img.set_colorkey(notcolor)

        return img

    def render(self, message, antialias, color):
        base = super().render(message, antialias, color)
        outline = self._hollow(message, antialias, (0, 0, 0))

        img = Surface(outline.get_size(), 16)
        img.blit(outline, (0, 0))
        img.blit(base, (1, 1))

        return img
