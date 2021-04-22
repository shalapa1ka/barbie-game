import pygame


class Hero:
    def __init__(self, x, y, path):
        self.speed_x = 0
        self.speed_y = 15
        self.image = pygame.image.load('images/' + path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 237))  # 252x589
        self.rect = self.image.get_rect(center=(x, 0), bottom=y)
        self.isJump = False
        self.isDrag = False
        self.lives = 0

    def set_difficulty(self, speed, hearts):
        self.speed_x = speed
        self.lives = hearts

    def get_hearts_list(self):
        heart = pygame.image.load('images/hearts.png').convert_alpha()
        heart = pygame.transform.scale(heart, (100, 100))
        hearts_list = []
        for i in range(self.lives):
            hearts_list.append(heart.copy())
        return hearts_list

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.left -= self.speed_x
        if keys[pygame.K_RIGHT]:
            self.rect.left += self.speed_x

    def jump(self, keys, ground):
        if keys[pygame.K_UP]:
            self.isJump = True
        if self.isJump:
            self.rect.bottom -= self.speed_y
            self.speed_y -= .5
            if self.rect.bottom >= ground.top:
                self.rect.bottom = ground.top
                self.speed_y = 15
                self.isJump = False

    def draw(self, sc):
        sc.blit(self.image, self.rect)

    def speed_up(self):
        self.speed_x += 1
        self.speed_y += 1
