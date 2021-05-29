import pygame, sys, random, pygame_menu

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

font = pygame.font.SysFont("calibri", 32)

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

class end():
    def __init__(self,end_x_pos,end_y_pos,end_x_size,end_y_size,end_rect):
        self.end_x_pos = end_x_pos
        self.end_y_pos = end_y_pos
        self.end_x_size = end_x_size
        self.end_y_size = end_y_size
        self.end_rect = end_rect

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

class boss():
    def __init__(self,boss_x_pos,boss_y_pos,boss_width,boss_height, boss_action,boss_frame,boss_flip,boss_movement_x,boss_movement_y,boss_alive,boss_hp):
        self.boss_x_pos = boss_x_pos
        self.boss_y_pos = boss_y_pos
        self.boss_width = boss_width
        self.boss_height = boss_height
        self.boss_action = boss_action
        self.boss_frame = boss_frame
        self.boss_flip = boss_flip
        self.boss_movement_x = boss_movement_x
        self.boss_movement_y = boss_movement_y
        self.boss_alive = boss_alive
        self.boss_hp = boss_hp

class jump_pad():
    def __init__(self,jump_pad_x_pos,jump_pad_y_pos,jump_pad_rect,jump_pad_cd):
        self.jump_pad_x_pos = jump_pad_x_pos
        self.jump_pad_y_pos = jump_pad_y_pos
        self.jump_pad_rect = jump_pad_rect
        self.jump_pad_cd = jump_pad_cd

class teleport_pad_up():
    def __init__(self,teleport_pad_up_x_pos,teleport_pad_up_y_pos,teleport_pad_up_rect,teleport_pad_up_cd):
        self.teleport_pad_up_x_pos = teleport_pad_up_x_pos
        self.teleport_pad_up_y_pos = teleport_pad_up_y_pos
        self.teleport_pad_up_rect = teleport_pad_up_rect
        self.teleport_pad_up_cd = teleport_pad_up_cd
    
class speed_up_pad():
    def __init__(self,speed_up_pad_x_pos,speed_up_pad_y_pos,speed_up_pad_rect):
        self.speed_up_pad_x_pos = speed_up_pad_x_pos
        self.speed_up_pad_y_pos = speed_up_pad_y_pos
        self.speed_up_pad_rect = speed_up_pad_rect

class teleport_pad_down():
    def __init__(self,teleport_pad_down_x_pos,teleport_pad_down_y_pos,teleport_pad_down_rect,teleport_pad_down_cd):
        self.teleport_pad_down_x_pos = teleport_pad_down_x_pos
        self.teleport_pad_down_y_pos = teleport_pad_down_y_pos
        self.teleport_pad_down_rect = teleport_pad_down_rect
        self.teleport_pad_down_cd = teleport_pad_down_cd

map_lvl = 0
def load_map(path):
    global map_lvl
    f = open("game/maps/map"+str(map_lvl)+'.txt', "r")
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
        
def show_score(x,y):
    global final_score, player_score
    score = font.render("Score: %d" %(final_score + player_score) , True, (255,255,255))
    display.blit(score, (x,y))

button1_clicked = 0
button2_clicked = 0
button3_clicked = 0
button4_clicked = 0
button5_clicked = 0

tank_live = 3
def button_1():
    global tank_live, button1_clicked,final_score
    if final_score >= 40 and button1_clicked != 1:
        final_score-=40
        button1_clicked = 1
        tank_live = 2
        return(tank_live, button1_clicked,final_score)

lampist_wait_timer = 120
def button_2():
    global lampist_wait_timer,button2_clicked,final_score
    if final_score >= 20 and button2_clicked != 1:
        final_score-=20
        button2_clicked = 1
        lampist_wait_timer = 60
        return(lampist_wait_timer,button2_clicked,final_score)

rudar_speed = 1
def button_3():
    global rudar_speed, button3_clicked, final_score
    if final_score >= 30 and button3_clicked != 1:
        final_score -= 30
        button3_clicked = 1
        rudar_speed = 0.8
        return (rudar_speed, button3_clicked, final_score)
player_jump_up = -15
def button_4():
    global player_jump_up, button4_clicked, final_score
    if final_score >= 40 and button4_clicked != 1:
        final_score -= 40
        button4_clicked = 1
        player_jump_up = -17.5
        return (player_jump_up, button4_clicked, final_score)
