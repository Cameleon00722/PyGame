import math

import pygame
import pytmx
import pyscroll

from monstre import Monstre
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

        self.screen = pygame.display.set_mode((900, 600))
        pygame.display.set_caption("dungeon heros")
        self.map = "world"

        # gestion bande son
        pygame.mixer.init()
        pygame.mixer.music.load("normal.mp3")
        # pygame.mixer.music.play(-1)

        # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame("carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3

        # generer joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        self.zone_degats_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())

        self.liste_monstres = []
        for monstre_position in tmx_data.objects:
            if monstre_position.name == "mob1":
                monstre = Monstre(monstre_position.x, monstre_position.y)
                self.liste_monstres.append(monstre)

        # stocker collision
        self.walls = []
        for obj in tmx_data.objects:
            if obj.name == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # stocker coffre
        self.coffre = [{"rect": pygame.Rect(obj.x, obj.y, obj.width, obj.height), "touche": False} for obj in
                       tmx_data.objects if obj.name == "coffre"]

        # dessiner le groupe calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=7)
        self.group.add(self.player)
        # self.group.add(self.zone_degats_layer)

        for monstre in self.liste_monstres:
            self.group.add(monstre)

        # créer l'inventaire
        self.menu_inventaire = MenuInventaire(self.player)

        # definir rect de collision d'entrée dans la maison
        enter_house = tmx_data.get_object_by_name('enter_house_red')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

    def handle_input(self):

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
            self.menu_inventaire.afficher(self.screen)

        elif pressed[pygame.K_f]:

            zone_degats = pygame.Rect(self.player.rect.x + self.player.rect.width, self.player.rect.y, 100,
                                      self.player.rect.height)

            # self.zone_degats_layer.surface.fill((0, 0, 0, 0))  # Effacer le calque
            # pygame.draw.rect(self.zone_degats_layer.surface, (255, 0, 0), zone_degats)

            # print("attack")
            for monstre in self.liste_monstres:
                if monstre.rect.colliderect(zone_degats):
                    monstre.subir_degats()
                    if monstre.vie <= 0:
                        # print("c'est un kill")
                        monstre.kill()
                        monstre.remove()
                        monstre.status = "dead"

    def detecter_coffre_touche(self, sprite):
        for i, coffre in enumerate(self.coffre):
            if not coffre["touche"] and sprite.feet.colliderect(coffre["rect"]):
                coffre["touche"] = True
                return i
        return None

    @staticmethod
    def sound(name):
        if name == "normal":
            pygame.mixer.music.load("normal.mp3")
            pygame.mixer.music.play(-1)
        elif name == "fight":
            # pygame.mixer.music.stop()
            pygame.mixer.music.load("Fight.mp3")
            pygame.mixer.music.play(-1)
        elif name == "boss":
            pygame.mixer.music.stop()
            pygame.mixer.music.load("DragonBorn.mp3")
            pygame.mixer.music.play(-1)

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
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=7)
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
            if obj.name == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner les différents calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
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
        self.player.check_invincibility()

        if self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()

        if self.map == "house" and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_world()

        if self.player.status == "dead":
            self.player.dead()

        for monstre in self.liste_monstres:

            if self.player.rect.colliderect(monstre.rect) and monstre.status != "dead":
                # collision détectée entre le joueur et le monstre
                self.player.take_damage()

            distance = math.sqrt(
                (self.player.rect.x - monstre.rect.x) ** 2 + (self.player.rect.y - monstre.rect.y) ** 2)

            # Si le joueur est à une distance de 10x/10y du monstre
            if distance <= 80 and monstre.status != "dead":

                # Calculer la direction vers laquelle le monstre doit se déplacer
                delta_x = self.player.rect.x - monstre.rect.x
                delta_y = self.player.rect.y - monstre.rect.y
                if abs(delta_x) > abs(delta_y):
                    if delta_x > 0:
                        monstre.move_right()
                    else:
                        monstre.move_left()
                else:
                    if delta_y > 0:
                        monstre.move_down()
                    else:
                        monstre.move_up()
            else:
                pass

        # verif collision
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
        # self.sound("normal")

        while running:

            self.player.save_loc()
            for monstre in self.liste_monstres:
                monstre.save_loc()
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
