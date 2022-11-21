import pygame as pg
from math import sqrt

pg.init()

sw=500
sh=500

screen = pg.display.set_mode((sw,sh))
clock = pg.time.Clock()
pg.display.set_caption('uwurawr')

class player(pg.sprite.Sprite):
    def __init__(self,image,px,py,obstacles):
        super().__init__()
        self.image=pg.image.load(image)
        self.rect=self.image.get_rect()
        self.x=px
        self.y=py
        self.rect.topleft=((self.x,self.y))
        self.vec=pg.math.Vector2()
        self.speed=5
        self.obstacles=obstacles
    
    def move(self):
        keys=pg.key.get_pressed()
        if keys[pg.K_d]:
            self.vec.x=1
        elif keys[pg.K_a]:
            self.vec.x=-1
        else:
            self.vec.x=0
        if keys[pg.K_s]:
            self.vec.y=1
        elif keys[pg.K_w]:
            self.vec.y=-1
        else:
            self.vec.y=0
        
        if self.vec.magnitude()!=0:
            self.vec=self.vec.normalize()
        self.x+=self.vec.x*self.speed
        self.rect.topleft=((self.x,self.y))
        self.collisionCheck('x')
        self.y+=self.vec.y*self.speed
        self.rect.topleft=((self.x,self.y))
        self.collisionCheck('y')
        self.rect.topleft=((self.x,self.y))
    
    def collisionCheck(self,dir):
        if dir=='x':
            for sprite in self.obstacles:
                if self.vec.x>0 and sprite.rect.colliderect(self.rect):
                    self.x=sprite.rect.left-self.rect.width
                elif self.vec.x<0 and sprite.rect.colliderect(self.rect):
                    self.x=sprite.rect.right
        elif dir=='y':
            for sprite in self.obstacles:
                if self.vec.y>0 and sprite.rect.colliderect(self.rect):
                    self.y=sprite.rect.top-self.rect.height
                elif self.vec.y<0 and sprite.rect.colliderect(self.rect):
                    self.y=sprite.rect.bottom


    def update(self):
        self.move()

class troop(pg.sprite.Sprite):
    def __init__(self,picture,positionx,positiony,visionR):
        super().__init__()
        self.x=positionx
        self.y=positiony
        self.image=pg.image.load(picture)
        self.rect=self.image.get_rect()
        self.rect.topleft=(self.x,self.y)
        self.speed=2
        self.vec=pg.math.Vector2()
        self.vRange=visionR

    def chase(self,targetx,targety):
        dx=targetx-self.x
        dy=targety-self.y
        inRange=sqrt(dx**2+dy**2)<self.vRange

        if inRange==True:
            self.vec.x=dx
            self.vec.y=dy

        if self.vec.magnitude()!=0:
            self.vec=self.vec.normalize()
        self.x+=self.vec.x*self.speed
        self.y+=self.vec.y*self.speed
        self.rect.topleft=((self.x,self.y))

    def update(self,targetx,targety):
        self.chase(targetx,targety)

class obstacle(pg.sprite.Sprite):
    def __init__(self,image,px,py):
        super().__init__()
        self.image=pg.image.load(image)
        self.rect=self.image.get_rect()
        self.rect.topleft=((px,py))


mapID=[
['w','w','w','w','w','w','w','w','w','w'],
['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
['w','z',' ',' ','p',' ',' ',' ',' ','w'],
['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
['w','w','w','w','w','w','w','w','w','w'],
]

px=0
py=0
zx=0
zy=0

rGroup=pg.sprite.Group()

rowNum=-1
for row in mapID:
    rowNum+=1
    coloumbNum=-1
    for coloumb in row:
        coloumbNum+=1
        if coloumb=='w':
            rGroup.add(obstacle('rock.png',coloumbNum*50,rowNum*50))
        elif coloumb=='p':
            px=coloumbNum*50
            py=rowNum*50
        elif coloumb=='z':
            zx=coloumbNum*50
            zy=rowNum*50

P1=player('testSprite.png',px,py,rGroup)
pGroup=pg.sprite.Group()
pGroup.add(P1)

enemy1=troop('zombie.png',zx,zy,200)
zGroup=pg.sprite.Group()
zGroup.add(enemy1)


def main():
    screen.fill('black')
    rGroup.draw(screen)
    pGroup.draw(screen)
    zGroup.draw(screen)
    pGroup.update()
    zGroup.update(P1.x,P1.y)
    pg.display.update()



run=True
while run:
    clock.tick(60)

    for event in pg.event.get():
        if event.type==pg.QUIT:
            run=False

    main()
