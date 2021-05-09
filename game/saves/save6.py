import pygame, sys, os, random, pygame_menu

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init() # initiates pygame

pygame.display.set_caption('Pygame Platformer')

WINDOW_SIZE = (1200,800)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

display = pygame.Surface((1200,800)) # used as the surface for rendering, which is scaled

player_jump = False
moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0

scroll = [0,0]

class rudar():
    def __init__(self,rudar_x_pos,rudar_y_pos,rudar_width,rudar_height, rudar_action,rudar_frame,rudar_flip,rudar_movement_x,rudar_movement_y,rudar_alive):
        self.rudar_x_pos=rudar_x_pos
        self.rudar_y_pos=rudar_y_pos
        self.rudar_width= rudar_width
        self.rudar_height =rudar_height
        self.rudar_action =rudar_action
        self.rudar_frame = rudar_frame
        self.rudar_flip = rudar_flip
        self.rudar_movement_x = rudar_movement_x
        self.rudar_movement_y = rudar_movement_y
        self.rudar_alive = rudar_alive

class lučkar():
    def __init__(self,lučkar_x_pos,lučkar_y_pos,lučkar_width,lučkar_height, lučkar_action,lučkar_frame,lučkar_flip,lučkar_movement_x,lučkar_movement_y,lučkar_alive,lučkar_wait_timer,lučkar_attack_timer):
        self.lučkar_x_pos=lučkar_x_pos
        self.lučkar_y_pos=lučkar_y_pos
        self.lučkar_width= lučkar_width
        self.lučkar_height =lučkar_height
        self.lučkar_action =lučkar_action
        self.lučkar_frame = lučkar_frame
        self.lučkar_flip = lučkar_flip
        self.lučkar_movement_x = lučkar_movement_x
        self.lučkar_movement_y = lučkar_movement_y
        self.lučkar_alive =lučkar_alive
        self.lučkar_wait_timer = lučkar_wait_timer
        self.lučkar_attack_timer = lučkar_attack_timer

def load_map(path):
    f = open("game/"+path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

global animation_frames
animation_frames = {}

def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        print(img_loc)
        animation_image = pygame.image.load(img_loc)
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame
        

animation_database = {}

animation_database['player_walk'] = load_animation('game/assets/characters/janez/player_walk', [0, 1, 2, 3, 4,5,6,7])
animation_database['player_idle'] = load_animation('game/assets/characters/janez/player_idle', [1, 1])
animation_database['rudar_walk'] = load_animation('game/assets/characters/rudar/rudar_walk', [0, 1,2,3,4,5,6,7])
animation_database['rudar_attack'] = load_animation('game/assets/characters/rudar/rudar_attack', [0, 1, 2, 3])
animation_database["lučkar_walk"] = load_animation('game/assets/characters/lučkar/lučkar_walk', [0, 1, 2,3,4,5,6,7])
animation_database["lučkar_attack"] = load_animation('game/assets/characters/lučkar/lučkar_attack', [0, 1, 2,3,4,5,6,7,8,9,10])

game_map = load_map('map')

grass_img = pygame.image.load('grass.png')
dirt_img = pygame.image.load('dirt.png')

player_action = 'player_idle'
player_frame = 0
player_flip = False

#test = 0

player_rect = pygame.Rect(100,100,48,96)

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]

"""
NOTE: če tuki daš unused rudarja se naredi bug, k randomly floata

"""

rudar_sez=[]
lučkar_sez=[]
load_map_timer = 0

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types



