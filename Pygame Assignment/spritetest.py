import pygame as pg, sys

pg.init()
clock = pg.time.Clock()

sw=1260
sh=600
screen=pg.display.set_mode((sw,sh))

class test(pg.sprite.Sprite):
    def __init__(self,px,py,w,h,colour):
        super().__init__()
        self.image=pg.Surface([w,h])
        self.image.fill(colour)
        self.rect=self.image.get_rect()
        self.rect.center=[px,py]

box=test(100,100,50,50,'green')

boxGroup=pg.sprite.Group()
boxGroup.add(box)

run=True
while run:
    clock.tick(30)

    for event in pg.event.get():
        if event.type==pg.QUIT:
            run = False
    screen.fill('black')
    boxGroup.draw(screen)
    pg.display.update()


pg.quit()