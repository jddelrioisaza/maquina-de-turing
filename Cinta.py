import pygame
import os

class CintaPygame:
    def __init__(self, cinta, width, height):
        os.environ['SDL_VIDEO_WINDOW_POS'] = '100,550'
        pygame.font.init()
        self.cinta = cinta
        self.width = width
        self.height = height
        self.padding = 10
        self.cell_size = (self.width - 2 * self.padding) // len(cinta)
        self.font = pygame.font.SysFont(None, self.cell_size)
        self.screen = pygame.display.set_mode((width, height))
        self.pointer_position = 0

        self.draw()

    def draw(self):
        self.screen.fill((255, 255, 255))

        for i in range(len(self.cinta)):
            x = self.padding + i * self.cell_size
            y = self.height // 2 - self.cell_size // 2
            cell_surface = self.font.render(self.cinta[i], True, (0, 0, 0))
            self.screen.blit(cell_surface, (x, y))
            if i == self.pointer_position:
                pygame.draw.line(self.screen, (255, 0, 0), (x - 15, y + self.cell_size), (x + self.cell_size//2 - 5, y + self.cell_size), 2)
                arrow_points = ((x + self.cell_size // 2 - 48, y + self.cell_size - 25),
                                (x + self.cell_size // 2 - 10 - 48, y + self.cell_size - 10),
                                (x + self.cell_size // 2 + 10 - 48, y + self.cell_size - 10))
                pygame.draw.polygon(self.screen, (255, 0, 0), arrow_points)
        pygame.display.update()

    def move_pointer_left(self):
        if self.pointer_position > 0:
            self.pointer_position -= 1
            self.draw()

    def move_pointer_right(self):
        if self.pointer_position < len(self.cinta) - 1:
            self.pointer_position += 1
            self.draw()