import random
from PIL import Image

concretes=["C","O","N"]
woods=["W","D"]
gravels=["G","V"]
def setMap(N):
    try:
        txt=open("data/maps/map"+str(N)+".txt","w")
    except:
        txt=open("data/maps/mapError.txt","w")
        print("mapError: map number "+str(N)+" does not exist")
    try:
        img=Image.open("data/maps/map"+str(N)+".png")
    except:
        img=Image.open("data/maps/mapError.png")
        print("mapError: map number "+str(N)+" does not exist")
    width,height=img.size
    for h in range(height):
        izpis=""
        for w in range(width):
            if str(img.getpixel((w,h)))=="(0, 0, 255)" or str(img.getpixel((w,h)))=="(0, 0, 255, 255)":
                izpis+="0"
            elif str(img.getpixel((w,h)))=="(0, 255, 0)" or str(img.getpixel((w,h)))=="(0, 255, 0, 255)":
                izpis+=str(random.randint(8,9))
            elif str(img.getpixel((w,h)))=="(100, 60, 30)" or str(img.getpixel((w,h)))=="(100, 60, 30, 255)":
                izpis+=str(random.randint(6,7))
            elif str(img.getpixel((w,h)))=="(100, 50, 30)" or str(img.getpixel((w,h)))=="(100, 50, 30, 255)":
                izpis+=str(random.randint(4,5))
            elif str(img.getpixel((w,h)))=="(100, 100, 100)" or str(img.getpixel((w,h)))=="(100, 100, 100, 255)":
                izpis+=str(random.randint(1,3))
            elif str(img.getpixel((w,h)))=="(255, 201, 14)" or str(img.getpixel((w,h)))=="(255, 201, 14, 255)":
                izpis+="I"
            elif str(img.getpixel((w,h)))=="(110, 110, 110)" or str(img.getpixel((w,h)))=="(110, 110, 110, 255)" or str(img.getpixel((w,h)))=="(80, 80, 80)" or str(img.getpixel((w,h)))=="(80, 80, 80, 255)":
                izpis+=concretes[random.randint(0,2)]#concrete
            elif str(img.getpixel((w,h)))=="(90, 90, 90)" or str(img.getpixel((w,h)))=="(90, 90, 90, 255)":
                izpis+=gravels[random.randint(0,1)]#gravel
            elif str(img.getpixel((w,h)))=="(200, 200, 200)" or str(img.getpixel((w,h)))=="(200, 200, 200, 255)":
                izpis+="R"#rail
            elif str(img.getpixel((w,h)))=="(110, 55, 30)" or str(img.getpixel((w,h)))=="(110, 55, 30, 255)":
                izpis+=woods[random.randint(0,1)]#wood
            elif str(img.getpixel((w,h)))=="(23, 23, 23)" or str(img.getpixel((w,h)))=="(23, 23, 23, 255)":
                izpis+="Z"#wheel left
            elif str(img.getpixel((w,h)))=="(10, 10, 10)" or str(img.getpixel((w,h)))=="(10, 10, 10, 255)":
                izpis+="H"#wheel right
            elif str(img.getpixel((w,h)))=="(14, 255, 239)" or str(img.getpixel((w,h)))=="(14, 255, 239, 255)":
                izpis+="Q"#chain
            else:
                izpis+="A"
        txt.write(izpis+"\n")
    txt.close()

setMap(4)