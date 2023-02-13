import pygame as pg
import random
from MageClass import EXPLOSIONS
import glob

#boss class
class boss(pg.sprite.Sprite):
    def __init__(self,px,py, images, bGroup, char):
        super().__init__()
        #a ton of init 
        self.images= images
        self.rect=pg.transform.scale(self.images[0], (225,300)).get_rect()
        self.image = self.images[0]
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
        self.HP=750
        self.aState=0
        self.mState=0
        self.sDone=True
        self.cd=0
        self.mTime=0
        self.mDone=True
        self.dead=False
        self.phase=1
        self.index = 0
        self.attacks = bGroup
        self.playerchar = char
        self.explosion = [pg.image.load(img) for img in glob.glob("sprites\\EXPLOSIONS\\*.png")]
        self.hitsound = pg.mixer.Sound("sounds\\g_hit.wav")
        self.hitsound.set_volume(0.2)
        self.deathsound = pg.mixer.Sound("sounds\\g_die2.wav")
        self.deathsound.set_volume(0.6)
        self.is_immune = False
        self.immuneTimer = 0
        self.healthpercent = 10

    #crazy spiral attack
    def attackOne(self):
        self.healthpercent = int(self.HP / 75) 
        self.mState+=1
        if self.sDone:
            if self.aState==0:
                self.aState+=1
                self.cd=2+self.healthpercent
                return BossBullet(self.rect.centerx-70,self.rect.centery-15,self.vec1)
            elif self.aState==1:
                self.aState+=1
                self.cd=2+self.healthpercent
                return BossBullet(self.rect.centerx-70,self.rect.centery-15,self.vec2)
            elif self.aState==2:
                self.aState+=1
                self.cd=2+self.healthpercent
                return BossBullet(self.rect.centerx-70,self.rect.centery-15,self.vec3)
            elif self.aState==3:
                self.aState+=1
                self.cd=2+self.healthpercent
                return BossBullet(self.rect.centerx-70,self.rect.centery-15,self.vec4)
            elif self.aState==4:
                self.aState+=1
                self.cd=2+self.healthpercent
                return BossBullet(self.rect.centerx-70,self.rect.centery-15,self.vec5)
            elif self.aState==5:
                self.aState+=1
                self.cd=2+self.healthpercent
                return BossBullet(self.rect.centerx-70,self.rect.centery-15,self.vec6)
            elif self.aState==6:
                self.aState+=1
                self.cd=2+self.healthpercent
                return BossBullet(self.rect.centerx-70,self.rect.centery-15,self.vec7)
            elif self.aState==7:
                self.aState=0
                self.cd=2+self.healthpercent
                return BossBullet(self.rect.centerx-70,self.rect.centery-15,self.vec8)
    
    #checks for collision with player projectiles
    def collisionCheck(self, BoomGroup):
        for sprite in self.attacks:
            if sprite.rect.colliderect(self.rect):
                if self.playerchar == "mage":
                    BoomGroup.add(EXPLOSIONS(self.explosion, self.rect.centerx, self.rect.centery, sprite.damage, sprite.revengance))
                self.HP-= sprite.damage
                self.hitsound.play()
                sprite.kill()
        for BOOMsprite in BoomGroup: 
            if BOOMsprite.rect.colliderect(self.rect) and not self.is_immune:
                self.HP -= BOOMsprite.damage * 2.4
                self.is_immune = True
            if self.is_immune:
                self.immuneTimer += 1
                if self.immuneTimer >= 50:
                    self.is_immune = False
                    self.immuneTimer = 0
    #checks for death
    def healthCheck(self):
        if self.HP<=0:
            self.kill()
            self.dead=True

    #movement phase
    def move(self):
        if self.mTime==0:
            self.rect.center+=self.vec1*5
        elif self.mTime==1:
            self.rect.center+=self.vec3*4
        elif self.mTime==2:
            self.rect.center+=self.vec5*5
        elif self.mTime==3:
            self.rect.center+=self.vec7*4
        
    #basic animation code
    def animate(self, size):
        self.image = pg.transform.scale(self.images[int(self.index)], size)
        self.index += 0.1
        if self.index >= len(self.images):
            self.index = 0
        if self.mTime == 2 and not self.mDone:
            self.image = pg.transform.flip(self.image, True, False)

    #the boss healthbar
    def healthbar(self, screen):
        self.HPbarrect = pg.rect.Rect(165, 650, self.HP, 50)
        pg.draw.rect(screen, 'red', self.HPbarrect, border_radius=4)
        self.barrect = pg.rect.Rect(165, 650, 750, 50)
        pg.draw.rect(screen, (247,207,73), self.barrect, 10, 5)

    #update function
    def update(self, screen, BoomGroup):
        self.healthbar(screen)
        self.animate((225,300))
        self.collisionCheck(BoomGroup)
        self.healthCheck()


#seperate class for the boss's projeciles
class BossBullet(pg.sprite.Sprite):
    def __init__(self,px,py,vec):
        super().__init__()
        self.image=pg.transform.scale(pg.image.load("sprites\\Googbal.png"), (30,30))
        self.rect=self.image.get_rect(center=(px,py))
        self.vec=vec
        self.vec=self.vec.normalize()
        self.rotate = random.randint(0,3)
        self.image = pg.transform.rotate(self.image, self.rotate*90)
        self.popsound = pg.mixer.Sound("sounds\\pop.ogg")
        self.popsound.set_volume(0.2)
        self.popsound.play()
    def move(self):
        self.rect.center+=self.vec.normalize()*3
    def update(self):
        self.move()
        if self.rect.centerx>1080 or self.rect.centerx<0 or self.rect.centery>720 or self.rect.centery<0:
            self.kill()




#the boss ai
def bossFight(Boss, eGroup):
    if Boss.dead==False:
        if Boss.mState<20 and Boss.mDone:
            if Boss.cd==0:
                eGroup.add(Boss.attackOne())
            else:
                Boss.cd-=1
        elif Boss.mState<30 and Boss.mDone:
            Boss.attackOne()
            Boss.sDone=False
        elif Boss.mState==30 and Boss.mDone:
            Boss.mState=50
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