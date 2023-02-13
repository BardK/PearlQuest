import pygame as pg
class gunner(pg.sprite.Sprite):

    def __init__(self, pos, images, simages, size):
        super().__init__()
        self.images = images
        self.simages = simages
        self.index = 0
        self.size = size
        self.rect = self.images[0].get_rect()
        self.rect.center = (pos[0],pos[1])
        self.sindex = 0
        self.is_shoot = False

    def shooting(self):
        self.is_shoot = True

    def attack(self, screen):
        if self.is_shoot:
            if self.sindex  >= len(self.simages):
                self.is_shoot = False
                self.sindex = 0
                screen.blit(pg.transform.scale(self.images[1], self.size), self.rect)
            else:  
                self.simage = pg.transform.scale(self.simages[int(self.sindex)], (self.size[0]*1.4, self.size[1]))
                screen.blit(self.simage, (self.rect[0]-80, self.rect[1]))
                self.sindex += 0.25




    def update(self):
        if self.is_shoot == False:
            
            if self.index >= len(self.images):
                self.index = 0
            self.image = pg.transform.scale(self.images[int(self.index)], self.size)
            self.image.set_alpha(255)
            self.index += 0.2
        else:
            self.image.set_alpha(0)
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
