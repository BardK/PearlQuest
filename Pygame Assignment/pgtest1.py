import pygame as pg
from math import sqrt

#Initialize pygame
pg.init()

#set screen dimentions and screen id
boundx=500
boundy=500

#create screen
screen=pg.display.set_mode((boundx,boundy))
pg.display.set_caption("Test1")

#set clock and frame rate
clock=pg.time.Clock()
FPS=60

#set the player class
class player:
    def __init__(self,title,positionx,positiony):
        self.x=positionx
        self.y=positiony
        self.w=20
        self.h=40
        self.v=5
    def draw(self,screen):
        pg.draw.rect(screen,(0,0,255),(self.x,self.y,self.w,self.h))
    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.x-=self.v
        if keys[pg.K_d]:
            self.x+=self.v
        if keys[pg.K_w]:
            self.y-=self.v
        if keys[pg.K_s]:
            self.y+=self.v
    def checkBounds(self,xmax,ymax):
        if (P1.x+self.w/2)>xmax:
            P1.x=0   
        if P1.y+self.h/2>ymax:
            P1.y=0   
        if P1.x<0-self.w/2:
            P1.x=xmax-self.w    
        if P1.y<0-self.h/2:
            P1.y=ymax-self.h
        
#Obstacle class
class obstacle:
    def __init__(self,positionx,positiony,width,height):
        self.x=positionx
        self.y=positiony
        self.width=width
        self.height=height
    def draw(self, screen):
        pg.draw.rect(screen,(0,0,0),(self.x,self.y,self.w,self.h))
        

#Enemy troop class
class troop:
    def __init__(self,positionx,positiony,visionR):
        self.x=positionx
        self.y=positiony
        self.w=20
        self.h=40
        self.v=2
        self.vRange=visionR
    def draw(self,screen):
        pg.draw.rect(screen,(255,0,0),(self.x,self.y,self.w,self.h))
    def chase(self, targetx,targety):
        dx=abs(self.x-targetx)
        dy=abs(self.y-targety)
        inRange=sqrt(dx**2+dy**2)<self.vRange

        if self.x<targetx and inRange==True:
            self.x+=self.v
        if self.x>targetx and inRange==True:
            self.x-=self.v
        if self.y<targety and inRange==True:
            self.y+=self.v
        if self.y>targety and inRange==True:
            self.y-=self.v

#create player and enemies
P1 = player("bard",0,0)
enemy1 = troop(300,300,500)
enemy2 = troop(100,100,100)

def functionCall():
    screen.fill('white')
    P1.draw(screen)
    P1.move()
    P1.checkBounds(boundx,boundy)
    enemy1.draw(screen)
    enemy2.draw(screen)
    enemy1.chase(P1.x,P1.y)
    enemy2.chase(P1.x,P1.y)

    pg.display.update()

#loop
loop=True    
while loop:
    #use clock to manage fps
    clock.tick(FPS)
    #set quit conditions
    for event in pg.event.get():
        if event.type==pg.QUIT:
           loop=False

    functionCall()

pg.quit()