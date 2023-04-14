import pygame


class Monstre(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load('slime.png')
        self.image = self.get_img(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.speed = 0.5
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 10)
        self.old_position = self.position.copy()
        self.vie = 2
        self.status = ""
        self.is_invincible = False
        self.last_hit_time = 0

    def save_loc(self):
        self.old_position = self.position.copy()

    def move_right(self):
        self.position[0] += self.speed
        # print("droite")

    def move_left(self):
        self.position[0] -= self.speed
        # print("gauche")

    def move_up(self):
        self.position[1] -= self.speed
        # print("haut")

    def move_down(self):
        self.position[1] += self.speed
        # print("bas")

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

    def subir_degats(self):
        if not self.is_invincible:

            self.is_invincible = True
            self.last_hit_time = pygame.time.get_ticks()

            self.vie -= 1

            if self.vie <= 0:
                self.status = "dead"

    def check_invincibility(self):
        if self.is_invincible:
            now = pygame.time.get_ticks()
            if now - self.last_hit_time > 3000:
                self.is_invincible = False
