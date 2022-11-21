import pygame as pg

pg.init()
sw=300
sh=300
lcd = pg.display.set_mode((sw,sh))
pg.display.set_caption("Map gen test")
clock=pg.time.Clock()

class obstacle:
    def __init__(self,positionx,positiony,width,height,colour):
        self.x=positionx
        self.y=positiony
        self.w=width
        self.h=height
        self.colour=colour
    def draw(self, screen):
        pg.draw.rect(screen,self.colour,(self.x,self.y,self.w,self.h))

g='green'
b='blue'
r='red'
mapid=[
[g,g,g,g,g,g,g,g,g,g],
[g,g,g,g,g,g,g,g,g,g],
[g,g,g,g,g,g,g,g,g,g],
[g,g,g,g,g,g,g,g,g,g],
[g,g,g,b,g,g,g,g,g,g],
[g,g,g,b,g,g,g,g,g,g],
[g,g,b,b,b,g,g,g,g,g],
[g,g,g,g,g,g,g,g,g,g],
[g,g,g,g,g,g,g,g,g,g],
[g,g,g,g,g,g,g,g,g,g],
]

objList=[]

def drawMap():
    coloumb=-1
    row=0
    for i in mapid:
        coloumb+=1
        row=0
        for j in i:
            if j == g:
                pg.draw.rect(lcd,(0,255,0),(row*30,coloumb*30,sw/len(mapid),sh/len(mapid[row])))
            elif j == b:
                pg.draw.rect(lcd,(0,0,255),(row*30,coloumb*30,sw/len(mapid),sh/len(mapid[row])))
            elif j == r:
                pg.draw.rect(lcd,(255,0,0),(row*30,coloumb*30,sw/len(mapid),sh/len(mapid[row])))
            row+=1


run=True
while run:
    clock.tick(20)
    for event in pg.event.get():
        if event.type==pg.QUIT:
            run=False
    lcd.fill('white')
    drawMap()
    pg.display.update()


pg.quit()