player_speed = 5
def button_5():
    global player_speed, button5_clicked, final_score
    if final_score >= 50 and button5_clicked != 1:
        final_score -= 50
        button5_clicked = 1
        player_speed = 7.5
        return (player_speed, button5_clicked, final_score)

animation_database = {}

animation_database['player_walk'] = load_animation('game/assets/characters/janez/player_walk', [0, 1, 2, 3, 4,5,6,7])
animation_database['player_idle'] = load_animation('game/assets/characters/janez/player_idle', [1, 1])
animation_database['rudar_walk'] = load_animation('game/assets/characters/rudar/rudar_walk', [0, 1,2,3,4,5,6,7])
animation_database['rudar_attack'] = load_animation('game/assets/characters/rudar/rudar_attack', [0, 1, 2, 3])
animation_database["lučkar_walk"] = load_animation('game/assets/characters/lučkar/lučkar_walk', [0, 1, 2,3,4,5,6,7])
animation_database["lučkar_attack"] = load_animation('game/assets/characters/lučkar/lučkar_attack', [0, 1, 2,3,4,5,6,7,8,9,10])
animation_database["tank_walk"] = load_animation('game/assets/characters/tank/tank_walk', [0, 1, 2,3,4,5,6,7,8,9,10,11])
animation_database["boss_idle"] = load_animation("game/assets/characters/boss/boss_idle", [1])
animation_database["boss_mad"] = load_animation("game/assets/characters/boss/boss_mad", [1,2])
animation_database["boss_attack"] = load_animation("game/assets/characters/boss/boss_attack", [1])

game_map = load_map('map')

grass_img = pygame.image.load('grass.png')
dirt_img = pygame.image.load('dirt.png')
coin_img = pygame.image.load("coin.png")
jump_pad_img = pygame.image.load("jump_pad.png")
background_img = pygame.image.load("bg.png").convert()
endpoint_img = pygame.image.load("endpoint.png")
teleport_pad_down_img = pygame.image.load("teleport_pad_down.png")
teleport_pad_up_img = pygame.image.load("teleport_pad_up.png")
speed_up_pad_img = pygame.image.load("speed.png")


player_action = 'player_idle'
player_frame = 0
player_flip = False
player_score = 0


player_rect = pygame.Rect(100,300,48,96)

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]

"""
NOTE: če tuki daš unused rudarja se naredi bug, k randomly floata

"""

rudar_sez=[]
lučkar_sez=[]
tank_sez=[]
tile_rects = []
coin_sez = []
jump_pad_sez = []
end_sez = []
teleport_pad_down_sez = []
teleport_pad_up_sez = []
speed_up_pad_sez = []
boss_sez = []
load_map_timer = 0
final_score = 0
speed_up_timer = 0
boss_up_down = 0
boss_attack_timer = random.randint(180,300)
boss_mad_timer = 60
boss_movement_count = 0
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

pygame.mixer.music.load('music.wav')
pygame.mixer.music.play(-1)

