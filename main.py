import pygame
from hero import Hero

pygame.init()

# ***** const
FPS = 120
W, H = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# ***** draw main scene
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Блядки')
# sky
sky = pygame.image.load('images/background.jpg').convert()
sky = pygame.transform.scale(sky, (W, H))
# ground
ground = pygame.image.load('images/dirt.jpg').convert()
ground = pygame.transform.scale(ground, (W, 100))
rect_ground = ground.get_rect(bottom=H)
# create hero
Mario = Hero(W // 2, H - 100, 5, 'barbie.png')

clock = pygame.time.Clock()
screen.blit(sky, (0, 0))
screen.blit(ground, rect_ground)
Mario.draw(screen)

# isRun = True
while True:  # isRun:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
            # pygame.quit()
            # isRun = False
    keys = pygame.key.get_pressed()
    mouse_click = pygame.mouse.get_pressed(3)

    screen.blit(sky, (0, 0))
    screen.blit(ground, rect_ground)
    Mario.draw(screen)
    Mario.move(keys)
    Mario.jump(keys, rect_ground)
    pygame.display.update()
    clock.tick(FPS)
