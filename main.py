import pygame
import time
import os
from hero import Hero
from ball import Ball
from random import randint

# ***** const
FPS = 120
TIME = 2000
W, H = 1000, 1000
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# init
pygame.init()
pygame.time.set_timer(pygame.USEREVENT, TIME)

# ***** draw main scene
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Блядки')
# create hero
hero = Hero(W // 2, H - 100, 5, 5, 'barbie.png')
# sky
sky = pygame.image.load('images/background.jpg').convert()
sky = pygame.transform.scale(sky, (W, H))
# ground
ground = pygame.image.load('images/dirt.jpg').convert()
ground = pygame.transform.scale(ground, (W, 100))
rect_ground = ground.get_rect(bottom=H)
# score
score = pygame.image.load('images/score.png').convert_alpha()
score = pygame.transform.scale(score, (200, 100))
font = pygame.font.SysFont('opensans', 30)
# hearts
heart = pygame.image.load('images/hearts.png').convert_alpha()
heart = pygame.transform.scale(heart, (100, 100))
hearts_list = []
for i in range(hero.lives):
    hearts_list.append(heart.copy())
# game over
game_over = pygame.image.load("images/over.png").convert_alpha()

# create balls group
balls = pygame.sprite.Group()


def createBall(group, min_speed, max_speed):
    x = randint(20, W - 20)
    speed = randint(min_speed, max_speed)
    surf = pygame.image.load('images/ken.png').convert_alpha()
    surf = pygame.transform.scale(surf, (100, 276))  # 172x470
    return Ball(x, speed, surf, group)


game_score = 0
tmp_score = game_score
min_speed = 1
max_speed = 3


def collideBalls():
    global game_score
    for ball in balls:
        if hero.rect.collidepoint(ball.rect.center):
            game_score += 100
            ball.kill()


clock = pygame.time.Clock()

# isRun = True
while True:  # isRun:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
            # pygame.quit()
            # isRun = False
        elif event.type == pygame.USEREVENT:
            createBall(balls, min_speed, max_speed)
    if len(hearts_list) == 0:
        over_x = screen.get_rect().center[0] - game_over.get_width() // 2
        over_y = screen.get_rect().center[1] - game_over.get_height() // 2
        screen.fill(BLACK)
        over_text = font.render("Your score = " + str(game_score), True, WHITE)
        over_text_x = screen.get_rect().center[0] - over_text.get_width() // 2
        over_text_y = game_over.get_rect().bottom + 100
        screen.blit(game_over, (over_x, over_y))
        screen.blit(over_text, (over_text_x, over_text_y))
        pygame.display.flip()  # Add this.
        time.sleep(3)
        os._exit(1)
        pygame.quit()
    if game_score == tmp_score + 400:
        min_speed += 1
        max_speed += 2
        tmp_score = game_score
    keys = pygame.key.get_pressed()
    mouse_click = pygame.mouse.get_pressed(3)

    screen.blit(sky, (0, 0))
    screen.blit(score, (10, 10))
    for heart in hearts_list:
        screen.blit(heart, (W - 10 - heart.get_width() * (hearts_list.index(heart) + 1), 10))
    sc_text = font.render(str(game_score), True, WHITE)

    text_x = score.get_rect().center[0] - sc_text.get_width() // 2 + 10
    text_y = score.get_rect().center[1] - sc_text.get_height() // 2 + 10
    screen.blit(sc_text, (text_x, text_y))
    screen.blit(ground, rect_ground)
    hero.draw(screen)
    hero.move(keys)
    hero.jump(keys, rect_ground)
    balls.draw(screen)
    balls.update(hearts_list, H)
    collideBalls()

    pygame.display.update()
    clock.tick(FPS)
