import pygame
from pygame.locals import *


pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen= pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tile based')

# define game variables
tile_size = 25

# load images
backround = pygame.image.load("backround.png")
img1_sun = pygame.image.load("imgsun.png")



class player():
    def __init__(self, x, y):
        img2_guy = pygame.image.load("player.png")
        self.image = pygame.transform.scale(img2_guy,(20,60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        
    def update(self):
        dx = 0 
        dy = 0
        
        # get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            dy = -5
            self.vel_y +=5
        if key[pygame.K_LEFT]:
            dx -=5
        if key[pygame.K_RIGHT]:
            dx +=5
        
        # add gravity
        if self.vel_y >0: 
            self.vel_y -= 1
            dy += 1
        # check for collision 
        
        # update player coordinates
        self.rect.x += dx
        self.rect.y += dy
        
        # # the player onto screen
        screen.blit(self.image,self.rect)
        
        
    
class World():
   def __init__(self, data):
       self.tile_list = []
       
    #  load images
       sand_cube_img = pygame.image.load("sand_cube.png")
       grass_img = pygame.image.load("grass.png")
       
       Number_of_row = 0
       for row in data:
           number_of_col = 0
           for tile in row:
               if tile == 1:
                   img = pygame.transform.scale(sand_cube_img, (tile_size, tile_size))
                   img_rect = img.get_rect()
                   img_rect.x = number_of_col * tile_size
                   img_rect.y = Number_of_row * tile_size
                   tile = (img, img_rect)
                   self.tile_list.append(tile)
                
               if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = number_of_col * tile_size
                    img_rect.y = Number_of_row * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
               number_of_col += 1
           Number_of_row +=1
               
        
        
   def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


player = player(50, SCREEN_HEIGHT -80)
world = World(world_data)

run = True
while run:

    screen.blit(backround , (0,0))
    screen.blit(img1_sun , (60,60))

    player.update()
    world.draw()
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