def main():
    global player_rect,moving_right,moving_left,vertical_momentum,player_action,player_frame,air_timer,player_flip, load_map_timer,tile_rects, player_score,coin_img,coin_sez,jump_pad_sez,jump_pad_img,tank_sez,lučkar_sez,rudar_sez,end_sez,map_lvl,game_map,final_score, endpoint_img,teleport_pad_down_sez,teleport_pad_up_sez, teleport_pad_up_img, teleport_pad_down_img, speed_up_pad_img,speed_up_pad_sez,speed_up_timer,tank_live, lampist_wait_timer,rudar_speed, player_jump_up,player_speed,boss_sez,boss_up_down,boss_attack_timer, boss_mad_timer,boss_movement_count

    while True: # game loop
        display.blit(background_img, (0,0))# clear screen by filling it with blue
        y = 0
        scroll[0] += (player_rect.x-scroll[0] - (500+16))/20 #premikanje kamere na x osi
        scroll[1] = -100 # y os kamera
        for layer in game_map: #za vsako vrstico v mapi
            x = 0 #x nastavimo na 0
            for tile in layer: #za vsako kocko v plasti
                if load_map_timer == 0: #poskrbi za enkratno spawnanje objektov
                    if tile == "1" or tile == "2" or tile == "3": #če je dirt ali grass nastavi rect.
                        tile_rects.append(pygame.Rect(x*64,y*64,64,64)) #nastavimo rect
                if player_rect.x+1000 > x*64 and player_rect.x-700 <x*64: #optimizacija x osi
                    if tile == '1': #pogledamo, če je tile 1
                        display.blit(dirt_img,(x*64-scroll[0],y*64-scroll[1])) #ga blitamo
                    if tile == '2': #pogledamo če je tile 2
                        display.blit(grass_img,(x*64-scroll[0],y*64-scroll[1])) #ga blitamo
                if load_map_timer == 0: #pogledamo če je load timer 0, kar pomeni, da se samo 1x spawna
                    if tile == "l": #če je tile lučkar
                        lučkar1 = lučkar(x * 64-32, y * 64-32, 48, 96, "lučkar_walk", 0, False, 0, 0, True, 180, 0) #ustvarimo lučkarja
                        lučkar_sez.append(lučkar1)#ga appendamo na sez lučkarjev
                    if tile == "r":
                        rudar1 = rudar(x * 64-32, y * 64-32, 48, 96, "rudar_walk", 0, False, 0, 0, True)
                        rudar_sez.append(rudar1)
                    if tile == "t":
                        tank1 = tank(x * 64-32, y * 64-32, 54, 96, "tank_walk", 0, False, 0, 0, True,tank_live)
                        tank_sez.append(tank1)
                    if tile == "c":
                        coin1 = coin(x * 64, y * 64 - 32, 16, 16, (x * 64-16, y * 64 - 32, 16, 16), True)
                        coin_sez.append(coin1)
                    if tile == "j":
                        jump_pad1 = jump_pad (x*64,y*64+59,(x*64,y*64+48,64,5),0)
                        jump_pad_sez.append(jump_pad1)
                    if tile =="e":
                        end1= end(x*64,y*64,64,128,(x*64,y*64,64-63,128-(256+64+23)))
                        end_sez.append(end1)
                    if tile =="d":
                        teleport_pad_down1 = teleport_pad_down(x*64,y*64+59,(x*64,y*64+48,64,5),0)
                        teleport_pad_down_sez.append(teleport_pad_down1)
                    if tile =="u":
                        teleport_pad_up1 = teleport_pad_up(x*64,y*64+59,(x*64,y*64+48,64,5),0)
                        teleport_pad_up_sez.append(teleport_pad_up1)
                    if tile =="s":
                        speed_up_pad1 = speed_up_pad(x*64,y*64+59,(x*64,y*64+48,64,5))
                        speed_up_pad_sez.append(speed_up_pad1)
                    if tile =="B":
                        boss1 = boss(x * 64-32, y * 64-32, 106, 180, "boss_idle", 0, False, 0, 0, True,12)
                        boss_sez.append(boss1)
                        boss_perm_pos_x = x*64-32

                x += 1 #x+1

            y += 1 #y+1
        load_map_timer = 1 #load timer nastavimo na 1 če je že šlo čez celo zanko


        for jump_pads in jump_pad_sez: # za vsak jump pad na mapi
            display.blit(jump_pad_img,(jump_pads.jump_pad_x_pos - scroll[0],jump_pads.jump_pad_y_pos-scroll[1])) # prikaže jump pad
            if player_rect.colliderect(jump_pads.jump_pad_rect): #če se player dotakne jump pada
                if jump_pads.jump_pad_cd == 0: #če jump pad nima cd-ja
                    vertical_momentum=-20 #player skoči
                    jump_pads.jump_pad_cd = 60 #nastavi jump pad cd
            if jump_pads.jump_pad_cd != 0: #Zmanjševanje cd-ja
                jump_pads.jump_pad_cd -=1

        for teleport_pad_downs in teleport_pad_down_sez: # za vsak jump pad na mapi
            display.blit(teleport_pad_down_img,(teleport_pad_downs.teleport_pad_down_x_pos - scroll[0],teleport_pad_downs.teleport_pad_down_y_pos-scroll[1])) # prikaže jump pad
            if player_rect.colliderect(teleport_pad_downs.teleport_pad_down_rect): #če se player dotakne jump pada
                if teleport_pad_downs.teleport_pad_down_cd == 0: #če jump pad nima cd-ja
                    player_rect.y+=192
                    teleport_pad_downs.teleport_pad_down_cd = 60 #nastavi jump pad cd
            if teleport_pad_downs.teleport_pad_down_cd != 0: #Zmanjševanje cd-ja
                teleport_pad_downs.teleport_pad_down_cd -=1
        
        for teleport_pad_ups in teleport_pad_up_sez: # za vsak jump pad na mapi
            display.blit(teleport_pad_up_img,(teleport_pad_ups.teleport_pad_up_x_pos - scroll[0],teleport_pad_ups.teleport_pad_up_y_pos-scroll[1])) # prikaže jump pad
            if player_rect.colliderect(teleport_pad_ups.teleport_pad_up_rect): #če se player dotakne jump pada
                if teleport_pad_ups.teleport_pad_up_cd == 0: #če jump pad nima cd-ja
                    player_rect.y-=192
                    teleport_pad_ups.teleport_pad_up_cd = 60 #nastavi jump pad cd
            if teleport_pad_ups.teleport_pad_up_cd != 0: #Zmanjševanje cd-ja
                teleport_pad_ups.teleport_pad_up_cd -=1

        for ends in end_sez:
            display.blit(endpoint_img,(ends.end_x_pos-scroll[0]-63,ends.end_y_pos-(256+64+23)))
            if player_rect.colliderect(ends.end_rect) == True:
                map_lvl+=1
                player_rect = pygame.Rect(100,300,48,96)
                load_map_timer = 0
                final_score+=player_score
                player_score = 0
                end_sez =[]
                rudar_sez= []
                lučkar_sez =[]
                tank_sez = []
                coin_sez = []
                jump_pad_sez = []
                tile_rects = []
                teleport_pad_down_sez = []
                teleport_pad_up_sez = []
                speed_up_pad_sez = []
                boss_sez = []
                speed_up_timer = 0
                boss_up_down = 0
                boss_attack_timer = random.randint(180, 300)
                boss_mad_timer = 60
                boss_movement_count = 0
                game_map=load_map("map")

        for speed_up_pads in speed_up_pad_sez: # za vsak jump pad na mapi
            display.blit(speed_up_pad_img,(speed_up_pads.speed_up_pad_x_pos - scroll[0],speed_up_pads.speed_up_pad_y_pos-scroll[1])) # prikaže jump pad
            if player_rect.colliderect(speed_up_pads.speed_up_pad_rect): #če se player dotakne jump pada
                    speed_up_timer = 90
                


        for coins in coin_sez: #vse coine v seznamu
            if coins.coin_alive == True: #če coin še ni bil pobran
                pickup_test = player_rect.colliderect(coins.colider) # ali se player dotkne coina
                display.blit(coin_img, (coins.x_pos - scroll[0], coins.y_pos - scroll[1])) # prikazovanje coinov
                if pickup_test == True: #če se player dotakne coina
                    coins.colider = (0, 0, 0, 0) #coin colider nastavi na 0000
                    player_score += 1 #player scoru dodamo 1
                    coins.coin_alive = False # coin nastavimo na "dead", da se ne prikazuje več

        for rudars in rudar_sez: #za vse rudarje v seznamu
            if rudars.rudar_alive == True: #če je rudar živ
                rudars.rudar_movement_y += 1 #y os rudarja prištejemo 1
                rudar_rects = pygame.Rect(rudars.rudar_x_pos,rudars.rudar_y_pos,48,96) #rudarjev celoten rect
                rudar_top_colider = pygame.Rect(rudars.rudar_x_pos, rudars.rudar_y_pos, 48, 48)#colider za testiranje stranskih dotikov
                if player_rect.x + 1200 > rudar_rects.x: #Se zacne premikati če se player pribljiža rudarjem
                    if rudars.rudar_x_pos > player_rect.x+50: #premikanje rudarja gelde na kater istrani rudarja je player
                        rudars.rudar_action, rudars.rudar_frame = change_action(rudars.rudar_action,rudars.rudar_frame, "rudar_walk")#zamenjava animacije
                        rudars.rudar_flip = True
                        rudars.rudar_movement_x = -rudar_speed
                    elif rudars.rudar_x_pos < player_rect.x-50:
                        rudars.rudar_action, rudars.rudar_frame = change_action(rudars.rudar_action, rudars.rudar_frame,"rudar_walk")
                        rudars.rudar_flip = False
                        rudars.rudar_movement_x = rudar_speed
                rudar_rects, collisions = move(rudar_rects, [rudars.rudar_movement_x,rudars.rudar_movement_y], tile_rects)#preverjanje collisionov glede na tile
                if collisions["bottom"] == True: #če se dotika tila spodaj
                    rudars.rudar_movement_y = 0 #se y os ne spreminja
                if rudar_rects.y > 800:
                    rudars.rudar_alive = False
                if player_rect.x + 1200 > rudar_rects.x:#enako kot zgoraj
                    if collisions["left"] == True or collisions["right"] == True:#če se rudar zabije v levo ali denso stran ostane primeru
                        rudars.rudar_movement_x = 0
                    rudars.rudar_x_pos += rudars.rudar_movement_x #prišteje premikanje po x osi
                    rudars.rudar_y_pos += rudars.rudar_movement_y#prišteje premikanje po y osi
                    rudars.rudar_frame += 1 #prišteje 1 animaciji ki se izvaja/zamenja frame animacije
                    if rudars.rudar_frame >= len(animation_database[rudars.rudar_action]):#če frami presežejo največji možni frame animacije se resetira na 0
                        rudars.rudar_frame = 0
                    rudar_id = animation_database[rudars.rudar_action][rudars.rudar_frame]#pridobivanje poti za animacijo
                    rudar_img = animation_frames[rudar_id]
                    display.blit(pygame.transform.flip(rudar_img, rudars.rudar_flip, False),(rudars.rudar_x_pos - scroll[0], rudars.rudar_y_pos - scroll[1]))#prikaz enemija
                    rudar_test_top_left = player_rect.collidepoint(rudar_rects.topleft)#testiranje dotikov
                    rudar_test_top_right = player_rect.collidepoint(rudar_rects.topright)
                    rudar_test_left_middle = player_rect.collidepoint(rudar_top_colider.midleft)
                    rudar_test_right_middle = player_rect.collidepoint(rudar_top_colider.midright)
                    if rudar_test_top_left == True or rudar_test_top_right == True:
                        rudars.rudar_alive = False
                        vertical_momentum = -15
                    if rudar_test_top_left == True and rudar_test_left_middle == True or rudar_test_top_right == True and rudar_test_right_middle == True:#respawn
                        rudars.rudar_alive = True
                        player_rect = pygame.Rect(100,300,48,96)
                        load_map_timer = 0
                        rudar_sez= []
                        lučkar_sez =[]
                        tank_sez = []
                        coin_sez = []
                        jump_pad_sez = []
                        player_score = 0
                        tile_rects = []
                        teleport_pad_down_sez = []
                        teleport_pad_up_sez = []
                        speed_up_pad_sez = []
                        boss_sez = []
                        speed_up_timer = 0
                        boss_up_down = 0
                        boss_attack_timer = random.randint(180, 300)
                        boss_mad_timer = 60
                        boss_movement_count = 0
                    if rudars.rudar_alive == False:
                        rudar_rects = pygame.Rect(0, 0, 0, 0)

        for lučkars in lučkar_sez:
            if lučkars.lučkar_alive == True:
                lučkars.lučkar_movement_y += 1
                lučkar_rects = pygame.Rect(lučkars.lučkar_x_pos,lučkars.lučkar_y_pos,48,96)
                lučkar_top_colider = pygame.Rect(lučkars.lučkar_x_pos, lučkars.lučkar_y_pos, 48, 48)
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
                        lučkars.lučkar_attack_timer = lampist_wait_timer
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
                    lučkar_test_left_middle = player_rect.collidepoint(lučkar_top_colider.midleft)
                    lučkar_test_right_middle = player_rect.collidepoint(lučkar_top_colider.midright)
                    if lučkar_test_top_left == True or lučkar_test_top_right == True:
                        lučkars.lučkar_alive = False
                        vertical_momentum = -15
                    if lučkar_test_top_left == True and lučkar_test_left_middle == True or lučkar_test_top_right == True and lučkar_test_right_middle == True:
                        lučkars.lučkar_alive = True
                        player_rect = pygame.Rect(100,300,48,96)
                        load_map_timer = 0
                        rudar_sez= []
                        lučkar_sez =[]
                        tank_sez = []
                        coin_sez = []
                        jump_pad_sez = []
                        player_score = 0
                        tile_rects = []
                        teleport_pad_down_sez = []
                        teleport_pad_up_sez = []
                        speed_up_pad_sez = []
                        boss_sez = []
                        speed_up_timer = 0
                        boss_up_down = 0
                        boss_attack_timer = random.randint(180, 300)
                        boss_mad_timer = 60
                        boss_movement_count = 0
                    if lučkars.lučkar_alive == False:
                        lučkar_rects = pygame.Rect(0, 0, 0, 0)

        for tanks in tank_sez:
            if tanks.tank_alive == True:
                tanks.tank_movement_y += 1
                tank_rects = pygame.Rect(tanks.tank_x_pos,tanks.tank_y_pos,54,96)
                tank_top_colider = pygame.Rect(tanks.tank_x_pos, tanks.tank_y_pos, 54, 48)
                fix_colider = pygame.Rect(tanks.tank_x_pos,tanks.tank_y_pos,26,48)
                if player_rect.x + 1200 > tank_rects.x:
                    if tanks.tank_x_pos > player_rect.x+50:
                        tanks.tank_action, tanks.tank_frame = change_action(tanks.tank_action,tanks.tank_frame, "tank_walk")
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
                    tank_test_left_middle = player_rect.collidepoint(tank_top_colider.midleft)
                    tank_test_right_middle = player_rect.collidepoint(tank_top_colider.midright)
                    tank_test_top_fix = player_rect.collidepoint(fix_colider.topright)
                    if tank_test_top_left == True or tank_test_top_right == True or tank_test_top_fix == True:
                        tanks.tank_hp -= 1
                        vertical_momentum = -15
                    if tank_test_top_left == True and tank_test_left_middle == True or tank_test_top_right == True and tank_test_right_middle == True:
                        player_rect = pygame.Rect(100,300,48,96)
                        load_map_timer = 0
                        rudar_sez= []
                        lučkar_sez =[]
                        tank_sez = []
                        coin_sez = []
                        jump_pad_sez = []
                        player_score = 0
                        tile_rects = []
                        teleport_pad_down_sez = []
                        teleport_pad_up_sez = []
                        speed_up_pad_sez = []
                        boss_sez = []
                        speed_up_timer = 0
                        boss_up_down = 0
                        boss_attack_timer = random.randint(180, 300)
                        boss_mad_timer = 60
                        boss_movement_count = 0
                    if tanks.tank_hp == 0:
                        tanks.tank_alive = False


        for bosss in boss_sez:
            if bosss.boss_alive == True:
                boss_rects = pygame.Rect(bosss.boss_x_pos,bosss.boss_y_pos,106,180)
                boss_rect1 = pygame.Rect(bosss.boss_x_pos+28,bosss.boss_y_pos,48,48)
                boss_rect2 = pygame.Rect(bosss.boss_x_pos, bosss.boss_y_pos,106,90)
                boss_rect3 = pygame.Rect(bosss.boss_x_pos, bosss.boss_y_pos+90,106,90)
                boss_rect4 = pygame.Rect(bosss.boss_x_pos,bosss.boss_y_pos,180,106)
                if boss_attack_timer <= 0:
                    if boss_mad_timer >0:
                        boss_attack = False
                        if bosss.boss_x_pos >player_rect.x:
                            bosss.boss_action, bosss.boss_frame = change_action(bosss.boss_action, bosss.boss_frame,"boss_mad")
                            bosss.boss_flip = True
                            boss_mad_timer -= 1
                        elif bosss.boss_x_pos < player_rect.x:
                            bosss.boss_action, bosss.boss_frame = change_action(bosss.boss_action, bosss.boss_frame,"boss_mad")
                            bosss.boss_flip = False
                            boss_mad_timer -=1
                    if boss_mad_timer == 0:
                        boss_attack = True
                        bosss.boss_action, bosss.boss_frame = change_action(bosss.boss_action, bosss.boss_frame,"boss_attack")
                        bosss.boss_flip = False
                        bosss.boss_movement_x = -20
                        bosss.boss_movement_y = 0
                        if bosss.boss_x_pos == boss_perm_pos_x-1500:
                            bosss.boss_x_pos = boss_perm_pos_x+1500
                        if bosss.boss_x_pos == boss_perm_pos_x:
                            boss_movement_count+=1
                        if boss_movement_count == 3:
                            boss_movement_count = 0
                            boss_mad_timer = 60
                            boss_attack_timer = random.randint(180,300)
                            bosss.boss_movement_x = 0
                else:
                    boss_attack = False
                    if bosss.boss_x_pos > player_rect.x:
                        bosss.boss_action, bosss.boss_frame = change_action(bosss.boss_action,bosss.boss_frame, "boss_idle")
                        bosss.boss_flip = True
                    elif bosss.boss_x_pos < player_rect.x:
                        bosss.boss_action, bosss.boss_frame = change_action(bosss.boss_action, bosss.boss_frame,"boss_idle")
                        bosss.boss_flip = False
                    boss_attack_timer -=1
                    if boss_up_down == 0:
                        bosss.boss_movement_y =-3
                        if boss_rects.y < 0:
                            boss_up_down = 1
                    else:
                        bosss.boss_movement_y =3
                        if boss_rects.y > 500:
                            boss_up_down = 0


                bosss.boss_x_pos += bosss.boss_movement_x
                bosss.boss_y_pos += bosss.boss_movement_y
                bosss.boss_frame += 1
                if bosss.boss_frame >= len(animation_database[bosss.boss_action]):
                    bosss.boss_frame = 0
                boss_id = animation_database[bosss.boss_action][bosss.boss_frame]
                boss_img = animation_frames[boss_id]
                display.blit(pygame.transform.flip(boss_img, bosss.boss_flip, False),(bosss.boss_x_pos - scroll[0], bosss.boss_y_pos - scroll[1]))
                boss_test_top_left = player_rect.collidepoint(boss_rects.topleft)
                boss_test_top_right = player_rect.collidepoint(boss_rects.topright)
                boss_test_left_middle = player_rect.collidepoint(boss_rect1.topleft)
                boss_test_right_middle = player_rect.collidepoint(boss_rect1.topright)

                boss_test_collider_left1 = player_rect.collidepoint(boss_rect2.midleft)
                boss_test_collider_left2 = player_rect.collidepoint(boss_rect2.bottomleft)
                boss_test_collider_left3 = player_rect.collidepoint(boss_rect3.midleft)
                boss_test_collider_left4 = player_rect.collidepoint(boss_rect3.bottomleft)

                boss_test_collider_right1 = player_rect.collidepoint(boss_rect2.midright)
                boss_test_collider_right2 = player_rect.collidepoint(boss_rect2.bottomright)
                boss_test_collider_right3 = player_rect.collidepoint(boss_rect3.midright)
                boss_test_collider_right4 = player_rect.collidepoint(boss_rect3.bottomright)
                if boss_attack == False:
                    if boss_test_top_left == True or boss_test_top_right == True or boss_test_left_middle == True or boss_test_right_middle == True:
                        bosss.boss_hp -= 1
                        vertical_momentum = -15

                    if boss_test_collider_left1 == True or boss_test_collider_left2 == True or boss_test_collider_left3 == True or boss_test_collider_left4 == True or boss_test_collider_right1 == True or boss_test_collider_right2 == True or boss_test_collider_right3 == True or boss_test_collider_right4 == True:
                        player_rect = pygame.Rect(100,300,48,96)
                        load_map_timer = 0
                        rudar_sez= []
                        lučkar_sez =[]
                        tank_sez = []
                        coin_sez = []
                        jump_pad_sez = []
                        player_score = 0
                        tile_rects = []
                        teleport_pad_down_sez = []
                        teleport_pad_up_sez = []
                        speed_up_pad_sez = []
                        boss_sez = []
                        speed_up_timer = 0
                        boss_up_down = 0
                        boss_attack_timer = random.randint(180, 300)
                        boss_mad_timer = 60
                        boss_movement_count = 0
                    if bosss.boss_hp == 0:
                        bosss.boss_alive = False
                else:
                    if player_rect.colliderect(boss_rect4) == True:
                        player_rect = pygame.Rect(100, 300, 48, 96)
                        load_map_timer = 0
                        rudar_sez = []
                        lučkar_sez = []
                        tank_sez = []
                        coin_sez = []
                        jump_pad_sez = []
                        player_score = 0
                        tile_rects = []
                        teleport_pad_down_sez = []
                        teleport_pad_up_sez = []
                        speed_up_pad_sez = []
                        boss_sez = []
                        speed_up_timer = 0
                        boss_up_down = 0
                        boss_attack_timer = random.randint(180, 300)
                        boss_mad_timer = 60
                        boss_movement_count = 0

        player_movement = [0,0]
        if moving_right == True:
            if speed_up_timer == 0:
                player_movement[0] += player_speed
            else:
                player_movement[0] +=10
        if moving_left == True:
            if speed_up_timer == 0:
                player_movement[0] -= player_speed
            else:
                player_movement[0] -=10
        speed_up_timer -=1
        if speed_up_timer <= 0:
            speed_up_timer = 0
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

        if collisions["top"] == True:
            vertical_momentum = 0

        player_frame += 1
        if player_frame >= len(animation_database[player_action]):
            player_frame = 0
        player_img_id = animation_database[player_action][player_frame]
        player_img = animation_frames[player_img_id]
        display.blit(pygame.transform.flip(player_img,player_flip,False),(player_rect.x-scroll[0],player_rect.y-scroll[1]))

        if player_rect.y >800: #respawn ob padcu v prepad
            player_rect = pygame.Rect(100,300,48,96)
            load_map_timer = 0
            rudar_sez= []
            lučkar_sez =[]
            tank_sez = []
            coin_sez = []
            jump_pad_sez = []
            player_score = 0
            tile_rects = []
            teleport_pad_down_sez = []
            teleport_pad_up_sez = []
            speed_up_pad_sez = []
            boss_sez = []
            speed_up_timer = 0
            boss_up_down = 0
            boss_attack_timer = random.randint(180, 300)
            boss_mad_timer = 60
            boss_movement_count = 0

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
                        vertical_momentum = player_jump_up
                if event.key == K_ESCAPE:
                    return

            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    moving_right = False
                if event.key == K_LEFT:
                    moving_left = False

        player_jump = False
        #test+=1

        show_score(50,10)
        display.blit(coin_img,(5,5))
        screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
        pygame.display.update()
        clock.tick(60)


