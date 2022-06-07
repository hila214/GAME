from pickle import FALSE
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
fps = 50


screen= pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tile based')

# define font
font_score = pygame.font.SysFont('Bauhaus 93' , 30)

# define game variables
tile_size = 25
game_over = 0
main_menu = True
score = 0

# define colors
black = (0, 0, 0)

# load images
backround = pygame.image.load("backround.png")
img1_sun = pygame.image.load("imgsun.png")
restart_img = pygame.image.load("restart_game.png")
start_img = pygame.image.load("start.png")
exit_img = pygame.image.load("exit.png")


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))




# image for its will be button that restart the game
class Button():
    def __init__(self, x, y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False


    def draw(self):
        action = False

        # get mouse place
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
           if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
               action = True
               self.clicked = True

           if pygame.mouse.get_pressed()[0] == 0:
               self.clicked = False

        # draw button
        screen.blit(self.image , self.rect)

        return action
        
    


class player():
    def __init__(self, x, y):
        self.reset(x , y)
        
    def update(self, game_over):
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
        
        
        if game_over == 0:
            #get keypresses
            key = pygame.key.get_pressed()
            if (key[pygame.K_SPACE] or hand_up) and self.jumped == False and self.in_air == False:
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

            self.in_air = True
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
                        self.in_air = False



            #check for collision with enemies
            if pygame.sprite.spritecollide(self, monster_group, False):
                game_over = -1

            #check for collision with lava
            if pygame.sprite.spritecollide(self, Lava_group, False):
                game_over = -1

            #update player coordinates
            self.rect.x += dx
            self.rect.y += dy
            
        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 100:
                self.rect.y -= 5


        #draw player onto screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        
        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f'img.guy{num}.png')
            img_right = pygame.transform.scale(img_right, (20, 60))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('ghost.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True


        
        
    
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
               if tile == 6:
                    lava = Lava(number_of_col * tile_size, Number_of_row * tile_size + (tile_size// 2))
                    Lava_group.add(lava)
               if tile == 7:
                   coin = Coin(number_of_col * tile_size + (tile_size // 2), Number_of_row * tile_size + (tile_size// 2))
                   Coin_group.add(coin)


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
        # pygame.draw.rect(screen,white, self.rect)


class Lava(pygame.sprite.Sprite):
   def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        lava_img = pygame.image.load("lava.png")
        self.image = pygame.transform.scale(lava_img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Coin(pygame.sprite.Sprite):
   def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        lava_img = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(lava_img, (tile_size  // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    


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


player = player(60, SCREEN_HEIGHT -130)

monster_group = pygame.sprite.Group()
Lava_group = pygame.sprite.Group()
Coin_group = pygame.sprite.Group()

world = World(world_data)

#create buttons
restart_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 100 , restart_img)
start_button = Button(SCREEN_WIDTH // 2 - 190, SCREEN_HEIGHT // 2, start_img)
exit_button = Button(SCREEN_WIDTH // 2 + 80, SCREEN_HEIGHT // 2, exit_img)


run = True
while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    ret, frame = vid.read()
    clock.tick(fps)

    screen.blit(backround , (0,0))
    screen.blit(img1_sun , (60,60))

    if main_menu == True:
      if exit_button.draw():
          run = False
      if start_button.draw():
          main_menu = False

    else:
        world.draw()
        
        if game_over == 0:
         monster_group.update()
        # update score
        # check if a coin has been collected
        if pygame.sprite.spritecollide(player, Coin_group, True):
            score += 1
        draw_text('SCORE: X' + str(score), font_score, black, tile_size - 10, 10)

        
        monster_group.draw(screen)
        Lava_group.draw(screen)
        Coin_group.draw(screen)
        
        game_over = player.update(game_over)
        
        #if player has died
        if game_over == -1:
         if  restart_button.draw():
            player.reset(100, SCREEN_HEIGHT -130)
            game_over = 0 
            score = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    
    
    # print(player.rect.x)
    # print(player.rect.x /500*20//1)
    # print(player.rect.y /500*20//1+2)
    
            
            

    pygame.display.update()

pygame.quit()

