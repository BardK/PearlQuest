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

class player(pg.sprite.Sprite):
    def __init__(self,image,px,py,obstacles,eBullets,tiles,screen):
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
        self.eBullets=eBullets
        self.tiles=tiles
        self.hp=100
    
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
        for e in self.eBullets:
            if e.rect.colliderect(self.rect):
                e.kill()
                self.hp-=20
                print (self.hp)
        for tile in self.tiles:
            if tile.rect.colliderect(self.rect):
                if tile.att=='heal':
                    self.hp+=20
                    print(self.hp)
                elif tile.att=='hurt':
                    self.hp-=20
                    print(self.hp)
                tile.kill()

    def shoot(self):
        self.ammo=bullet(self.rect.centerx,self.rect.centery,self.lxdir,self.lydir)
        return self.ammo

    def update(self):
        self.move()

class bullet(pg.sprite.Sprite):
    def __init__(self,px,py,xdir,ydir):
        super().__init__()
        self.image=pg.Surface((10,10))
        self.image.fill((255,255,0))
        self.rect=self.image.get_rect(center=(px,py))
        self.xdir=xdir
        self.ydir=ydir
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
        self.rect.center+=self.vec*10
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

class turret(pg.sprite.Sprite):
    def __init__(self,px,py,dir):
        super().__init__()
        self.image=pg.Surface((50,50))
        self.image.fill('blue')
        self.rect=self.image.get_rect(center=(px,py))
        self.vec=pg.math.Vector2()
        self.cd=0
        self.cdstate=False
        if dir=='left':
            self.vec.x=-1
            self.vec.y=0
        elif dir=='right':
            self.vec.x=1
            self.vec.y=0
        elif dir=='up':
            self.vec.x=0
            self.vec.y=-1
        elif dir=='down':
            self.vec.x=0
            self.vec.y=1
    def shoot(self):
        return enemyBullet(self.rect.centerx,self.rect.centery,self.vec)        

class enemyBullet(pg.sprite.Sprite):
    def __init__(self,px,py,vec):
        super().__init__()
        self.image=pg.Surface((15,15))
        self.image.fill('yellow')
        self.rect=self.image.get_rect(center=(px,py))
        self.vec=vec
    def move(self):
        self.rect.center+=self.vec*3
    def update(self):
        self.move()
        if self.rect.centerx>500 or self.rect.centerx<0 or self.rect.centery>500 or self.rect.centery<0:
            self.kill()

class obstacle(pg.sprite.Sprite):
    def __init__(self,image,px,py):
        super().__init__()
        self.image=pg.image.load(image)
        self.rect=self.image.get_rect()
        self.rect.topleft=((px,py))

class healthTile(pg.sprite.Sprite):
    def __init__(self,px,py,attribute):
        super().__init__()
        self.image=pg.Surface((25,25))
        self.rect=self.image.get_rect(center=(px,py))
        attribute
        if attribute=='heal':
            self.image.fill('green')
            self.att='heal'
        elif attribute=='hurt':
            self.image.fill('red')
            self.att='hurt'

mapID=[
['w','w','w','w','w','w','w','w','w','w'],
['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
['w','h','w',' ',' ',' ',' ',' ',' ','w'],
['w','w','w',' ','p',' ',' ','1',' ','w'],
['w','x','w',' ',' ',' ','2',' ',' ','w'],
['w',' ','w',' ',' ','3',' ',' ',' ','w'],
['w',' ',' ',' ','4',' ',' ',' ',' ','w'],
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
tGroup=pg.sprite.Group()
eGroup=pg.sprite.Group()
hGroup=pg.sprite.Group()

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
            zGroup.add(troop('zombie.png',coloumbNum*50,rowNum*50,200))
        elif coloumb=='1':
            tGroup.add(turret(coloumbNum*50,rowNum*50,'left'))
        elif coloumb=='2':
            tGroup.add(turret(coloumbNum*50,rowNum*50,'right'))
        elif coloumb=='3':
            tGroup.add(turret(coloumbNum*50,rowNum*50,'up'))
        elif coloumb=='4':
            tGroup.add(turret(coloumbNum*50,rowNum*50,'down'))
        elif coloumb=='x':
            hGroup.add(healthTile(coloumbNum*50,rowNum*50,'hurt'))
        elif coloumb=='h':
            hGroup.add(healthTile(coloumbNum*50,rowNum*50,'heal'))


P1=player(gidle[0],px,py,rGroup,eGroup,hGroup,screen)
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
    tGroup.draw(screen)
    hGroup.draw(screen)
    for turret in tGroup:
        if turret.cd==False:
            eGroup.add(turret.shoot())
            turret.cdstate=True
            turret.cd=120
        else:
            turret.cd-=1
            if turret.cd==0:
                turret.cdstate=False
    eGroup.draw(screen)
    eGroup.update()
    pGroup.update()
    bGroup.update()
    zGroup.update(P1.x,P1.y)
    pg.display.update()


gamestate=0
shootstate=False
run=True
while run:
    clock.tick(60)

    for event in pg.event.get():
        if event.type==pg.QUIT:
            run=False
        if event.type==pg.MOUSEBUTTONDOWN and shootstate==False:
            bGroup.add(P1.shoot())

    if gamestate==0:
        gamestate=menu()

    elif gamestate==1:
        main()
        if P1.hp<=0:
            gamestate=0
        
        