menu_font = pygame_menu.font.FONT_8BIT #izberemo font za glavni meni

menu_background_image = pygame_menu.baseimage.BaseImage(image_path = "background.png") #odpremo sliko za temo glavnega menija
menu_theme = pygame_menu.themes.THEME_DARK.copy() #kopiramo že obstoječo temo, ki jo bomo uredili
menu_theme.background_color = menu_background_image #temi nastavimo sliko ozadja
menu_theme.widget_font = menu_font #nastavimo izbrani font
menu_theme.widget_font_size = 64 #nastavimo izbrano velikost besedila

submenu_font = pygame_menu.font.FONT_8BIT #za podmeni izberemo font

submenu_theme = pygame_menu.themes.THEME_DARK.copy() #kopiramo temo, ki jo bomo preuredili
submenu_theme.widget_font = menu_font #nastavimo font menija
submenu_theme.widget_font_size = 32 #nastavimo velikost texta
submenu_theme.widget_alignment = pygame_menu.locals.ALIGN_CENTER #nastavimo kako, bodo postavljeni elementi
submenu_theme.widget_margin = (0,15) #nastavimo razmik med gumbi oz. elementi
submenu_theme.widget_selection_effect=pygame_menu.widgets.SimpleSelection() #nastavimo, kako se bodo označevali elementi


