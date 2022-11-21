import pygame as pg, sys, random

pg.init()
clock = pg.time.Clock()

sw=1260
sh=600
screen=pg.display.set_mode((sw,sh))
background=pg.image.load("testbackground.jpg")
pg.mouse.set_visible(False)

class Cursor(pg.sprite.Sprite):
    def __init__(self,picture):
        super().__init__()
        self.image=pg.image.load(picture)
        self.rect=self.image.get_rect()
        self.gunshot=pg.mixer.Sound("gunshot.wav")
        self.breakw=pg.mixer.Sound("break.wav")
    def shoot(self):
        self.gunshot.play()
        if pg.sprite.spritecollide(cursor,targetGroup,True):
            self.breakw.play()
    def update(self):
        self.rect.center=pg.mouse.get_pos()

class target(pg.sprite.Sprite):
    def __init__(self,picture,posx,posy):
        super().__init__()
        self.image=pg.image.load(picture)
        self.rect=self.image.get_rect()
        self.rect.center=[posx,posy]  


cursor=Cursor("cursor.png")
cursorGroup=pg.sprite.Group()
cursorGroup.add(cursor)

targetGroup=pg.sprite.Group()
for i in range(20):
    newTarget=target("target.png",random.randrange(0+32,sw-32),random.randrange(0+32,sh-32))
    targetGroup.add(newTarget)

run=True
while run:
    clock.tick(144)

    for event in pg.event.get():
        if event.type==pg.QUIT:
            run = False
        if event.type==pg.MOUSEBUTTONDOWN:
            cursor.shoot()


    screen.blit(background,(0,0))
    targetGroup.draw(screen)
    cursorGroup.draw(screen)
    cursorGroup.update()
    pg.display.update()


pg.quit()