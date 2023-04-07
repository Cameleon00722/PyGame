import pygame
import pytmx
import pyscroll

from player import Player


class Game:

    def __init__(self):
        # création fenetre

        self.screen = pygame.display.set_mode((900, 600))
        pygame.display.set_caption("dungeon heros")
        print("sa init")

        #charger la carte
        tmx_data = pytmx.util_pygame.load_pygame("carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3

        #generer joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        #stocker collision
        self.walls = []
        for obj in tmx_data.objects:
            if obj.name == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))


        #dessiner le groupe calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=8)
        self.group.add(self.player)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()

        elif pressed[pygame.K_DOWN]:
            self.player.move_down()

        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()

        elif pressed[pygame.K_LEFT]:
            self.player.move_left()

    def update(self):
        self.group.update()

        #verif collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):

        clock = pygame.time.Clock()
        # boucle du jeu

        running = True

        while running:

            self.player.save_loc()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(60)

        pygame.quit()
