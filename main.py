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
pygame.display.set_caption('my game')
screen.fill(BLACK)
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
        mouse_btn = pygame.mouse.get_pressed(3)
        if mouse_btn[0] == 1:
            x, y = pygame.mouse.get_pos()
            r = 2
            pygame.draw.circle(screen, WHITE, (x - (r // 2), y - (r // 2)), r)
        if mouse_btn[2] == 1:
            screen.fill(BLACK)

    #         x = pygame.mouse.get_pos()[0] - 25
    #         y = pygame.mouse.get_pos()[1] - 25
    # keys = pygame.key.get_pressed()

    # if keys[pygame.K_LEFT]:
    #     x -= speed
    # if keys[pygame.K_RIGHT]:
    #     x += speed
    # if keys[pygame.K_UP]:
    #     y -= speed
    # if keys[pygame.K_DOWN]:
    #     y += speed

    # pygame.draw.rect(screen, BLACK, (x, y, 50, 50))
    pygame.display.update()
    clock.tick(FPS)