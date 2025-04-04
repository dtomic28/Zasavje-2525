import pygame, sys, os, random

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
player_score = 0
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

class coin():
    def __init__(self, x_pos,y_pos, x_size, y_size, colider, coin_alive):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_size = x_size
        self.y_size = y_size
        self.colider = colider
        self.coin_alive = coin_alive

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

class coin():
    def __init__(self, x_pos,y_pos, x_size, y_size, colider, coin_alive):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_size = x_size
        self.y_size = x_size
        self.colider = colider
        self.coin_alive = coin_alive

class tank():
    def __init__(self,tank_x_pos,tank_y_pos,tank_width,tank_height, tank_action,tank_frame,tank_flip,tank_movement_x,tank_movement_y,tank_alive,tank_hp):
        self.tank_x_pos = tank_x_pos
        self.tank_y_pos = tank_y_pos
        self.tank_width = tank_width
        self.tank_height = tank_height
        self.tank_action = tank_action
        self.tank_frame = tank_frame
        self.tank_flip = tank_flip
        self.tank_movement_x = tank_movement_x
        self.tank_movement_y = tank_movement_y
        self.tank_alive = tank_alive
        self.tank_hp = tank_hp

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
animation_database["tank_walk"] = load_animation('game/assets/characters/tank/tank_walk', [0, 1, 2,3,4,5,6,7,8,9,10,11])

game_map = load_map('map')

grass_img = pygame.image.load('grass.png')
dirt_img = pygame.image.load('dirt.png')
coin_img = pygame.image.load("coin.png")

player_action = 'player_idle'
player_frame = 0
player_flip = False
player_score = 0


player_rect = pygame.Rect(100,100,48,96)


