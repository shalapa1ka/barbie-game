import pygame

pygame.init()
font = pygame.font.SysFont('arial', 30, True)


class Button:
    def __init__(self, size=(0, 0), pos=(0, 0), name='', color=(0, 0, 0)):
        self.rect = pygame.Rect(0, 0, *size)
        self.name = name
        self.color = color
        self.rect.center = pos[0], pos[1]

    def on_click(self):
        return self.name

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)
        text = font.render(self.name, True, (0, 0, 0))
        text_x = self.rect.centerx - text.get_width() // 2
        text_y = self.rect.centery - text.get_height() // 2
        surf.blit(text, (text_x, text_y))
