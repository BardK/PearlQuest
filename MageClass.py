import pygame as pg
#mage player class
#this was the hardest character to make
class Mage(pg.sprite.Sprite):
    def __init__(self,images,px,py,obstacles,screen, size, animages, eGroup, tiles, enemies, MEGAGroup, progressgroup, revengance):
        super().__init__()
        #alot alot of init
        self.screen=screen
        self.images=images
        self.rect=pg.transform.scale(self.images[0], (size[0]-3, size[1]-5)).get_rect()
        self.x=px
        self.y=py
        self.lxdir='left'
        self.lydir='up'
        self.rect.topleft=((self.x,self.y))
        self.vec=pg.math.Vector2()
        self.speed=4
        self.obstacles=obstacles
        self.Progressobstacles = progressgroup
        self.MEGAGroup = MEGAGroup

        self.rNum = 90
        self.damage = 30
        self.eBullets = eGroup
        self.tiles = tiles
        self.enemies = enemies

        self.simages = animages
        self.index = 0
        self.sindex = 0
        self.is_shoot = False
        self.direction = "left"
        self.offset = 0
        self.size = size
        self.image = self.images[0]
        self.chargeNum = 10
        self.iframes = 0
        self.immune = False
        self.Miframes = 0
        self.Mimmune = False
        self.revengance = 1
        if revengance:
            self.revengance = 2

        self.hp = 120/self.revengance
        self.hp_max = 120/self.revengance
        self.target_health = 120 / self.revengance
        self.health_bar_length = 500 / self.revengance
        self.health_ratio = self.hp_max / self.health_bar_length
        self.health_change_speed = 2
        self.hitgraphic = pg.transform.scale(pg.image.load("sprites\\blood.png"), (1080,720)).convert_alpha()
        self.fireballsound = pg.mixer.Sound("sounds\\FIREBALL.ogg")
        self.fireballsound.set_volume(0.05)
        self.hitsound = pg.mixer.Sound("sounds\\p_hit.wav")
        self.hitsound.set_volume(0.7)
        self.ghosthitsound = pg.mixer.Sound("sounds\\hitsound.ogg")
        self.ghosthitsound.set_volume(0.4)
        self.healsound = pg.mixer.Sound("sounds\\heal sound.ogg")


    #take damage
    def get_damage(self,amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health < 0:
            self.hp = 0
    #heal
    def get_health(self,amount):
        if self.target_health < self.hp_max:
            self.target_health += amount
        if self.target_health > self.hp_max:
            self.target_health = self.hp_max
    #healthbar
    def advanced_health(self):
        transition_width = 0
        transition_color = (255,0,255)
        if self.hp < self.target_health:
            self.hp += self.health_change_speed
            transition_width = int((self.target_health - self.hp) / self.health_ratio)
            transition_color = (0,255,0)

        if self.hp > self.target_health:
            self.hp -= self.health_change_speed 
            transition_width = int((self.hp - self.target_health-10) / self.health_ratio)
            transition_color = (255,255,255)
            self.hitgraphic.set_alpha((self.hp - self.target_health)*3)
            self.screen.blit(self.hitgraphic, (0,0))

        health_bar_width = int(self.hp / self.health_ratio)
        health_bar = pg.Rect(10,45,health_bar_width,25)
        transition_bar = pg.Rect(health_bar.right,45,transition_width,25)

        pg.draw.rect(self.screen,(255,0,0),health_bar)	
        pg.draw.rect(self.screen,(255,255,255),(10,45,self.health_bar_length,25),4)	
        pg.draw.rect(self.screen,transition_color,transition_bar)

    #movement
    def move(self):
        keys=pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.vec.x=1
            self.lxdir='right'
            self.xdir='right'
            self.direction = "right"
        elif keys[pg.K_LEFT]:
            self.vec.x=-1
            self.lxdir='left'
            self.xdir='left'
            self.direction = "left"
        else:
            self.vec.x=0
            self.xdir=''
        if keys[pg.K_DOWN]:
            self.vec.y=1
            self.lydir='down'
            self.ydir='down'
        elif keys[pg.K_UP]:
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
    
    #checks for wall collision
    def collisionCheck(self,dir):
        if dir=='x':
            for sprite in self.obstacles:
                if self.vec.x>0 and sprite.rect.colliderect(self.rect):
                    self.x=sprite.rect.left-self.rect.width
                elif self.vec.x<0 and sprite.rect.colliderect(self.rect):
                    self.x=sprite.rect.right
            for sprite in self.Progressobstacles:
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
            for sprite in self.Progressobstacles:
                if self.vec.y>0 and sprite.rect.colliderect(self.rect):
                    self.y=sprite.rect.top-self.rect.height
                elif self.vec.y<0 and sprite.rect.colliderect(self.rect):
                    self.y=sprite.rect.bottom

        #checks for enemy bullets or ghost rects
        for e in self.eBullets:
            if e.rect.colliderect(self.rect):
                e.kill()
                self.get_damage(2)
                self.hitsound.play()
        for tile in self.tiles:
            if tile.rect.colliderect(self.rect):
                if tile.att=='heal':
                    self.get_health(100)
                    self.healsound.play()
                elif tile.att=='hurt':
                    self.get_damage(2)
                    self.hitsound.play()
                tile.kill()
        if self.hp > self.hp_max:
            self.hp = self.hp_max

        for enemy in self.enemies:
            if enemy.rect.colliderect(self.rect):
                if not self.immune:
                    self.get_damage(3)
                    self.hitsound.play()
                    self.iframes = 0
                    self.immune = True
                if self.immune:
                    self.iframes+= 1
                    if self.iframes == 75:
                        self.immune = False
        for Menemy in self.MEGAGroup:
            if Menemy.rect.colliderect(self.rect):
                if not self.Mimmune:
                    self.get_damage(6)
                    self.hitsound.play()
                    self.Miframes = 0
                    self.Mimmune = True
                if self.Mimmune:
                    self.Miframes += 1
                    if self.Miframes == 75:
                        self.Mimmune = False

    #this method is used by other characters and is called in the main code everytime you press space
    #so to avoid errors this method just does nothing. 
    def attack(self):
        return None

    #the actual attack method for the mage (it calls this method after you have released the space bar after charging)
    def FIREattack(self):
        self.ammo=bullet(self.rect.centerx,self.rect.centery,self.lxdir,self.lydir, self.chargeNum, self.revengance)
        return self.ammo

    #update function includes animation code
    def update(self):
        if self.index >= len(self.images):
            self.index = 0
        self.image = pg.transform.scale(self.images[int(self.index)] , self.size)
        self.index += 0.1

        if self.direction == "left":
            self.image = self.image
        if self.direction == "right":
            self.image = pg.transform.flip(self.image, True, False)
        self.move()
        self.advanced_health()
    
    #just a thing for animation (does nothing for mage)
    def shooting(self):
        self.is_shoot = True

    #charges when called
    def charge(self):
        self.chargeNum += 30*(1/(self.chargeNum+1))+0.1 #the charge up number increases by a non linear amount, meaning it charges faster, then slower and slower (easier to get more damage quicker)
        self.knockbackStren = self.chargeNum / 8
        if self.chargeNum > 50:                     #sets the volume according to charge
            self.fireballsound.set_volume(0.35)     
        else:
            self.fireballsound.set_volume(0.05)



#player projectile 
class bullet(pg.sprite.Sprite):
    def __init__(self,px,py,xdir,ydir, size, revengance):
        super().__init__()
        self.image= pg.transform.scale(pg.image.load("sprites\\Fireball.png"), (size, size))
        self.rect=self.image.get_rect(center=(px,py))
        self.xdir=xdir
        self.ydir=ydir
        self.rotation = 0
        self.damage = (size/6 -2) / revengance
        self.knockback = size / 12
        self.revengance = revengance
        
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


    #so the knights update takes a bunch of arguments to work, and this one doesn need these but will throw up errors if it doesnt accept it, becuase its always gonna pass in arguments
    def update(self, You, Found, An, EasterEgg, ee):
        self.move()
        self.checkbounds()
        self.rotation +=22.5
        if self.rotation % 90 == 0:
            self.image= pg.transform.rotate(self.image, self.rotation)
    def checkbounds(self):
        if self.rect.centerx>2000 or self.rect.centerx<0-200 or self.rect.centery>2000 or self.rect.centery<0-200:
            self.kill()
            return False
        else:
            return True



#the icon that shows up when you hold down the bar
class chargeicon(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("sprites\\Fireball.png")
        self.backimg = pg.image.load("sprites\\Fireball.png")
        self.rect = self.image.get_rect()
        self.chargesound = pg.mixer.Sound("sounds\\chargeup2.ogg")
        self.chargesound.set_volume(0.1)
        self.channelchannel = pg.mixer.Channel(1)

    def update(self, charge, pos):
        charge = int(charge)
        if charge % 4 == 0:
            self.image = self.backimg
        if charge % 1 == 0:
            self.rect = self.image.get_rect()
            self.image = pg.transform.scale(self.image, (charge, charge))
            self.rect = self.image.get_rect()
            self.rect.center = (pos[0]+40, pos[1]+38)
        if charge == 11:
            self.channelchannel.play(self.chargesound, -1)



#I HAVE JUST ONE QUESTION: EXPLOSIONS?
class EXPLOSIONS(pg.sprite.Sprite):
    def __init__(self,EXPLOSION, px,py, volumedamage, revengance):
        super().__init__()
        self.images = EXPLOSION
        self.image = self.images[0]
        self.rect = pg.transform.scale(self.images[0], (200,200)).get_rect()
        self.index = 0
        self.rect.center = (px,py)
        self.pos = (px,py)
        self.sound = pg.mixer.Sound("sounds\\EXPLODE.ogg")
        self.damage = volumedamage
        if volumedamage > (45/6) / revengance:
            self.sound.set_volume(0.3)
            self.size = (300,300)
        else:
            self.sound.set_volume(0.02)
            self.size = (50,50)

        if volumedamage >(150/6) / revengance:
            self.sound.set_volume(0.5)
            self.size = (900,900)
        self.sound.play()
    def explode(self):
        self.start = True
    def update(self):
        self.explode()
        if self.start == True:
            self.index += 0.25
            self.image = pg.transform.scale(self.images[int(self.index)], self.size)
            self.rect = self.image.get_rect()
            self.rect.center = (self.pos[0] + 20, self.pos[1] +20)
            if self.index >= 11:
                self.start = False
                self.index = 0
                self.kill()
