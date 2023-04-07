import pygame

pygame.init()

# création fenetre

pygame.display.set_mode((800, 600))
pygame.display.set_caption("Elder Quest")

# boucle du jeu

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
