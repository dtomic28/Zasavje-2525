import random
from PIL import Image

#tule gre u isti folder kukr j main file. mape grejo v:
#main folder -> maps -> "mapN.png", "mapN.txt"
def setMap(N):
    try:
        txt=open("maps/map"+str(N)+".txt","w")
    except:
        txt=open("maps/mapError.txt","w")
        print("mapError: map number "+str(N)+" does not exist")
    try:
        img=Image.open("maps/map"+str(N)+".png")
    except:
        img=Image.open("maps/mapError.png")
        print("mapError: map number "+str(N)+" does not exist")
    width,height=img.size
    for h in range(height):
        izpis=""
        for w in range(width):
            if str(img.getpixel((w,h)))=="(233, 113, 38)":
                izpis+="1"
            elif str(img.getpixel((w,h)))=="(251, 242, 54)":
                izpis+"2"
            elif str(img.getpixel((w,h)))=="(153, 229, 80)":
                izpis+="3"
            elif str(img.getpixel((w,h)))=="(106, 190, 48)":
                izpis+="r"
            elif str(img.getpixel((w,h)))=="(55, 148, 110)":
                izpis+="l"
            elif str(img.getpixel((w,h)))=="(63, 63, 116)":
                izpis+="t"
            elif str(img.getpixel((w,h)))=="(91, 110, 255)":
                izpis+="c"
            elif str(img.getpixel((w,h)))=="(99, 155, 255)":
                izpis+="j"
            elif str(img.getpixel((w,h)))=="(95, 205, 228)":
                izpis+="e"
            elif str(img.getpixel((w,h)))=="(172, 50, 50)":
                izpis+="d"
            elif str(img.getpixel((w,h)))=="(118, 66, 138)":
                izpis+="u"
            elif str(img.getpixel((w,h)))=="(217, 87, 99)":
                izpis+="s"
            else:
                izpis+="0"
        txt.write(izpis+"\n")
    txt.close()

#v main folderji j treba modifyat tule:
"""
def choseMap(N=1): #dudat tule pred 'def load_map():' u line 25
    mapMaker.setMap(N)
    return("maps/map"+str(N))

game_map = load_map(choseMap(1)) #tule j treba sam spremenit is "map.txt" n choseMap(1) u line 71
"""

"""
for tile in layer: #za vsako kocko v plasti
                if load_map_timer == 0: #poskrbi za enkratno spawnanje objektov
                    if tile == "1" or tile == "2" or tile == "3": #če je dirt ali grass nastavi rect.
                        tile_rects.append(pygame.Rect(x*64,y*64,64,64)) #nastavimo rect
                if player_rect.x+1000 > x*64 and player_rect.x-1000 <x*64: #optimizacija x osi
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
                x += 1 #x+1
"""