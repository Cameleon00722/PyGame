import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load('player_knight.png')
        self.image = self.get_img(0,0)
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0,0, self.rect.width*0.5, 10)
        self.old_position = self.position.copy()

    def save_loc(self): self.old_position = self.position.copy()

    def move_right(self): self.position[0] += 2

    def move_left(self): self.position[0] -= 2

    def move_up(self): self.position[1] -= 2

    def move_down(self): self.position[1] += 2

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_img(self, x, y):
        image = pygame.Surface([16, 16])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 16, 16))
        return image