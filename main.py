import pygame as pg
from button import Button, fade
import glob
from idleanims import idle_anims, titlebob
from math import sin
from playerclass import gunner
pg.init()
#clock setup
clock = pg.time.Clock()

#colours
WHITE = (255,255,255)
BLACK = (0,0,0)

#screen
width = 1080
height = 720
screen = pg.display.set_mode((width, height))

# sprites (static)
bg = pg.transform.scale(pg.image.load("sprites\mountain1.png"), (width, height))
buttimg = pg.image.load("sprites\woodenbutton.png").convert_alpha()
alagard = pg.font.Font('sprites/alagard.ttf', 60)
alagardSMOL = pg.font.Font('sprites/alagard.ttf', 30)
foretbg = pg.transform.scale(pg.image.load("sprites/forestbg.png"), (width, height))
title = pg.transform.scale(pg.image.load("sprites/Title.png"), (600,200))
bg1 = pg.image.load("sprites\ForestSplash.png")

#animation sprites
gidle = [pg.image.load(img) for img in glob.glob("Gunner\\*.png")]
widle = [pg.image.load(img) for img in glob.glob("warriordle\\*.png")]
midle = [pg.image.load(img) for img in glob.glob("mageidle\\*.png")]
thefade = fade((width, height))
gshoot = [pg.image.load(img) for img in glob.glob("gunner shoot\\*.png")]

#set up classes
knightbutt = idle_anims((250,250), (width/4,height/2 + 50), 1, widle)
gunnerbutt = idle_anims((260,260), (width/2 + 15,height/2 + 50), 1, gidle)
magebutt = idle_anims((250,250), (3*width/4, height/2 +50), 1, midle)
titleanim = titlebob(title)


#variables
game_state = "menu"
char = "bazinga"
has_selected = False


fading = True

#button classes
startbutt = Button(image = buttimg, colour = BLACK , pos = ((width/2),(height/2 + 50)), size = (294,120), text_inp= 'START', font = alagard)
exitbutt = Button(image =buttimg, colour= BLACK, pos = ((width/2),(height/2+200)), size = (294,120), text_inp= 'EXIT', font = alagard)
selecbutt = Button(image =buttimg, colour= BLACK, pos = ((width/2),(height/2-200)), size = (1000,200),
 text_inp= 'SELECT YOUR CHARACTER', font = alagard)

#main menu function
def main_menu():
    global game_state
    global thefade
    mouse_pos = pg.mouse.get_pos()

    def update_screen(screen):
        screen.blit(bg, (0,0))
        startbutt.update(screen)
        exitbutt.update(screen)
        titleanim.update(screen)
        clock.tick(30)
    update_screen(screen)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if exitbutt.check_clicked(mouse_pos) == True:
                pg.quit()
            if startbutt.check_clicked(mouse_pos) ==True:
                game_state = "fading1"

    thefade.fadein(screen)

        
#character select function
def charaselect():
    global char
    global game_state
    screen.fill('white')
    screen.blit(foretbg, (0,0))

    mouseposget = pg.mouse.get_pos() 
    knightbutt.checkhover(mouseposget)
    gunnerbutt.checkhover(mouseposget)
    magebutt.checkhover(mouseposget)
    knightbutt.update(screen)
    gunnerbutt.update(screen)
    magebutt.update(screen)
    selecbutt.update(screen)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit() 
        if event.type == pg.MOUSEBUTTONDOWN:
            if knightbutt.checkhover(mouseposget):
                char = "knight"
                game_state = "fade2"
            elif gunnerbutt.checkhover(mouseposget):
                char = "gunner"
                game_state = "fade2"
            elif magebutt.checkhover(mouseposget):
                char = "mage"
                game_state = "fade2"


#DEfine character selection function
def selectedchar(char): 
    if char == "gunner":
        player = gunner((0,0), gidle, gshoot, (200,200))
        return(player)
    elif char == "mage":
    # player = mage()
        pass
    elif char == "knight":
        pass


#floor 1:
def floor1(player):
    global game_state
    screen.fill(WHITE)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.shooting()
    
    player.update()
    player.attack(screen)
    player.draw(screen)


#MAIN GAME LOOP

while True:
    if game_state == "menu":
        main_menu()
        pg.display.flip()
    elif game_state == "fading1":
        if thefade.isdone != True:
            main_menu()
            thefade.fadein(screen)
            thefade.fadept1()
            pg.display.flip()
        else:
            game_state = "char_selec"

    elif game_state == "char_selec":
        charaselect()
        thefade.fadeout(screen)
        pg.display.update()
        clock.tick(30)

    elif game_state == "fade2":
        if has_selected == False:
            thefade.reset((width, height))
            player = selectedchar(char)
            has_selected = True

        if thefade.isdone != True:
            charaselect()
            thefade.fadein(screen)
            thefade.fadept1()
            pg.display.flip()
        else:
            game_state = "1F load"

    elif game_state == "1F load":
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    thefade.reset((width, height))
                    game_state = "1F fade"
        
        screen.blit(bg1, (0,0))
        screen.blit(alagardSMOL.render("Press Space To Start", True, WHITE), (20,650))
        thefade.fadeout(screen)
        clock.tick(30)
        pg.display.flip()

    elif game_state == "1F fade":
        if thefade.isdone != True:
            screen.blit(bg1, (0,0))
            thefade.fadein(screen)
            thefade.fadept1()
            pg.display.flip()
        else:
            game_state = "1F"

    elif game_state == "1F":
        floor1(player)

        pg.display.flip()
        




"""
        player.update()
        player.draw(screen)
        player.attack(screen)
        clock.tick(30)
        pg.display.update()
        
"""


