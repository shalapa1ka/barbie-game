import pygame as pg
import json
import time
import datetime as dt
from hero import Hero
from ball import Ball
from button import Button
from input import InputBox
from random import randint
from mysql.connector import connect, Error

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
player = {
    'date': '',
    'name': '',
    'score': 0,
}

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
buttons = [easy_btn, normal_btn, hard_btn]

# nameBox
nameBox = InputBox(W // 2 - 70, 200, 140, 40)
txt_name = font.render('Enter your name', True, WHITE)

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
main_theme = pg.mixer.Sound('sounds/show.wav')
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


def get_difficulty_level():
    done = False
    while not done:
        for event in pg.event.get():
            nameBox.handle_event(event)
            if event.type == pg.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        choice = button.name
                        done = True
            elif event.type == pg.QUIT:
                exit()
        screen.fill((30, 30, 30))
        screen.blit(txt_name, (W // 2 - txt_name.get_width() // 2, 150))
        for button in buttons:
            button.draw(screen)
        nameBox.update(screen)
        nameBox.draw(screen)
        pg.display.update()

    player['name'] = nameBox.get_name()
    player['date'] = dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    difficulty_dict = {
        'Easy': {'speed': 10, 'hearts': 5},
        'Normal': {'speed': 7, 'hearts': 3},
        'Dior': {'speed': 5, 'hearts': 0}
    }
    speed = difficulty_dict[choice]['speed']
    hearts = difficulty_dict[choice]['hearts']
    return speed, hearts


# set hero speed and lives
hero.set_difficulty(*get_difficulty_level())
hearts_list = hero.get_hearts_list()

main_theme.play(loops=-1)
isRun = True
while isRun:  # isRun:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
            # pygame.quit()
            # isRun = False
        elif event.type == pg.USEREVENT:
            createBall(balls, min_speed, max_speed)
    if len(hearts_list) == 0:
        player['score'] = game_score
        over_x = screen.get_rect().center[0] - game_over.get_width() // 2
        over_y = 200
        screen.fill(BLACK)
        over_text = font.render(player['name'] + " score = " + str(game_score), True, WHITE)
        over_text_x = screen.get_rect().center[0] - over_text.get_width() // 2
        over_text_y = game_over.get_rect().bottom - 50
        screen.blit(game_over, (over_x, over_y))
        screen.blit(over_text, (over_text_x, over_text_y))
        main_theme.stop()
        game_over_sound.play()
        player_score_list = []
        try:
            with connect(
                    host="localhost",
                    user='root',
                    password='',
            ) as connection:
                use_barbie = "USE barbie"
                insert_current_result = "insert into player_results(date, name, score)" \
                                        "VALUES (%s, %s, %s) "
                values = (player['date'], player['name'], player['score'])
                select_list = "select date, name, score from player_results order by score DESC limit 10"
                with connection.cursor() as cursor:
                    cursor.execute(use_barbie)
                    cursor.execute(insert_current_result, values)
                    connection.commit()
                    cursor.execute(select_list)
                    i = 0
                    bias = 50
                    for item in cursor:
                        row_text = item[0] + " " + item[1] + "  " + str(item[2])
                        row_text = font.render(str(row_text), True, WHITE)
                        row_x = screen.get_rect().center[0] - row_text.get_width() // 2 + 10
                        row_y = 400 + bias * i
                        screen.blit(row_text, (row_x, row_y))
                        i += 1
                    pg.display.flip()
        except Error as e:
            print(e)
        time.sleep(10)
        isRun = False
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
