import pygame as pg
#player class for knight
class Knight(pg.sprite.Sprite):
    def __init__(self,images,px,py,obstacles,screen, size, animages, eGroup, tiles, enemies, MEGAgroup, progressgroup, revengance):
        super().__init__()
        #the usual init
        self.screen=screen
        self.images=images
        self.rect=pg.transform.scale(self.images[0], (size[0]-5, size[1]-3)).get_rect()
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
        self.MEGAGroup = MEGAgroup

        self.rNum = 40

        self.simages = animages
        self.index = 0
        self.sindex = 0
        self.is_shoot = False
        self.direction = "left"
        self.offset = 0
        self.size = size
        self.swingsound = pg.mixer.Sound("sounds\\woosh.wav")
        self.hitsound = pg.mixer.Sound("sounds\\p_hit.wav")
        self.hitsound.set_volume(0.7)
       
        self.enemies = enemies
        self.immune = False
        self.iframes = 0
        self.Miframes = 0
        self.Mimmune = False
        self.revengance = 1
        if revengance:
            self.revengance = 2
        self.hp = 350 / self.revengance
        self.hp_max = 350 / self.revengance
        self.target_health = 350 / self.revengance
        self.health_bar_length = 600 / self.revengance
        self.health_ratio = self.hp_max / self.health_bar_length
        self.health_change_speed = 2
        self.hitgraphic = pg.transform.scale(pg.image.load("sprites\\blood.png"), (1080,720)).convert_alpha()
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
#healthbar code
    def advanced_health(self):
        transition_width = 0
        transition_color = (255,0,255)
        if self.hp < self.target_health:
            self.hp += self.health_change_speed
            transition_width = int((self.target_health - self.hp) / self.health_ratio)
            transition_color = (0,255,0)

        if self.hp > self.target_health:
            self.hp -= self.health_change_speed 
            transition_width = int((self.hp - self.target_health-15) / self.health_ratio)
            transition_color = (255,255,255)
            self.hitgraphic.set_alpha((self.hp - self.target_health)*3)
            self.screen.blit(self.hitgraphic, (0,0))
        health_bar_width = int(self.hp / self.health_ratio)
        health_bar = pg.Rect(10,45,health_bar_width,25)
        transition_bar = pg.Rect(health_bar.right,45,transition_width,25)

        pg.draw.rect(self.screen,(255,0,0),health_bar)	
        pg.draw.rect(self.screen,(255,255,255),(10,45,self.health_bar_length,25),4)	
        pg.draw.rect(self.screen,transition_color,transition_bar)
#movement code
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
        
        if self.vec.magnitude()!=0:
            self.vec=self.vec.normalize()
        self.x+=self.vec.x*self.speed
        self.rect.topleft=((self.x,self.y))
        self.collisionCheck('x')
        self.y+=self.vec.y*self.speed
        self.rect.topleft=((self.x,self.y))
        self.collisionCheck('y')
        self.rect.topleft=((self.x,self.y))

#checks for collisions with walls and enemies
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
                    self.get_health(500)
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
                        
    #the attack method, creates a sword swing depending on which direction the player faces
    def attack(self):
        self.swingsound.play()
        if self.lxdir=='right':
            self.sword=sword(self.rect.centerx+self.rect.width/2,self.rect.centery,1, self.revengance)
        elif self.lxdir=='left':
            self.sword=sword(self.rect.centerx-self.rect.width/2,self.rect.centery,-1, self.revengance) 
        return self.sword
        
    #update also handles animations
    def update(self):
        self.move()
        self.advanced_health()
        if self.index >= len(self.images):
            self.index = 0
        self.image = pg.transform.scale(self.images[int(self.index)] , self.size)
        self.index += 0.1

        if self.is_shoot == True:
            self.image = pg.transform.scale(self.simages[int(self.sindex)], (self.size[0]*1.521, self.size[1]*1.19))
            self.sindex +=0.1
            if self.sindex >= len(self.simages):
                self.sindex = 0
                self.is_shoot = False
                self.image = pg.transform.scale(self.images[0] , self.size)  
        
        if self.direction == "left":
            self.offset = -36
            self.image = self.image
            if self.is_shoot:
                self.rect.topleft = (self.rect.topleft[0]+self.offset, self.rect.topleft[1]-10)
             
        if self.direction == "right":
            self.offset = 0 
            self.image = pg.transform.flip(self.image, True, False)
            if self.is_shoot:
                self.rect.topleft = (self.rect.topleft[0]+self.offset, self.rect.topleft[1]-10)

        
    #animation
    def shooting(self):
        self.is_shoot = True
    #needs this method for the mage to work
    def charge(self):
        pass


#Sword Class
class sword(pg.sprite.Sprite):
    def __init__(self,px,py,vecx, revengance):
        super().__init__()
        self.image=pg.Surface((60,60))
        self.image.fill(('red'))
        self.image.set_alpha(0)
        self.rect=self.image.get_rect()
        self.rect.center=(px,py)
        self.vec=pg.math.Vector2()
        self.vec.x=vecx
        self.backup = vecx
        self.vec.y=0
        self.damage = 40 / revengance
        self.knockback = 4
        
    def update(self,cd, px, py, dir, vecx):
        self.vec.x = vecx        #changes depending on which way the player faces
        if dir == "left":
            if self.vec.x == 0:
                self.vec.x = self.backup
            self.rect.center=(px-20,py+50)
        else:
            if self.vec.x == 0:
                self.vec.x = self.backup
            self.rect.center = (px+100, py+50)
            
        if cd<=0:
            self.kill()      #goes away when done
        else:
            pass

        