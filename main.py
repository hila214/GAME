import pygame
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

screen= pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tile based')

SIZE_SQUARE = 200

backround = pygame.image.load("backround.png")
img1_sun = pygame.image.load("imgsun.png")

def draw_Map():
    for line in range(0, 6):
        pygame.draw.line(screen, (255, 255, 255), (0, line * SIZE_SQUARE), (SCREEN_WIDTH, line * SIZE_SQUARE))
        pygame.draw.line(screen, (255, 255, 255), (line * SIZE_SQUARE, 0), (line * SIZE_SQUARE, SCREEN_HEIGHT))

class Game():
   def __init__(self, data):
       Sand =pygame.image.load("sand_cube.png")

       for line in data:
           for SQUARE in line:
               if SQUARE ==1 :
                   img2 = pygame.transform.scale(Sand, (SIZE_SQUARE, SIZE_SQUARE))

THE_GAME_WORLD = [
[1, 1, 1, 1, 1],
[1, 0, 0, 0, 1],
[1, 0, 0, 0, 1],
[1, 0, 0, 0, 1],
[1, 1, 1, 1, 1],
]




run = True
while run:

    screen.blit(backround , (0,0))
    screen.blit(img1_sun , (100,80))

    draw_Map()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

