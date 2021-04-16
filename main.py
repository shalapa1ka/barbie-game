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
# ***** hero params
x = W // 2
y = H // 2
speed = 4
jump = 20
move = jump + 1
# ***** draw main scene
screen = pygame.display.set_mode((W, H))
ground = pygame.Surface((W, 100))
hero = pygame.Surface((50, 50))
hero.fill(WHITE)
ground.fill(GREEN)
rect_ground = ground.get_rect(bottom=H)
rect_hero = hero.get_rect(centerx=x - 25, bottom=H - ground.get_height())
clock = pygame.time.Clock()
screen.blit(ground, rect_ground)
screen.blit(hero, rect_hero)

# isRun = True
while True:  # isRun:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
            # pygame.quit()
            # isRun = False

    keys = pygame.key.get_pressed()
    # ***** walk
    if keys[pygame.K_LEFT]:
        rect_hero.left -= speed
    if keys[pygame.K_RIGHT]:
        rect_hero.left += speed
    # *****
    # ***** jump
    if keys[pygame.K_SPACE] and H - ground.get_height() == rect_hero.bottom:
        move = -jump
    if move <= jump:
        if rect_hero.bottom + move < H - ground.get_height():
            rect_hero.bottom += move
            if move < jump:
                move += 1
        else:
            rect_hero.bottom = H - ground.get_height()
            move = jump + 1
    # *****
    screen.fill(BLACK)
    screen.blit(ground, rect_ground)
    screen.blit(hero, rect_hero)
    pygame.display.update()
    clock.tick(FPS)
