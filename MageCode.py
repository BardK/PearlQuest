import pygame as pg
import glob
from math import sqrt

pg.init()

sw=500
sh=500

screen = pg.display.set_mode((sw,sh))
clock = pg.time.Clock()
pg.display.set_caption('uwurawr')

gidle=[pg.image.load(img) for img in glob.glob("Gunner\\*.png")]
kidle=[pg.image.load(img) for img in glob.glob("Knight\\*.png")]
midle=[pg.image.load(img) for img in glob.glob("Mage\\*.png")]

class player(pg.sprite.Sprite):
    def __init__(self,image,px,py,obstacles,screen):
        super().__init__()
        self.screen=screen
        self.image=image
        self.rect=self.image.get_rect()
        self.x=px
        self.y=py
        self.lxdir='left'
        self.lydir='up'
        self.rect.topleft=((self.x,self.y))
        self.vec=pg.math.Vector2()
        self.speed=5
        self.obstacles=obstacles
    
    def move(self):
        keys=pg.key.get_pressed()
        if keys[pg.K_d]:
            self.vec.x=1
            self.lxdir='right'
            self.xdir='right'
        elif keys[pg.K_a]:
            self.vec.x=-1
            self.lxdir='left'
            self.xdir='left'
        else:
            self.vec.x=0
            self.xdir=''
        if keys[pg.K_s]:
            self.vec.y=1
            self.lydir='down'
            self.ydir='down'
        elif keys[pg.K_w]:
            self.vec.y=-1
            self.lydir='up'
            self.ydir='up'
            
        else:
            self.vec.y=0
            self.ydir=''

        if self.xdir!=''and self.ydir=='':
            self.lydir=''
        
        elif self.ydir!='' and self.xdir=='':
            self.lxdir=''
        
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

    def shoot(self):
        self.ammo=bullet(self.rect.centerx,self.rect.centery,self.lxdir,self.lydir)
        return self.ammo

    def update(self):
        self.move()

class bullet(pg.sprite.Sprite):
    def __init__(self,px,py,xdir,ydir):
        super().__init__()
        self.image=pg.Surface((100,100))
        self.image.fill((255,255,0))
        self.rect=self.image.get_rect(center=(px,py))
        self.xdir=xdir
        self.ydir=ydir
        self.obstacles=rGroup
        self.vec=pg.math.Vector2()
        if self.xdir=='right':
            self.vec.x=1
        elif self.xdir=='left':
            self.vec.x=-1
        else:
            self.vec.x=0
        if self.ydir=='up':
            self.vec.y=-1
        elif self.ydir=='down':
            self.vec.y=1
        else:
            self.vec.y=0

    def move(self):
        self.rect.center+=self.vec*4
        
    def checkbounds(self):
        if self.rect.centerx>500 or self.rect.centerx<0 or self.rect.centery>500 or self.rect.centery<0:
            self.kill()
            return False
        else:
            return True

    def update(self):
        self.move()
        self.checkbounds()

class troop(pg.sprite.Sprite):
    def __init__(self,picture,positionx,positiony,visionR,attacks):
        super().__init__()
        self.x=positionx
        self.y=positiony
        self.image=pg.image.load(picture)
        self.rect=self.image.get_rect()
        self.rect.topleft=(self.x,self.y)
        self.speed=1
        self.vec=pg.math.Vector2()
        self.vRange=visionR
        self.attacks=attacks
        self.HP=100

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

    def isHit(self):
        for sprite in self.attacks:
            if sprite.rect.colliderect(self.rect):
                self.HP-=10
                print (self.HP)
                sprite.kill()
                for i in range(10):
                    self.x+=sprite.vec.x*10
                    self.y+=sprite.vec.y*10
                    self.rect.topleft=(self.x,self.y)
    def isDead(self):
        if self.HP<=0:
            self.kill()
    
    def update(self,targetx,targety):
        self.chase(targetx,targety)
        self.isHit()
        self.isDead()

class obstacle(pg.sprite.Sprite):
    def __init__(self,image,px,py):
        super().__init__()
        self.image=pg.image.load(image)
        self.rect=self.image.get_rect()
        self.rect.topleft=((px,py))


mapID=[
['w','w','w','w','w','w','w','w','w','w'],
['w',' ',' ','w','w',' ',' ',' ',' ','w'],
['w',' ',' ',' ',' ',' ','w',' ',' ','w'],
['w',' ','w',' ',' ',' ',' ',' ',' ','w'],
['w',' ',' ',' ','p',' ','z',' ',' ','w'],
['w',' ','w',' ',' ',' ',' ',' ',' ','w'],
['w',' ','w',' ',' ',' ','w',' ',' ','w'],
['w',' ',' ',' ','w',' ',' ',' ',' ','w'],
['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
['w','w','w','w','w','w','w','w','w','w'],
]

px=0
py=0
zx=0
zy=0

rGroup=pg.sprite.Group()
zGroup=pg.sprite.Group()
bGroup=pg.sprite.Group()

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
            zGroup.add(troop('zombie.png',coloumbNum*50,rowNum*50,200,bGroup))

P1=player(midle[0],px,py,rGroup,screen)
pGroup=pg.sprite.Group()
pGroup.add(P1)

def menu():
    keys=pg.key.get_pressed()
    if keys[pg.K_0]:
        return 1
    else:
        return 0

def main():
    screen.fill('black')
    rGroup.draw(screen)
    pGroup.draw(screen)
    zGroup.draw(screen)
    bGroup.draw(screen)
    pGroup.update()
    bGroup.update()
    zGroup.update(P1.x,P1.y)
    pg.display.update()


gamestate=0
shotNum=0
reload=False
run=True
while run:
    clock.tick(60)

    for event in pg.event.get():
        if event.type==pg.QUIT:
            run=False
        if event.type==pg.MOUSEBUTTONDOWN and reload!=True:
            bGroup.add(P1.shoot())
            shotNum+=1
            if shotNum==1:
                shotNum=60
                reload=True
    if reload==True:
        shotNum-=1
        if shotNum==0:
            print("Done reloading")
            reload=False

    if gamestate==0:
        gamestate=menu()

    elif gamestate==1:
        main()