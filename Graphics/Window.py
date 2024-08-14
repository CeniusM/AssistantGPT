import pygame
from pygame.font import Font
from collections import namedtuple
from pygame.locals import *

Size = namedtuple("Size", "w h")


class Window:
    def __init__(self, width = 800, height = 600) -> None:
        pygame.init()
        pygame.font.init()
        self.size = Size(width, height)
        self.screen = pygame.display.set_mode(self.size)
        self.center = (self.size[0] / 2, self.size[1] / 2)

    def render_present(self):
        pygame.display.flip()

    def fill(self, color):
        self.screen.fill(color)
    
    def draw_box(self, x, y, w, h, color):
        pygame.draw.rect(self.screen, color, (x,y,w,h))

    def draw_text(self, font: Font, text: str, position: tuple, forgound, background=None, antialias=True):
        text_surface = font.render(text, antialias, forgound, background)
        self.screen.blit(text_surface, position)

    def get_events(self):
        return pygame.event.get()
    
    def translate_render(self, x, y):
        self.screen.blit(self.screen, (x,y))

    def close(self):
        pygame.font.quit()
        pygame.quit()