import pygame as pg
from math import sqrt
from MageClass import EXPLOSIONS
import glob
from math import sin, radians

#ghost class
class troop(pg.sprite.Sprite):
    def __init__(self,picture,positionx,positiony,visionR,attacks, screen, character):
        super().__init__()
        self.x=positionx
        self.y=positiony
        self.image=picture
        self.rect=self.image.get_rect()
        self.rect.topleft=(self.x,self.y)
        self.speed=1
        self.vec=pg.math.Vector2()
        self.vRange=visionR
        self.attacks=attacks
        self.knockback=False
        self.knockbackStren = 0
        self.kx=0
        self.ky=0
        self.HP=100
        self.damagedsprite = pg.transform.scale(pg.image.load("sprites\\ghost_damaged.png").convert_alpha(), (46,75))
        self.screen = screen
        self.hitsound = pg.mixer.Sound("sounds\\g_hit.wav")
        self.hitsound.set_volume(0.2)
        self.deathsound = pg.mixer.Sound("sounds\\g_die2.wav")
        self.deathsound.set_volume(0.6)
        self.playerchar = character
        self.explosion = [pg.image.load(img) for img in glob.glob("sprites\\EXPLOSIONS\\*.png")]
        self.opacitynum = 0
        self.is_immune = False
        self.immuneTimer = 0
        self.alertedsound = pg.mixer.Sound("sounds\\spotted.ogg")
        self.alerted = False

    #chases the player's x and y
    def chase(self,targetx,targety):
        dx=targetx-self.x
        dy=targety-self.y
        inRange=sqrt(dx**2+dy**2)<self.vRange

        if inRange==True:
            if not self.alerted:
                self.alertedsound.play()
                self.alerted = True
            self.vec.x=dx
            self.vec.y=dy

        if self.vec.magnitude()!=0:
            self.vec=self.vec.normalize()
        self.x+=self.vec.x*self.speed
        self.y+=self.vec.y*self.speed
        self.rect.topleft=((self.x,self.y))

        if self.knockback==True:
            if self.knockbackNum==0:
                self.knockback=False
            self.x+=self.kx*self.knockbackStren
            self.y+=self.ky*self.knockbackStren
            self.rect.topleft=((self.x,self.y))
            self.knockbackNum-=1
            self.damagedsprite.set_alpha(self.knockbackNum*15)
            self.screen.blit(self.damagedsprite, (self.x-2, self.y))

    #detects being hit by player attacks
    def isHit(self, BoomGroup):
        for sprite in self.attacks:
            if sprite.rect.colliderect(self.rect):
                if self.playerchar == "mage":
                    BoomGroup.add(EXPLOSIONS(self.explosion, self.x, self.y, sprite.damage, sprite.revengance))
                self.HP-= sprite.damage 
                self.hitsound.play()

                sprite.kill()
                self.kx=sprite.vec.x
                self.ky=sprite.vec.y
                self.knockbackStren = sprite.knockback
                self.knockback=True
                self.knockbackNum=15
        for BOOMsprite in BoomGroup: 
            if BOOMsprite.rect.colliderect(self.rect) and not self.is_immune:
                self.HP -= BOOMsprite.damage * 2.2
                self.is_immune = True
            if self.is_immune:
                self.immuneTimer += 1
                if self.immuneTimer >= 50:
                    self.is_immune = False
                    self.immuneTimer = 0
                
    #checks for death
    def isDead(self):
        if self.HP<=0:
            self.deathsound.play()
            self.kill()

    #update function
    def update(self,targetx,targety, BoomGroup):
        self.chase(targetx,targety)
        self.isHit(BoomGroup)
        self.isDead()
        self.opacitynum += 3
        self.image.set_alpha(int(50*sin(radians(self.opacitynum))+199)) #sets opacity to be oscilating, makes a nice animation with minimal effort
        if self.opacitynum >= 360:
            self.opacitynum = 0



#archer class
class turret(pg.sprite.Sprite):
    def __init__(self,px,py,dir):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load("sprites\\Archer.png"), (72,72))
        self.rect=self.image.get_rect(topleft=(px,py))
        self.vec=pg.math.Vector2()
        self.cd=0
        self.cdstate=False
        self.dir = dir
        if dir=='left':
            self.vec.x=-1
            self.vec.y=0
        elif dir=='right':
            self.vec.x=1
            self.vec.y=0
            self.image = pg.transform.flip(self.image, True, False)
        elif dir=='up':
            self.vec.x=0
            self.vec.y=-1
            self.image = pg.transform.flip(self.image, True, False)
        elif dir=='down':
            self.vec.x=0
            self.vec.y=1
    def shoot(self):
        return enemyBullet(self.rect.centerx,self.rect.centery,self.vec, self.dir)        


