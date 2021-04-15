import pygame
from math import pi

pygame.init()

# ***** const
FPS = 120
W, H = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
# *****
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

x = W // 2  # obj pos_x
y = H // 2  # obj pos_y
speed = 4  # obj speed

# isRun = True
while True:  # isRun:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
            # pygame.quit()
            # isRun = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed



    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (x, y, 50, 100))
    pygame.display.update()
    clock.tick(FPS)