rudar_sez=[]
lučkar_sez=[]
tank_sez=[]
tile_rects = []
coin_sez = []
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
    global player_rect,moving_right,moving_left,vertical_momentum,player_action,player_frame,air_timer,player_flip, load_map_timer,tile_rects, player_score,coin_img,coin_sez

    while(1): # game loop
        display.fill((76,0,150)) # clear screen by filling it with blue
        y = 0
        for layer in game_map:
            x = 0
            if player_rect.y+800 > y*64:
                for tile in layer:
                    if load_map_timer == 0:
                        if tile == "1" or tile == "2":
                            tile_rects.append(pygame.Rect(x*64,y*64,64,64))
                    if player_rect.x+1200 > x*64:
                        if tile == '1':
                            display.blit(dirt_img,(x*64-scroll[0],y*64-scroll[1]))
                        if tile == '2':
                            display.blit(grass_img,(x*64-scroll[0],y*64-scroll[1]))
                    if load_map_timer == 0:
                        if tile == "l":
                            lučkar1 = lučkar(x * 64-32, y * 64-32, 48, 96, "lučkar_walk", 0, False, 0, 0, True, 180, 0)
                            lučkar_sez.append(lučkar1)
                        if tile == "r":
                            rudar1 = rudar(x * 64-32, y * 64-32, 48, 96, "rudar_walk", 0, False, 0, 0, True)
                            rudar_sez.append(rudar1)
                        if tile == "t":
                            tank1 = tank(x * 64-32, y * 64-32, 54, 96, "tank_walk", 0, False, 0, 0, True,3)
                            tank_sez.append(tank1)
                        if tile == "c":
                            coin1 = coin(x * 64, y * 64 - 32, 16, 16, (x * 64, y * 64 - 32, 16, 16), True)
                            coin_sez.append(coin1)
                    x += 1

            y += 1
        load_map_timer = 1

        scroll[0] += (player_rect.x-scroll[0] - (500+16))/20
        scroll[1] = -200

        for coins in coin_sez:
            if coins.coin_alive == True:
                pickup_test = player_rect.colliderect(coins.colider)
                display.blit(coin_img, (coins.x_pos - scroll[0], coins.y_pos - scroll[1]))
                if pickup_test == True:
                    coins.colider = (0, 0, 0, 0)
                    player_score += 1
                    coins.coin_alive = False
                    print(player_score)

        for rudars in rudar_sez:
            if rudars.rudar_alive == True:
                rudars.rudar_movement_y += 1
                rudar_rects = pygame.Rect(rudars.rudar_x_pos,rudars.rudar_y_pos,48,96)
                top_colider = pygame.Rect(rudars.rudar_x_pos, rudars.rudar_y_pos, 48, 48)
                if player_rect.x + 1200 > rudar_rects.x:
                    if rudars.rudar_x_pos > player_rect.x+50:
                        rudars.rudar_action, rudars.rudar_frame = change_action(rudars.rudar_action,rudars.rudar_frame, "rudar_walk")
                        rudars.rudar_flip = True
                        rudars.rudar_movement_x = -1
                    elif rudars.rudar_x_pos < player_rect.x-50:
                        rudars.rudar_action, rudars.rudar_frame = change_action(rudars.rudar_action, rudars.rudar_frame,"rudar_walk")
                        rudars.rudar_flip = False
                        rudars.rudar_movement_x = 1
                rudar_rects, collisions = move(rudar_rects, [rudars.rudar_movement_x,rudars.rudar_movement_y], tile_rects)
                if collisions["bottom"] == True:
                    rudars.rudar_movement_y = 0
                if rudar_rects.y > 800:
                    rudars.rudar_alive = False
                if player_rect.x + 1200 > rudar_rects.x:
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
                    rudar_test_left_middle = player_rect.collidepoint(top_colider.midleft)
                    rudar_test_right_middle = player_rect.collidepoint(top_colider.midright)
                    if rudar_test_top_left == True or rudar_test_top_right == True:
                        rudars.rudar_alive = False
                    if rudar_test_top_left == True and rudar_test_left_middle == True or rudar_test_top_right == True and rudar_test_right_middle == True:
                        rudars.rudar_alive = True
                    if rudars.rudar_alive == False:
                        vertical_momentum = -15
                        rudar_rects = pygame.Rect(0, 0, 0, 0)

        for lučkars in lučkar_sez:
            if lučkars.lučkar_alive == True:
                lučkars.lučkar_movement_y += 1
                lučkar_rects = pygame.Rect(lučkars.lučkar_x_pos,lučkars.lučkar_y_pos,48,96)
                if player_rect.x + 1200 > lučkar_rects.x:
                    if lučkars.lučkar_x_pos > player_rect.x+50 and lučkars.lučkar_attack_timer == 0:
                        lučkars.lučkar_action, lučkars.lučkar_frame = change_action(lučkars.lučkar_action,lučkars.lučkar_frame, "lučkar_walk")
                        lučkars.lučkar_flip = True
                        lučkars.lučkar_movement_x = -1
                        lučkars.lučkar_wait_timer -= 1
                    elif lučkars.lučkar_x_pos < player_rect.x-50 and lučkars.lučkar_attack_timer == 0:
                        lučkars.lučkar_action, lučkars.lučkar_frame = change_action(lučkars.lučkar_action, lučkars.lučkar_frame,"lučkar_walk")
                        lučkars.lučkar_flip = False
                        lučkars.lučkar_movement_x = 1
                        lučkars.lučkar_wait_timer -= 1
                    elif lučkars.lučkar_attack_timer !=0:
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
                if player_rect.x + 1200 > lučkar_rects.x:
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
                    if lučkar_test_top_left == True or lučkar_test_top_right == True:
                        lučkars.lučkar_alive = False
                        vertical_momentum = -15

        for tanks in tank_sez:
            if tanks.tank_alive == True:
                tanks.tank_movement_y += 1
                tank_rects = pygame.Rect(tanks.tank_x_pos,tanks.tank_y_pos,54,96)
                if player_rect.x + 1200 > tank_rects.x:
                    if tanks.tank_x_pos > player_rect.x+50:
                        tanks.tank_action, tanks.rudar_frame = change_action(tanks.tank_action,tanks.tank_frame, "tank_walk")
                        tanks.tank_flip = True
                        tanks.tank_movement_x = -0.5
                    elif tanks.tank_x_pos < player_rect.x-50:
                        tanks.tank_action, tanks.tank_frame = change_action(tanks.tank_action, tanks.tank_frame,"tank_walk")
                        tanks.tank_flip = False
                        tanks.tank_movement_x = 0.5
                tank_rects, collisions = move(tank_rects, [tanks.tank_movement_x,tanks.tank_movement_y], tile_rects)
                if collisions["bottom"] == True:
                    tanks.tank_movement_y = 0
                if player_rect.x + 1200 > tank_rects.x:
                    if collisions["left"] == True or collisions["right"] == True:
                        tanks.tank_movement_x = 0
                    tanks.tank_x_pos += tanks.tank_movement_x
                    tanks.tank_y_pos += tanks.tank_movement_y
                    tanks.tank_frame += 1
                    if tanks.tank_frame >= len(animation_database[tanks.tank_action]):
                        tanks.tank_frame = 0
                    tank_id = animation_database[tanks.tank_action][tanks.tank_frame]
                    tank_img = animation_frames[tank_id]
                    display.blit(pygame.transform.flip(tank_img, tanks.tank_flip, False),(tanks.tank_x_pos - scroll[0], tanks.tank_y_pos - scroll[1]))
                    tank_test_top_left = player_rect.collidepoint(tank_rects.topleft)
                    tank_test_top_right = player_rect.collidepoint(tank_rects.topright)
                    if tank_test_top_left == True or tank_test_top_right == True:
                        tanks.tank_hp -= 1
                        vertical_momentum = -15
                    if tanks.tank_hp == 0:
                        tanks.tank_alive = False

        if moving_right == True:
            player_movement[0] += 5
        if moving_left == True:
            player_movement[0] -= 5
        player_movement[1] += vertical_momentum
        vertical_momentum += 0.5
        if vertical_momentum > 100:
            vertical_momentum = 100

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
                    if air_timer < 3:
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

""" menu = pygame_menu.Menu(800, 100, 'Zasavje 2525: Maščevanje Janeza',
                       theme=pygame_menu.themes.THEME_DARK)

menu.add.text_input('Ime :', default='Janez Novak')
menu.add.button('Igraj', main)
menu.add.button('Izhod', pygame_menu.events.EXIT)

menu.mainloop(screen) """

main()