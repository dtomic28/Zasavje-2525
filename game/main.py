import pygame
import os
from pygame.locals import *

#initializacija pygame
pygame.init() 

#ime okna
pygame.display.set_caption("Zasavje 2525")

#čas
clock = pygame.time.Clock()

#Velikost okna v px
WINDOW_SIZE = (400,400)

#Osnovne spremenljivke
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

#najde sliko janez.png v subpath
player_image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets/characters/janez','janez.png')).convert_alpha()

moving_left = False
moving_right = False

player_location = [50,50]
player_y_momentum = 0

player_rect = pygame.Rect(player_location[0], player_location[1], player_image.get_height(), player_image.get_width())
test_rect = pygame.Rect(100,100,100,50)


#GameLOOP
while True: #game loop
    screen.fill((146,244,255))
    screen.blit(player_image, player_location)

    if player_location[1] > WINDOW_SIZE[1]-player_image.get_height():
        player_y_momentum = -player_y_momentum
    else:
        player_y_momentum += 0.2
    player_location[1] += player_y_momentum


    if moving_right == True:
        player_location[0] += 4
    if moving_left == True:
        player_location[0] -= 4

    player_rect.x = player_location[0]
    player_rect.y = player_location[1]
    
    if player_rect.colliderect(test_rect):
        pygame.draw.rect(screen, (255,0,0), test_rect)
    else:
        pygame.draw.rect(screen, (0,0,0), test_rect)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
            

    pygame.display.update()
    clock.tick(60)