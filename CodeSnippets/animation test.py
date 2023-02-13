import glob
import pygame as pg

pg.init()

clock = pg.time.Clock()
#set up screen
width = 1080
height = 720
screen = pg.display.set_mode((width, height))

WHITE = (255,255,255)

gimages = [pg.image.load(img) for img in glob.glob("Gunner\\*.png")]
gsimages = [pg.image.load(img) for img in glob.glob("gunner shoot\\*.png")]

wimages = [pg.image.load(img) for img in glob.glob("warriordle\\*.png")]
wsimages = [pg.image.load(img) for img in glob.glob("warriorswing\\*png")]
#player class
class gunner():

    def __init__(self, pos, images, simages, size, ):
        self.images = images
        self.simages = simages
        self.index = 0
        self.size = size
        self.rect = self.images[0].get_rect()
        self.rect.center = (pos[0],pos[1])
        self.sindex = 0
        self.is_shoot = False
        self.direction = "left"
        self.offset = 0
      #  self.projectile = pg.transform.scale(projectile, projsize)
      #  self.projrect = self.projectile.get_rect()

    #shooting actually means swinging
    def shooting(self):
        self.is_shoot = True
   #update
    def update2(self):
        if self.index >= len(self.images):
            self.index = 0
        self.image = pg.transform.scale(self.images[int(self.index)] , self.size)
        self.index += 0.25

        if self.is_shoot == True:
            self.image = pg.transform.scale(self.simages[int(self.sindex)], (self.size[0]*1.4, self.size[1]))
            self.sindex +=0.5
            if self.sindex >= len(self.simages):
                self.sindex = 0
                self.is_shoot = False
                self.image = pg.transform.scale(self.images[0] , self.size)  
        
        if self.direction == "left":
            self.offset = -80
            self.image = self.image
             
        if self.direction == "right":
            self.offset = 0 
            self.image = pg.transform.flip(self.image, True, False)
        


    def draw(self, screen):
        if self.is_shoot != True:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(self.image, (self.rect[0] + self.offset, self.rect[1]))
        

def main():
    mcree =  gunner([width/2, height/2], gimages, gsimages, (200,200))
    running = True
    while running:
        screen.fill(WHITE)
        keyboardbools = pg.key.get_pressed()
        mcree.update2()
        mcree.draw(screen)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
        if keyboardbools[pg.K_SPACE]:
            mcree.shooting()
        if keyboardbools[pg.K_RIGHT]:
            mcree.direction = "right"
        if keyboardbools[pg.K_LEFT]:
            mcree.direction = "left"

        #mcree.update()
        clock.tick(30)
        pg.display.update()

main()

