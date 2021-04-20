import pygame
from hero import Hero
from ball import Ball
from random import randint

pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 2000)

# ***** const
FPS = 120
W, H = 1000, 1000
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
# score
score = pygame.image.load('images/score.png').convert_alpha()
score = pygame.transform.scale(score, (200, 100))
font = pygame.font.SysFont('opensans', 30)
# create hero
hero = Hero(W // 2, H - 100, 5, 'barbie.png')

# create balls group
balls = pygame.sprite.Group()


def createBall(group):
    x = randint(20, W - 20)
    speed = randint(1, 3)
    surf = pygame.image.load('images/ken.png').convert_alpha()
    surf = pygame.transform.scale(surf, (100, 276))  # 172x470
    return Ball(x, speed, surf, group)


game_score = 0


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
            createBall(balls)
    keys = pygame.key.get_pressed()
    mouse_click = pygame.mouse.get_pressed(3)

    screen.blit(sky, (0, 0))
    screen.blit(score, (10, 10))
    sc_text = font.render(str(game_score), True, WHITE)

    text_x = score.get_rect().center[0] - sc_text.get_width() // 2 + 10
    text_y = score.get_rect().center[1] - sc_text.get_height() // 2 + 10
    screen.blit(sc_text, (text_x, text_y))
    screen.blit(ground, rect_ground)
    hero.draw(screen)
    hero.move(keys)
    hero.jump(keys, rect_ground)
    balls.draw(screen)
    balls.update(H)
    collideBalls()

    pygame.display.update()
    clock.tick(FPS)