#archer arrow
class enemyBullet(pg.sprite.Sprite):
    def __init__(self,px,py,vec, dir):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load("sprites\\arrow.png"), (44,10)).convert_alpha()
        self.rect=self.image.get_rect(center=(px,py))
        self.vec=vec
        self.dir= dir
        if self.dir == "left":
            self.image = pg.transform.flip(self.image, True, False)
        elif self.dir == "up":
            self.image = pg.transform.rotate(self.image, 90)
        elif self.dir == "down":
            self.image = pg.transform.rotate(self.image, -90)
    def move(self):
        self.rect.center+=self.vec*3
    def update(self):
        self.move()
        if self.rect.centerx>1080 or self.rect.centerx<0 or self.rect.centery>720 or self.rect.centery<0:
            self.kill()


#makes tiles (spikes or healing pads)
class healthTile(pg.sprite.Sprite):
    def __init__(self,px,py,attribute):
        super().__init__()
        if attribute=='heal':
            self.image = pg.transform.scale(pg.image.load("sprites\\Health pickup.png"), (72,72)).convert_alpha()
            self.att='heal'
        elif attribute=='hurt':
            self.image=  pg.transform.scale(pg.image.load("sprites\\Spikes.png"), (72,72)).convert_alpha()
            self.att='hurt'
        self.rect=self.image.get_rect(topleft=(px,py))


#exit portal class because classes are cool
class exitportal(pg.sprite.Sprite):
    def __init__(self, px, py):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load("sprites\\Portal.png"), (350,500))
        self.rect = self.image.get_rect(center = (px,py))



# GHOST BOSS ----------------------------------------------------------------------------------------------------------------------------------------
#ghost boss (scary big ghost guy) class
#uses the same code as the regular ghost with some value adjustments 
class megatroop(pg.sprite.Sprite):
    def __init__(self,positionx,positiony,visionR,attacks, screen, character):
        super().__init__()
        self.x=positionx
        self.y=positiony
        self.image=pg.transform.scale(pg.image.load("sprites\\megaghost.png"), (150, 150))
        self.rect=self.image.get_rect()
        self.rect.topleft=(self.x,self.y)
        self.speed=1.4
        self.vec=pg.math.Vector2()
        self.vRange=visionR
        self.attacks=attacks
        self.knockback=False
        self.knockbackStren = 0
        self.kx=0
        self.ky=0
        self.HP = 750
        self.screen = screen
        self.hitsound = pg.mixer.Sound("sounds\\g_hit.ogg")
        self.hitsound.set_volume(0.2)
        self.deathsound = pg.mixer.Sound("sounds\\g_die.ogg")
        self.deathsound.set_volume(0.8)
        self.playerchar = character
        self.explosion = [pg.image.load(img) for img in glob.glob("sprites\\EXPLOSIONS\\*.png")]
        pg.mixer.Sound("sounds\\MEGAlaugh.ogg").play()
        self.opacitynum = 0
        self.is_immune = False
        self.immuneTimer = 0

        self.barlength = 750
        self.barrect = pg.rect.Rect(100, 650, 900, 50)


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

        if self.knockback==True:
            if self.knockbackNum==0:
                self.knockback=False
            self.x+=self.kx*self.knockbackStren
            self.y+=self.ky*self.knockbackStren
            self.rect.topleft=((self.x,self.y))
            self.knockbackNum-=1
        


    def isHit(self, BoomGroup):
        for sprite in self.attacks:
            if sprite.rect.colliderect(self.rect):
                if self.playerchar == "mage":
                    BoomGroup.add(EXPLOSIONS(self.explosion, self.x, self.y, sprite.damage, sprite.revengance))
                self.HP-= sprite.damage
                self.hitsound.play()
                sprite.kill()
                self.kx=sprite.vec.x
                self.ky=sprite.vec.y
                self.knockbackStren = sprite.knockback/2
                self.knockback=True
                self.knockbackNum=15
        for BOOMsprite in BoomGroup: 
            if BOOMsprite.rect.colliderect(self.rect) and not self.is_immune:
                self.HP -= BOOMsprite.damage * 2.2
                self.is_immune = True
            if self.is_immune:
                self.immuneTimer += 1
                if self.immuneTimer >= 50:
                    self.is_immune = False
                    self.immuneTimer = 0

                
    def isDead(self):
        if self.HP<=0:
            self.deathsound.play()
            self.kill()

    def healthbar(self, screen):
        self.hpbarrect = pg.rect.Rect(165, 650, self.HP, 50)
        pg.draw.rect(screen, 'red', self.hpbarrect, border_radius=4)
        self.barrect = pg.rect.Rect(165, 650, 750, 50)
        pg.draw.rect(screen, (247,207,73), self.barrect, 10, 5)

    def update(self,targetx,targety, BoomGroup, screen):
        self.healthbar(screen)
        self.chase(targetx,targety)
        self.isHit(BoomGroup)
        self.isDead()
        self.opacitynum += 2
        self.image.set_alpha(int(127.5*sin(radians(self.opacitynum))+127.5))
        if self.opacitynum >= 360:
            self.opacitynum = 0