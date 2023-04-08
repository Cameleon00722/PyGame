import pygame
import pytmx
import pyscroll

from player import Player

class MenuInventaire:
    def __init__(self, joueur):
        self.joueur = joueur
        self.font = pygame.font.Font(None, 30)
        self.surface = pygame.Surface((200, 400))
        self.surface.set_alpha(200)
        self.surface.fill((255, 255, 255))
        self.rect = self.surface.get_rect()
        self.rect.x = 10
        self.rect.y = 10


    def afficher(self, ecran):
        ecran.blit(self.surface, self.rect)
        y = 10
        for objet in self.joueur.inventaire:
            texte = self.font.render(objet, True, (0, 0, 0))
            ecran.blit(texte, (self.rect.x + 10, self.rect.y + y))
            y += 30

class Game:

    def __init__(self):
        # création fenetre

        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("dungeon heros")
        self.map = "world"
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

        # stocker coffre
        self.coffre = [{"rect": pygame.Rect(obj.x, obj.y, obj.width, obj.height), "touche": False} for obj in tmx_data.objects if obj.name == "coffre"]



        #dessiner le groupe calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=8)
        self.group.add(self.player)

        # créer l'inventaire
        self.menu_inventaire = MenuInventaire(self.player)

        #definir rect de collision d'entrée dans la maison
        enter_house = tmx_data.get_object_by_name('enter_house_red')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)


    def handle_input(self):
        #menu_inventaire = MenuInventaire(self.player)
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_z]:
            self.player.move_up()

        elif pressed[pygame.K_s]:
            self.player.move_down()

        elif pressed[pygame.K_d]:
            self.player.move_right()

        elif pressed[pygame.K_q]:
            self.player.move_left()

        elif pressed[pygame.K_i]:
            print("open inventaire")
            self.menu_inventaire.afficher(self.screen)

    def detecter_coffre_touche(self, sprite):
        for i, coffre in enumerate(self.coffre):
            if not coffre["touche"] and sprite.feet.colliderect(coffre["rect"]):
                coffre["touche"] = True
                return i
        return None

    def switch_house(self):
        self.map = "house"

        # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame("house.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 4


        # stocker collision
        self.walls = []
        for obj in tmx_data.objects:
            if obj.name == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # stocker coffre
        self.coffre = [{"rect": pygame.Rect(obj.x, obj.y, obj.width, obj.height), "touche": False} for obj in
                       tmx_data.objects if obj.name == "coffre"]

        # dessiner le groupe calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=8)
        self.group.add(self.player)

        # Porte de la maison
        enter_house = tmx_data.get_object_by_name("sortie_house_red1")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # Intérieur
        spawn_house_point = tmx_data.get_object_by_name("Spawn_house_red1")
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y - 20


    def switch_world(self):
        self.map = "world"

        # Charger la carte clasique
        tmx_data = pytmx.util_pygame.load_pygame("carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3

        # Les collisions
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner les différents calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # Porte de la maison
        enter_house = tmx_data.get_object_by_name("enter_house_red")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # Intérieur
        spawn_house_point = tmx_data.get_object_by_name("exit_house_red1")
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y + 20

    def update(self):
        self.group.update()

        if self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()

        if self.map == "house" and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_world()

        #verif collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

            indice_coffre_touche = self.detecter_coffre_touche(sprite)
            if indice_coffre_touche is not None:
                print("Coffre n°", indice_coffre_touche, "touché !")
                if indice_coffre_touche == 0:
                    self.player.ajouter_objet("épée")
                    print(self.player.inventaire)


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
