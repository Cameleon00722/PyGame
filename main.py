import pygame

import player
from game import Game, MenuInventaire

if __name__ == '__main__':
    pygame.init()
    game = Game()
    menu_inventaire = MenuInventaire(player)
    game.run()
