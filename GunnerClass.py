import pygame as pg
#player class for gunner (cowboy guy)
class Gunner(pg.sprite.Sprite):
    def __init__(self,images,px,py,obstacles,screen, size, animages, eGroup, tiles, enemies, MEGAGroup, progressgroup, revengance):
        super().__init__()
        #i dont know what super init really does, but it sounds cool
        self.screen=screen
        self.images = images
        self.rect=pg.transform.scale(self.images[0], (size[0]-5, size[1]-5)).get_rect()
        self.x=px
        self.y=py
        self.lxdir='left'
        self.lydir='up'
        self.rect.topleft=((self.x,self.y))
        self.vec=pg.math.Vector2()
        self.speed=4
        self.obstacles=obstacles
        self.Progressobstacles = progressgroup
        self.eBullets = eGroup
        self.tiles = tiles
        self.enemies = enemies
        self.MEGAGroup = MEGAGroup
    
        self.rNum = 18

        self.simages = animages
        self.index = 0
        self.sindex = 0
        self.is_shoot = False
        self.direction = "left"
        self.offset = 0
        self.size = size
        self.image = self.images[0]
        self.iframes = 0
        self.immune = False
        self.Miframes = 0
        self.Mimmune = False
        self.attacksound = pg.mixer.Sound("sounds\\bam.ogg")
        self.attacksound.set_volume(0.3)
        self.revengance = 1
        if revengance:
            self.revengance = 2
        self.hp = 200 / self.revengance
        self.hp_max = 200 / self.revengance
        self.target_health = 200 / self.revengance
        self.health_bar_length = 600 / self.revengance
        self.health_ratio = self.hp_max / self.health_bar_length
        self.health_change_speed = 3
        self.hitgraphic = pg.transform.scale(pg.image.load("sprites\\blood.png"), (1080,720)).convert_alpha()
        self.hitsound = pg.mixer.Sound("sounds\\p_hit.wav")
        self.hitsound.set_volume(0.7)
        self.healsound = pg.mixer.Sound("sounds\\heal sound.ogg")


    #gets hurt
    def get_damage(self,amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health < 0:
            self.hp = 0

    #gets healed
    def get_health(self,amount):
        if self.target_health < self.hp_max:
            self.target_health += amount
        if self.target_health > self.hp_max:
            self.target_health = self.hp_max

    #healthbar
    def advanced_health(self):
        transition_width = 0
        transition_color = (255,0,255)
        if self.hp < self.target_health: #HEAL
            self.hp += self.health_change_speed
            transition_width = int((self.target_health - self.hp) / self.health_ratio)
            transition_color = (0,255,0)

        if self.hp > self.target_health: #HURT
            self.hp -= self.health_change_speed 
            transition_width = (self.hp -self.target_health-10) / self.health_ratio
            transition_color = (255,255,255)
            self.hitgraphic.set_alpha((self.hp - self.target_health)*3)
            self.screen.blit(self.hitgraphic, (0,0))
        health_bar_width = int(self.hp / self.health_ratio)
        health_bar = pg.Rect(10,45,health_bar_width,25)
        transition_bar = pg.Rect(health_bar.right,45,transition_width/2, 25)

        pg.draw.rect(self.screen,(255,0,0),health_bar)	
        pg.draw.rect(self.screen,transition_color,transition_bar)
        pg.draw.rect(self.screen,(255,255,255),(10,45,self.health_bar_length,25),4)	
    
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
    
    #checks for collision with walls, enemies and enemy projectiles
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

        #checks for damage (enemies)
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

    #animation thing
    def shooting(self):
        self.is_shoot = True

    #the attack method, it returns the bullet object as it gets added to a sprite group
    def attack(self):
        self.attacksound.play()
        if self.direction == "right":
            self.ammo=bullet(self.rect.centerx+35,self.rect.centery+20,self.lxdir,self.lydir, self.obstacles, self.revengance)
        elif self.direction == "left":
            self.ammo=bullet(self.rect.centerx-30,self.rect.centery+20,self.lxdir,self.lydir, self.obstacles, self.revengance)
        return self.ammo

    #animation also handled here
    def update(self):
        self.move()
        self.advanced_health()
        if self.index >= len(self.images):
            self.index = 0
        self.image = pg.transform.scale(self.images[int(self.index)] , self.size)
        self.index += 0.1

        if self.is_shoot == True:
            self.image = pg.transform.scale(self.simages[int(self.sindex)], (self.size[0]*1.514, self.size[1]))
            self.sindex +=1/3
            if self.sindex >= len(self.simages):
                self.sindex = 0
                self.is_shoot = False
                self.image = pg.transform.scale(self.images[0] , self.size)  
        
        if self.direction == "left":
            self.offset = -37
            self.image = self.image
            if self.is_shoot:
                self.rect.topleft = (self.rect.topleft[0]+self.offset, self.rect.topleft[1])
             
        if self.direction == "right":
            self.offset = 0 
            self.image = pg.transform.flip(self.image, True, False)
    #needed for mage
    def charge(self):
        pass
        

#the gunners most important asset: his bullets
class bullet(pg.sprite.Sprite):
    def __init__(self,px,py,xdir,ydir, obstacles, revengance):
        super().__init__()
        self.image=pg.Surface((10,10))
        self.image = pg.transform.scale(pg.image.load("sprites\\Bulleto.png"), (50,20))
        self.rect=self.image.get_rect(center=(px,py))
        self.xdir=xdir
        self.ydir=ydir
        self.obstacles=obstacles
        self.vec=pg.math.Vector2()
        self.damage = 8 / revengance
        self.knockback = 0.6
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

        #rotates bullet depending on which way the player shot it at
        if (self.vec.x <0 and self.vec.y<0) or (self.vec.x>0 and self.vec.y>0):
            self.image = pg.transform.rotate(self.image, -45)
        if (self.vec.x >0 and self.vec.y<0) or (self.vec.x <0 and self.vec.y>0):
            self.image = pg.transform.rotate(self.image, 45)

        if self.vec.x == 0:
            self.image = pg.transform.rotate(self.image, 90)

    #moves, and detects if hits a wall
    def move(self):
        self.rect.center+=self.vec*12
        for sprite in self.obstacles:
            if sprite.rect.colliderect(self.rect):
                self.kill()

    def checkbounds(self):
        if self.rect.centerx>1080 or self.rect.centerx<0 or self.rect.centery>720 or self.rect.centery<0:
            self.kill()
            return False
        else:
            return True

    def update(self, cd, px, py, dir, ee):
        self.move()
        self.checkbounds()