def main():
    global player_rect,moving_right,moving_left,vertical_momentum,player_action,player_frame,air_timer,player_flip, load_map_timer

    while True: # game loop
        display.fill((76,0,150)) # clear screen by filling it with blue
        tile_rects = []
        y = 0
        for layer in game_map:
            x = 0
            for tile in layer:
                if tile == '1':
                    display.blit(dirt_img,(x*64-scroll[0],y*64-scroll[1]))
                if tile == '2':
                    display.blit(grass_img,(x*64-scroll[0],y*64-scroll[1]))
                if tile != '0' and tile != "l" and tile != "r":
                    tile_rects.append(pygame.Rect(x*64,y*64,64,64))
                if load_map_timer == 0:
                    if tile == "l":
                        lučkar1 = lučkar(x * 64, y * 64, 48, 96, "lučkar_walk", 0, False, 0, 0, True, 180, 0)
                        lučkar_sez.append(lučkar1)
                    if tile == "r":
                        rudar1 = rudar(x * 64, y * 64, 48, 96, "rudar_walk", 0, False, 0, 0, True)
                        rudar_sez.append(rudar1)
                x += 1
            y += 1
        load_map_timer = 1

        scroll[0] += (player_rect.x-scroll[0] - (500+16))/20
        scroll[1] += (player_rect.y - scroll[1] - (200 + 16)) / 30


        for rudars in rudar_sez:
            if rudars.rudar_alive == True:
                rudars.rudar_movement_y += 1
                rudar_rects = pygame.Rect(rudars.rudar_x_pos,rudars.rudar_y_pos,48,96)
                if rudars.rudar_x_pos > player_rect.x+50:
                    rudars.rudar_action, rudars.rudar_frame = change_action(rudars.rudar_action,rudars.rudar_frame, "rudar_walk")
                    rudars.rudar_flip = True
                    rudars.rudar_movement_x = -1
                if rudars.rudar_x_pos < player_rect.x-50:
                    rudars.rudar_action, rudars.rudar_frame = change_action(rudars.rudar_action, rudars.rudar_frame,"rudar_walk")
                    rudars.rudar_flip = False
                    rudars.rudar_movement_x = 1
                if rudars.rudar_x_pos-player_rect.x > 0 and rudars.rudar_x_pos-player_rect.x < 50:
                    rudars.rudar_action, rudars.rudar_frame = change_action(rudars.rudar_action, rudars.rudar_frame,"rudar_attack")
                    rudars.rudar_flip = True
                    rudars.rudar_movement_x = 0
                if rudars.rudar_x_pos-player_rect.x < 0 and rudars.rudar_x_pos-player_rect.x > -50:
                    rudars.rudar_action, rudars.rudar_frame = change_action(rudars.rudar_action, rudars.rudar_frame,"rudar_attack")
                    rudars.rudar_flip = False
                    rudars.rudar_movement_x = 0
                rudar_rects, collisions = move(rudar_rects, [rudars.rudar_movement_x,rudars.rudar_movement_y], tile_rects)
                if collisions["bottom"] == True:
                    rudars.rudar_movement_y = 0
                if collisions["left"] == True or collisions["right"] == True:
                    rudars.rudar_movement_x = 0
                rudars.rudar_x_pos += rudars.rudar_movement_x
                rudars.rudar_y_pos += rudars.rudar_movement_y
                rudars.rudar_frame += 1
                if rudars.rudar_frame >= len(animation_database[rudars.rudar_action]):
                    rudars.rudar_frame = 0
                rudar_id = animation_database[rudars.rudar_action][rudars.rudar_frame]
                rudar_img = animation_frames[rudar_id]
                display.blit(pygame.transform.flip(rudar_img, rudars.rudar_flip, False),(rudars.rudar_x_pos - scroll[0], rudars.rudar_y_pos - scroll[1]))
                rudar_test_top_left = player_rect.collidepoint(rudar_rects.topleft)
                rudar_test_top_right = player_rect.collidepoint(rudar_rects.topright)
                if rudar_test_top_left == True or rudar_test_top_right:
                    rudars.rudar_alive = False
                    vertical_momentum = -15

            else:
                rudar_rects=pygame.Rect(0,0,0,0)

        for lučkars in lučkar_sez:
            if lučkars.lučkar_alive == True:
                lučkars.lučkar_movement_y += 1
                lučkar_rects = pygame.Rect(lučkars.lučkar_x_pos,lučkars.lučkar_y_pos,48,96)
                if lučkars.lučkar_x_pos > player_rect.x+50 and lučkars.lučkar_attack_timer == 0:
                    lučkars.lučkar_action, lučkars.lučkar_frame = change_action(lučkars.lučkar_action,lučkars.lučkar_frame, "lučkar_walk")
                    lučkars.lučkar_flip = True
                    lučkars.lučkar_movement_x = -1
                    lučkars.lučkar_wait_timer -= 1
                if lučkars.lučkar_x_pos < player_rect.x-50 and lučkars.lučkar_attack_timer == 0:
                    lučkars.lučkar_action, lučkars.lučkar_frame = change_action(lučkars.lučkar_action, lučkars.lučkar_frame,"lučkar_walk")
                    lučkars.lučkar_flip = False
                    lučkars.lučkar_movement_x = 1
                    lučkars.lučkar_wait_timer -= 1
                if lučkars.lučkar_attack_timer !=0:
                    lučkars.lučkar_action, lučkars.lučkar_frame = change_action(lučkars.lučkar_action, lučkars.lučkar_frame,"lučkar_attack")
                    if lučkars.lučkar_x_pos > player_rect.x:
                        lučkars.lučkar_movement_x = -3
                    else:
                        lučkars.lučkar_movement_x = 3
                    if lučkars.lučkar_movement_x > 0:
                        lučkars.lučkar_flip = False
                    else:
                        lučkars.lučkar_flip = True
                    lučkars.lučkar_attack_timer-=1

                if lučkars.lučkar_wait_timer == 0:
                    lučkars.lučkar_wait_timer = 180
                    lučkars.lučkar_attack_timer = 60
                lučkar_rects, collisions = move(lučkar_rects, [lučkars.lučkar_movement_x,lučkars.lučkar_movement_y], tile_rects)
                if collisions["bottom"] == True:
                    lučkars.lučkar_movement_y = 0
                if collisions["left"] == True or collisions["right"] == True:
                    lučkars.lučkar_movement_x = 0
                lučkars.lučkar_x_pos += lučkars.lučkar_movement_x
                lučkars.lučkar_y_pos += lučkars.lučkar_movement_y
                lučkars.lučkar_frame += 1
                if lučkars.lučkar_frame >= len(animation_database[lučkars.lučkar_action]):
                    lučkars.lučkar_frame = 0
                lučkar_id = animation_database[lučkars.lučkar_action][lučkars.lučkar_frame]
                lučkar_img = animation_frames[lučkar_id]
                display.blit(pygame.transform.flip(lučkar_img, lučkars.lučkar_flip, False),(lučkars.lučkar_x_pos - scroll[0], lučkars.lučkar_y_pos - scroll[1]))
                lučkar_test_top_left = player_rect.collidepoint(lučkar_rects.topleft)
                lučkar_test_top_right = player_rect.collidepoint(lučkar_rects.topright)
                if lučkar_test_top_left == True or lučkar_test_top_right:
                    lučkars.lučkar_alive = False
                    vertical_momentum = -15

            else:
                lučkar_rects=pygame.Rect(0,0,0,0)

        player_movement = [0,0]
        if moving_right == True:
            player_movement[0] += 5
        if moving_left == True:
            player_movement[0] -= 5
        player_movement[1] += vertical_momentum
        vertical_momentum += 0.5
        if vertical_momentum > 7:
            vertical_momentum = 7

        if player_movement[0] == 0:
            player_action,player_frame = change_action(player_action,player_frame,'player_idle')
        if player_movement[0] > 0:
            player_flip = False
            player_action,player_frame = change_action(player_action,player_frame,'player_walk')
        if player_movement[0] < 0:
            player_flip = True
            player_action,player_frame = change_action(player_action,player_frame,'player_walk')

        player_rect,collisions = move(player_rect,player_movement,tile_rects)

        if collisions['bottom'] == True:
            air_timer = 0
            vertical_momentum = 0
        else:
            air_timer += 1

        player_frame += 1
        if player_frame >= len(animation_database[player_action]):
            player_frame = 0
        player_img_id = animation_database[player_action][player_frame]
        player_img = animation_frames[player_img_id]
        display.blit(pygame.transform.flip(player_img,player_flip,False),(player_rect.x-scroll[0],player_rect.y-scroll[1]))

        for event in pygame.event.get(): # event loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    moving_right = True
                if event.key == K_LEFT:
                    moving_left = True
                if event.key == K_UP:
                    if air_timer < 6:
                        vertical_momentum = -15

            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    moving_right = False
                if event.key == K_LEFT:
                    moving_left = False
        player_jump = False
        #test+=1
        screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
        pygame.display.update()
        clock.tick(60)

menu = pygame_menu.Menu(800, 1200, 'Welcome',
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Name :', default='John Doe')
menu.add.button('Play', main)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(screen)