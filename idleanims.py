import pygame as pg
import math

#class for the player selection screen buttons (the characters on the character selection screen)
class idle_anims:
    def __init__(self, size, center, speed, images):
        self.speed = speed
        self.size = size
        self.images = images
        self.rect = self.images[0].get_rect()
        self.rect.update(1,1,size[0], size[1])
        self.rect.center = (center[0], center[1])
        self.Ishover = False
        self.index = 0
        self.is_selected = False

    #checks for hover
    def checkhover(self, mousepos):
        if mousepos[0] in range(self.rect.left, self.rect.right) and mousepos[1] in range(self.rect.top, self.rect.bottom):
            self.Ishover = True
            return True
            
        else:
            self.Ishover = False
            return False
    #if hovering, animate it
    def update(self,screen):
        if self.Ishover == False:
            screen.blit((pg.transform.scale(self.images[0] , self.size)), self.rect)

        if self.Ishover == True:
            if self.index  >= len(self.images):
                self.index = 0
            
            screen.blit(pg.transform.scale(self.images[int(self.index)], self.size), self.rect)
            self.index += 0.2
        

#the title that bobs up and down (yes i made a class for it classes are nice)
class titlebob:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.ypos = 200
        self.rect.center = (540, self.ypos)
        self.goindown = True
        self.x = 0

    def update(self, screen):
        self.ypos = math.sin(self.x) * 5 + 150 #i could code an actual thing where it goes up and down using vectors and such, or i could just set its y position to a sin function
        self.x += 0.2
        self.rect.center = (540, self.ypos)
        screen.blit(self.image, self.rect)
        
