import pygame
import time
import os
from hero import Hero
from ball import Ball
from random import randint

# const
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

# params
game_score = tmp_score = 0
min_speed = 1
max_speed = 3
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 30, True)

# draw main scene
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Блядки')

# difficulty choice
easy = pygame.Surface()
rect_easy = easy.get_rect(center=(W // 2 - 150, H // 2))
easy_text = font.render('EASY', True, WHITE)
easy.fill(WHITE)
screen.blit(easy, rect_easy)
time.sleep(5)

# create hero
hero = Hero(W // 2, H - 100, 5, 1, 'barbie.png')

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

# hearts
heart = pygame.image.load('images/hearts.png').convert_alpha()
heart = pygame.transform.scale(heart, (100, 100))
hearts_list = []
for i in range(hero.lives):
    hearts_list.append(heart.copy())

# game over
game_over = pygame.image.load("images/over.png").convert_alpha()

# sounds
main_theme = pygame.mixer.Sound('sounds/dior.wav')
game_over_sound = pygame.mixer.Sound('sounds/opa.wav')
game_over_sound.set_volume(0.2)
main_theme.set_volume(0.1)
main_theme.play()

# create balls group
balls = pygame.sprite.Group()


def createBall(group, min_speed, max_speed):
    x = randint(20, W - 20)
    speed = randint(min_speed, max_speed)
    surf = pygame.image.load('images/ken.png').convert_alpha()
    surf = pygame.transform.scale(surf, (100, 276))  # 172x470
    return Ball(x, speed, surf, group)


# func for target capture tracking
def collideBalls():
    global game_score
    for ball in balls:
        if hero.rect.collidepoint(ball.rect.center):
            game_score += 100
            ball.kill()


def get_difficulty_level(choice):
    difficulty_dict = {
        'easy': {'speed': 10, 'hearts': 5},
        'normal': {'speed': 7, 'hearts': 3},
        'dior': {'speed': 5, 'hearts': 1}
    }
    speed = difficulty_dict[choice]['speed']
    hearts = difficulty_dict[choice]['hearts']
    return speed, hearts


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
        main_theme.stop()
        game_over_sound.play()
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
    score_text = font.render(str(game_score), True, WHITE)
    text_x = score.get_rect().center[0] - score_text.get_width() // 2 + 10
    text_y = score.get_rect().center[1] - score_text.get_height() // 2 + 10
    screen.blit(score_text, (text_x, text_y))

    for heart in hearts_list:
        screen.blit(heart, (W - 10 - heart.get_width() * (hearts_list.index(heart) + 1), 10))

    screen.blit(ground, rect_ground)
    hero.draw(screen)
    hero.move(keys)
    hero.jump(keys, rect_ground)
    balls.draw(screen)
    balls.update(hearts_list, H)
    collideBalls()

    pygame.display.update()
    clock.tick(FPS)
