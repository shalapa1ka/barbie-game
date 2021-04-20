import pygame


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, speed, surf, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = speed
        self.add(group)
        self.off = pygame.mixer.Sound('sounds/oof.wav')
        self.off.set_volume(0.5)

    def update(self, heats, *args):
        if self.rect.y < args[0] - 20:
            self.rect.y += self.speed
        else:
            self.kill()
            self.off.play()
            heats.pop()
