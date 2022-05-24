import pygame
from pygame.locals import *
import cv2
import mediapipe as mp

vid = cv2.VideoCapture(0)
mp_Hands = mp.solutions.hands
hands = mp_Hands.Hands()
mpDraw = mp.solutions.drawing_utils

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
clock = pygame.time.Clock()
fps = 60


screen= pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tile based')

# define game variables
tile_size = 25

# load images
backround = pygame.image.load("backround.png")
img1_sun = pygame.image.load("imgsun.png")



class player():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1 ,5):
            img_right = pygame.image.load(f'img.guy{num}.png')
            img_right = pygame.transform.scale(img_right,(20,60))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        # self.data = data
        
    def update(self):
        dx = 0 
        dy = 0
        walk_cooldown = 5
        hand_up = False

        ret, frame = vid.read()
        index_finger_x = 0
        RGB_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(RGB_image)
        multiLandMarks = results.multi_hand_landmarks
        if multiLandMarks:
            for handLms in multiLandMarks:
                mpDraw.draw_landmarks(frame, handLms, mp_Hands.HAND_CONNECTIONS)
            index_finger_x = multiLandMarks[0].landmark[8].x
            index_finger_y = multiLandMarks[0].landmark[8].y
            index_finger_5 = multiLandMarks[0].landmark[5].y

            if index_finger_y > index_finger_5:
                print("down")

            else:
                hand_up = True
                print("up")
                
                
            
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return

        
        key = pygame.key.get_pressed()
        if (key[pygame.K_SPACE] or hand_up) and self.jumped == False :
            self.vel_y = -15
            self.jumped = True
        if key[pygame.K_SPACE] == False:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 5
            self.counter += 1
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += 5
            self.counter += 1
            self.direction = 1
        if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]


        #handle animation
        if self.counter > walk_cooldown:
            self.counter = 0    
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]


        #add gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        #check for collision
        for tile in world.tile_list:
            #check for collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            #check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground i.e. jumping
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                #check if above the ground i.e. falling
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0




        #update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            dy = 0

        #draw player onto screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        
        
    
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
               if tile == 3:
                    monster = Enemy(number_of_col * tile_size  ,Number_of_row * tile_size +10)
                    monster_group.add(monster)
               number_of_col += 1
           Number_of_row +=1
               
        
        
   def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('monster.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

        
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
        # pygame.draw.rect(screen, white, self.rect)




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

# print(len(world_data[0]))
# quit()

player = player(100, SCREEN_HEIGHT -130)
monster_group = pygame.sprite.Group()
world = World(world_data)

run = True
while run:
    ret, frame = vid.read()
    screen.blit(backround , (0,0))
    screen.blit(img1_sun , (60,60))

    player.update()
    
    world.draw()
    monster_group.update()
    
    monster_group.draw(screen)
    clock.tick(fps)

    print(player.rect.x)
    print(player.rect.x /500*20//1)
    print(player.rect.y /500*20//1+2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
            

    pygame.display.update()

pygame.quit()

