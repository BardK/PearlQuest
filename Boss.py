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
    def __init__(self,image,px,py,obstacles,screen,eBola):
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
        self.eBola=eBola
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
        self.x+=self.vec.x*self.speed/2
        self.rect.topleft=((self.x,self.y))
        self.collisionCheck('x')
        self.y+=self.vec.y*self.speed/2
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
        for e in self.eBola:
            if e.rect.colliderect(self.rect):
                e.kill()
                self.hp-=10
                print (self.hp)

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

class boss(pg.sprite.Sprite):
    def __init__(self,px,py):
        super().__init__()
        self.image=pg.Surface((50,50))
        self.image.fill('red')
        self.rect=self.image.get_rect()
        self.x=px
        self.y=py
        self.rect.center=((self.x,self.y))
        self.vec1=pg.math.Vector2((-1,0))
        self.vec2=pg.math.Vector2((-0.71,-0.71))
        self.vec3=pg.math.Vector2((0,-1))
        self.vec4=pg.math.Vector2((0.71,-0.71))
        self.vec5=pg.math.Vector2((1,0))
        self.vec6=pg.math.Vector2((0.71,0.71))
        self.vec7=pg.math.Vector2((0,1))
        self.vec8=pg.math.Vector2((-0.71,0.71))
        self.hp=100
        self.aState=0
        self.mState=0
        self.sDone=True
        self.cd=0
        self.mTime=0
        self.mDone=True
        self.dead=False
        self.phase=1

    def attackOne(self):
        self.mState+=1
        if self.sDone:
            if self.aState==0:
                self.aState+=1
                self.cd=10
                return enemyBullet(self.rect.centerx,self.rect.centery,self.vec1)
            elif self.aState==1:
                self.aState+=1
                self.cd=10
                return enemyBullet(self.rect.centerx,self.rect.centery,self.vec2)
            elif self.aState==2:
                self.aState+=1
                self.cd=10
                return enemyBullet(self.rect.centerx,self.rect.centery,self.vec3)
            elif self.aState==3:
                self.aState+=1
                self.cd=10
                return enemyBullet(self.rect.centerx,self.rect.centery,self.vec4)
            elif self.aState==4:
                self.aState+=1
                self.cd=10
                return enemyBullet(self.rect.centerx,self.rect.centery,self.vec5)
            elif self.aState==5:
                self.aState+=1
                self.cd=10
                return enemyBullet(self.rect.centerx,self.rect.centery,self.vec6)
            elif self.aState==6:
                self.aState+=1
                self.cd=10
                return enemyBullet(self.rect.centerx,self.rect.centery,self.vec7)
            elif self.aState==7:
                self.aState=0
                self.cd=10
                return enemyBullet(self.rect.centerx,self.rect.centery,self.vec8)
        
    def collisionCheck(self,damageSprites):
        for sprite in damageSprites:
            if sprite.rect.colliderect(self.rect):
                sprite.kill()
                self.hp-=1
                print (self.hp)
    def healthCheck(self):
        if self.hp==0:
            self.kill()
            self.dead=True

    
    def move(self):
        if self.mTime==0:
            self.rect.center+=self.vec1*1.5
        elif self.mTime==1:
            self.rect.center+=self.vec3*1.5
        elif self.mTime==2:
            self.rect.center+=self.vec5*2
        elif self.mTime==3:
            self.rect.center+=self.vec7*2

    def update(self, damagesprites):
        self.collisionCheck(damagesprites)
        self.healthCheck()





class enemyBullet(pg.sprite.Sprite):
    def __init__(self,px,py,vec):
        super().__init__()
        self.image=pg.Surface((15,15))
        self.image.fill('yellow')
        self.rect=self.image.get_rect(center=(px,py))
        self.vec=vec
        self.vec=self.vec.normalize()
    def move(self):
        self.rect.center+=self.vec.normalize()*3
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


mapID=[
['w','w','w','w','w','w','w','w','w','w'],
['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
['w',' ',' ',' ',' ',' ',' ','p',' ','w'],
['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
['w',' ',' ',' ',' ',' ',' ','b',' ','w'],
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
fGroup=pg.sprite.Group()


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
        elif coloumb=='b':
            Boss=boss(coloumbNum*50,rowNum*50)
            fGroup.add(Boss)
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


P1=player(gidle[0],px,py,rGroup,screen,eGroup)
pGroup=pg.sprite.Group()
pGroup.add(P1)

def menu():
    keys=pg.key.get_pressed()
    if keys[pg.K_0]:
        return 1
    else:
        return 0

def bossFight():
    if Boss.dead==False:
        if Boss.mState<30 and Boss.mDone:
            if Boss.cd==0:
                eGroup.add(Boss.attackOne())
            else:
                Boss.cd-=1
        elif Boss.mState<40 and Boss.mDone:
            Boss.attackOne()
            Boss.sDone=False
        elif Boss.mState==40 and Boss.mDone:
            Boss.mState=100
            Boss.sDone=True
            Boss.mDone=False
        if not Boss.mDone:
            Boss.move()
            Boss.mState-=1
            if Boss.mState==0:
                if Boss.mTime!=3:
                    Boss.mTime+=1
                else:
                    Boss.mTime=0
                Boss.mDone=True

def main():
    screen.fill('black')
    rGroup.draw(screen)
    pGroup.draw(screen)
    zGroup.draw(screen)
    bGroup.draw(screen)
    tGroup.draw(screen)
    fGroup.draw(screen)
    for turret in tGroup:
        if turret.cd==False:
            eGroup.add(turret.shoot())
            turret.cdstate=True
            turret.cd=120
        else:
            turret.cd-=1
            if turret.cd==0:
                turret.cdstate=False
    bossFight()
    eGroup.draw(screen)
    fGroup.update(bGroup)
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
        
        