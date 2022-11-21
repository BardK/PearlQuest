import pygame as pg
from math import sqrt

#Initialize pygame
pg.init()

#set screen dimentions and screen id
boundx=1080
boundy=600

#create screen
screen=pg.display.set_mode((boundx,boundy))
pg.display.set_caption("Test1")

#set clock and frame rate
clock=pg.time.Clock()
FPS=60

#set the player class
class player(pg.sprite.Sprite):
    def __init__(self,picture,posx,posy,obstacles):
        super().__init__()
        self.image=pg.image.load(picture)
        self.rect=self.image.get_rect()
        self.x=posx
        self.y=posy
        self.w=64
        self.h=64
        self.rect.center=(self.x,self.y)
        self.vec=pg.math.Vector2()
        self.speed=5

        self.obstacles=obstacles

    def move(self):
        keys=pg.key.get_pressed()
        if keys[pg.K_a]:
            self.vec.x=-1
        elif keys[pg.K_d]:
            self.vec.x=1
        else:
            self.vec.x=0
        
        if keys[pg.K_w]:
            self.vec.y=-1
        elif keys[pg.K_s]:
            self.vec.y=1
        else:
            self.vec.y=0
        
        if self.vec.magnitude()!=0:
            self.vec=self.vec.normalize()
        self.x+=self.vec.x*self.speed
        self.y+=self.vec.y*self.speed
        self.rect.center=(self.x,self.y)
        

    def update(self):
        self.move()

#Enemy troop class
class troop(pg.sprite.Sprite):
    def __init__(self,picture,positionx,positiony,visionR):
        super().__init__()
        self.x=positionx
        self.y=positiony
        self.image=pg.image.load(picture)
        self.rect=self.image.get_rect()
        self.rect.center=(self.x,self.y)
        self.speed=2
        self.vec=pg.math.Vector2()
        self.vRange=visionR

    def chase(self, targetx,targety):
        dx=targetx-self.x
        dy=targety-self.y
        inRange=sqrt(dx**2+dy**2)<self.vRange

        if inRange==True:
            self.vec.x=dx
            self.vec.y=dy

        if self.vec.magnitude()!=0:
            self.vec=self.vec.normalize()
        self.rect.center+=self.vec*self.speed
        self.x+=self.vec.x*self.speed
        self.y+=self.vec.y*self.speed
        self.rect.center=(self.x,self.y)
        
    def update(self,targetx,targety):
        self.chase(targetx,targety)

class object(pg.sprite.Sprite):
    def __init__(self,image,walkthrough,posx,posy):
        super().__init__()
        self.image=pg.image.load(image)
        self.x=posx
        self.y=posy
        self.walkthrough=walkthrough
        self.rect=self.image.get_rect()
        self.rect.topleft=(self.x,self.y)

grass=object('grass.png',True,100,100)
grassGroup=pg.sprite.Group()
grassGroup.add(grass)
rock=object('rock.png',False,200,100)
rockGroup=pg.sprite.Group()
rockGroup.add(rock)

#create player and enemies

P1=player("testSprite.png",32,32,rockGroup)
P1Group=pg.sprite.Group()
P1Group.add(P1)
enemy1 = troop('zombie.png',300,300,500)
enemyGroup=pg.sprite.Group()
enemyGroup.add(enemy1)

def functionCall():

    screen.fill('black')
    
    grassGroup.draw(screen)
    rockGroup.draw(screen)
    P1Group.draw(screen)
    P1Group.update()
    enemyGroup.draw(screen)
    enemyGroup.update(P1.x,P1.y)

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