def shop_menu(): #definiramo metodo za dostop do podmenija
    global final_score,button1_clicked,button2_clicked,button3_clicked,button4_clicked,button5_clicked #uporabimo globalno spremenljivko, ki nam shranjuje vrednost
    play_submenu = pygame_menu.Menu( #inicializiramo meni
        height=800, #mu nastavimo velikost
        theme= submenu_theme, #temo 
        title='Submenu', #naslov
        width=1200, #širino
    )

    play_submenu.add.label(final_score) #dodamo mu vrednost premoga
    if button1_clicked == 0:
        play_submenu.add.button("Tank HP down   40", button_1) #dodamo gumb za upgrade
    if button2_clicked == 0:
        play_submenu.add.button("Lampist attack 1sec downgrade   20", button_2)
    if button3_clicked == 0:
        play_submenu.add.button("Rudar speed down   30", button_3)
    if button4_clicked == 0:
        play_submenu.add.button("Player jump upgrade   50", button_4)
    if button5_clicked == 0:
        play_submenu.add.button("Player speed upgrade   40", button_5)
    play_submenu.add.button("BACK", play_submenu.disable) #dodamo exit gumb

    play_submenu.mainloop(screen) #ustvarimo mainloop za meni



menu = pygame_menu.Menu(800, 1200, '', #ustvarimo glavni meni
                       theme = menu_theme)
menu.add.button('Play', main) #ustvarimo gumb za igranje same igre
menu.add.button('Menu', shop_menu) #ustvarimo gumb za shop
menu.add.button('Quit', pygame_menu.events.EXIT) #in ustvarimo gumb za izhod

menu.mainloop(screen) #ustvarimo mainloop za glavni meni
