import pygame
import random
import time

class Monstre(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load('slime.png')
        self.image = self.get_img(0,0)
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.speed = 1
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 10)
        self.old_position = self.position.copy()

    def save_loc(self):
        self.old_position = self.position.copy()

    def move(self):
        random_value = random.randint(1, 100)


        if random_value <= 25:
            self.position[0] += self.speed
        elif 51 > random_value > 25:
            self.position[0] -= self.speed

        elif 76 > random_value >= 51:
            self.position[1] += self.speed

        elif 101 > random_value > 75:
            self.position[1] -= self.speed

    def get_img(self, x, y):
        image = pygame.Surface([16, 16])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 16, 16))
        return image

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
