import pygame as pg
import time
import os
from hero import Hero
from ball import Ball
from button import Button
from random import randint

# const
FPS = 120
TIME = 2000
W, H = 1000, 1000
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

# init
pg.init()
pg.time.set_timer(pg.USEREVENT, TIME)

# params
game_score = tmp_score = 0
min_speed = 1
max_speed = 3
clock = pg.time.Clock()
font = pg.font.SysFont('arial', 30, True)

# draw main scene
screen = pg.display.set_mode((W, H))
pg.display.set_caption('Barbie')

# button draw
easy_btn = Button((133, 200), (200, H // 2), 'Easy', GREEN)
easy_btn.draw(screen)
normal_btn = Button((133, 200), (W // 2, H // 2), 'Normal', ORANGE)
normal_btn.draw(screen)
hard_btn = Button((133, 200), (W - 200, H // 2), 'Dior', RED)
hard_btn.draw(screen)
pg.display.flip()

# sky
sky = pg.image.load('images/background.jpg').convert()
sky = pg.transform.scale(sky, (W, H))

# ground
ground = pg.image.load('images/dirt.jpg').convert()
ground = pg.transform.scale(ground, (W, 100))
rect_ground = ground.get_rect(bottom=H)

# score
score = pg.image.load('images/score.png').convert_alpha()
score = pg.transform.scale(score, (200, 100))

# create hero
hero = Hero(W // 2, H - 100, 'barbie.png')

# game over
game_over = pg.image.load("images/over.png").convert_alpha()

# sounds
main_theme = pg.mixer.Sound('sounds/dior.wav')
game_over_sound = pg.mixer.Sound('sounds/opa.wav')
game_over_sound.set_volume(0.2)
main_theme.set_volume(0.1)

# create balls group
balls = pg.sprite.Group()


def createBall(group, min_speed, max_speed):
    x = randint(20, W - 20)
    speed = randint(min_speed, max_speed)
    surf = pg.image.load('images/ken.png').convert_alpha()
    surf = pg.transform.scale(surf, (100, 276))  # 172x470
    return Ball(x, speed, surf, group)


# func for target capture tracking
def collideBalls():
    global game_score
    for ball in balls:
        if hero.rect.collidepoint(ball.rect.center):
            game_score += 100
            ball.kill()


def get_difficulty_level(choice=None):
    while choice is None:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if easy_btn.rect.collidepoint(pg.mouse.get_pos()):
                    choice = easy_btn.on_click()
                elif normal_btn.rect.collidepoint(pg.mouse.get_pos()):
                    choice = normal_btn.on_click()
                elif hard_btn.rect.collidepoint(pg.mouse.get_pos()):
                    choice = hard_btn.on_click()
            elif event.type == pg.QUIT:
                exit()
    difficulty_dict = {
        'Easy': {'speed': 10, 'hearts': 5},
        'Normal': {'speed': 7, 'hearts': 3},
        'Dior': {'speed': 5, 'hearts': 1}
    }
    speed = difficulty_dict[choice]['speed']
    hearts = difficulty_dict[choice]['hearts']
    return speed, hearts


# set hero speed and lives
hero.set_difficulty(*get_difficulty_level())

hearts_list = hero.get_hearts_list()

main_theme.play(loops=-1)
# isRun = True
while True:  # isRun:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
            # pygame.quit()
            # isRun = False
        elif event.type == pg.USEREVENT:
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
        pg.display.flip()  # Add this.
        main_theme.stop()
        game_over_sound.play()
        time.sleep(3)
        os._exit(1)
        pg.quit()
    if game_score == tmp_score + 400:
        min_speed += 1
        max_speed += 2
        tmp_score = game_score
        hero.speed_up()
    keys = pg.key.get_pressed()
    # mouse_click = pygame.mouse.get_pressed(3)

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
    hero.move(keys, screen)
    hero.jump(keys, rect_ground)
    balls.draw(screen)
    balls.update(hearts_list, H)
    collideBalls()

    pg.display.update()
    clock.tick(FPS)
