import pygame

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

screen= pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tile based')


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

