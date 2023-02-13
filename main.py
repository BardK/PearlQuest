#python modules
import pygame as pg
import glob
from math import sin
import random
#Pearl Quest modules
from KnightClass import Knight , sword
from LevelHandler import obstacle, FloorTile, ProgressObstacle
from mapobjects import troop, turret, enemyBullet, healthTile, exitportal, megatroop
from levels import *
from GunnerClass import Gunner
from MageClass import Mage, chargeicon, EXPLOSIONS
from Boss import boss, BossBullet, bossFight
from idleanims import idle_anims, titlebob
from button import Button, fade


pg.init()
pg.mixer.set_num_channels(10)
pg.mixer.set_reserved(2)
#clock setup
clock = pg.time.Clock()

#colours
WHITE = (255,255,255)
BLACK = (0,0,0)

#screen
width = 1080
height = 720
screen = pg.display.set_mode((width, height))
pg.display.set_caption('Pearl Quest!!')
pg.display.set_icon(pg.transform.scale(pg.image.load("sprites\\Googbal.png"), (20,20)))

#loading sprites -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# sprites (static)
loading = pg.transform.scale(pg.image.load("sprites\\loading.png"), (width, height))
screen.blit(loading, (0,0))
pg.display.update()
bg = pg.transform.scale(pg.image.load("sprites\\mountain1.png"), (width, height))
buttimg = pg.image.load("sprites\\woodenbutton.png").convert_alpha()
alagard = pg.font.Font('sprites\\alagard.ttf', 60)
alagardSMOL = pg.font.Font('sprites\\alagard.ttf', 30)
foretbg = pg.transform.scale(pg.image.load("sprites\\forestbg.png"), (width, height))
title = pg.transform.scale(pg.image.load("sprites\\Title.png"), (600,200))
bg1 = pg.image.load("sprites\\ForestSplash.png")
bg2 = pg.image.load("sprites\\bg2.png")
bg3 = pg.image.load("sprites\\bg3.png")
bg4 = pg.image.load("sprites\\skyload.png")
bg5 = pg.image.load("sprites\\Final tower.png")
ghosts = [pg.image.load(img) for img in glob.glob("sprites\\ghosts\\*.png")]
screeneffect = pg.transform.scale(pg.image.load("sprites\\screeneffect.png"), (width, height))
F1tile = pg.image.load("sprites\\grass.png")
F1wall = pg.image.load("sprites\\wood.png")
F2tile = pg.image.load("sprites\\Sand.png")
F2wall = pg.image.load("sprites\\sandwalls.png")
F3tile = pg.image.load("sprites\\water.png")
F3wall = pg.image.load("sprites\\waterwall.png")
F4tile = pg.image.load("sprites\\Cloud.png")
F4wall = pg.image.load("sprites\\castlewalls.png")
F5tile = pg.image.load("sprites\\evilfloor.png")
F5wall = pg.image.load("sprites\\evilwalls.png")
Gameoverfont = pg.font.Font("sprites\\alagard.ttf", 100)
Gameovertext = Gameoverfont.render("GAME OVER", True, "red")
creditsscreen = pg.image.load("sprites\\credits.png")
alertgraphic = pg.transform.scale(pg.image.load("sprites\\alertgraphic.jpg"), (150,100))

#animation sprites
gidle = [pg.image.load(img) for img in glob.glob("Gunner\\*.png")]
widle = [pg.image.load(img) for img in glob.glob("warriordle\\*.png")]
midle = [pg.image.load(img) for img in glob.glob("mageidle\\*.png")]
thefade = fade((width, height))
gshoot = [pg.image.load(img) for img in glob.glob("gunner shoot\\*.png")]
wswing = [pg.image.load(img) for img in glob.glob("warriorswing\\*.png")]
bossimages = [pg.image.load(img) for img in glob.glob("sprites\\boss\\*.png")]


#sounds
mm_theme = pg.mixer.Sound("sprites\\menutheme.ogg")
mm_theme.set_volume(0.2)
first_floor_theme = pg.mixer.Sound("sprites\\foresttheme.ogg")
first_floor_theme.set_volume(0.3)
second_floor_theme = pg.mixer.Sound("sprites\\templetheme.ogg")
third_floor_theme = pg.mixer.Sound("sprites\\brinecave.ogg")
fourth_floor_theme = pg.mixer.Sound("sprites\\sky tower.ogg")
fifth_floor_theme = pg.mixer.Sound("sprites\\BABABA.ogg")
channel1 = pg.mixer.Channel(0)
channel1busy = False
chargesound = pg.mixer.Sound("sounds\\chargeup.ogg")
wewob = pg.mixer.Sound("sounds\\wewob.wav")
wewob.set_volume(0.8)
warpsound = pg.mixer.Sound("sounds\\warp.wav")
warpsound.set_volume(0.7)
MEGAtheme = pg.mixer.Sound("sounds\\dusknoir theme.ogg")
BOSStheme = pg.mixer.Sound("sounds\\RIPcarson.ogg")
BOSStheme.set_volume(0.8)
gameoverTheme = pg.mixer.Sound("sounds\\dontgiveup.wav")
creditstheme = pg.mixer.Sound("sounds\\congrat.wav")
creditstheme.set_volume(0.7)
alert = pg.mixer.Sound("sounds\\spotted.ogg")


#set up classes
knightbutt = idle_anims((260,250), (width/4-15,height/2 + 50), 1, widle)
gunnerbutt = idle_anims((240,240), (width/2 + 15,height/2 + 55), 1, gidle)
magebutt = idle_anims((250,265), (3*width/4+20, height/2 +51), 1, midle)
titleanim = titlebob(title)
chargeiconTEST= chargeicon()


#set up sprite groups
wGroup=pg.sprite.Group()   #WALLS
zGroup=pg.sprite.Group()   #GHOSTS
bGroup=pg.sprite.Group()   #PLAYER BULLETS
fGroup = pg.sprite.Group() #FLOOR
pGroup = pg.sprite.Group() #PLAYER
eGroup = pg.sprite.Group() #ENEMY BULLETS
hGroup = pg.sprite.Group() #HEALTH TILES
tGroup = pg.sprite.Group() #TURRETS
MEGAGroup = pg.sprite.Group()  #GHOST BOSS
portalGroup = pg.sprite.Group()   #PORTAL
mageGroup = pg.sprite.Group()   #MAGECHARGE UP ICON
BoomGroup = pg.sprite.Group()   #EXPLOSIONS??
ProgressGroup = pg.sprite.Group()   #WALLS THAT DISSAPEAR
BossGroup = pg.sprite.Group()  #DA BOSS

#variables
game_state = "menu"     #The entire game revolves around this variable
char = "bazinga"       #this gets reassigned dont worry
has_selected = False
fading = True
reload = True
rNum= 10
progress = 0
eventhandle = [False, False, False, False, False, False, False, False]
eventhandle2 = [False, False, False, False]
mageHasShot = False
keycounter = [0,0,0,0,0,0,0,0]
n = 0
hasadd = False
RevengeanceMode = False     #dont mind this...

#button classes
startbutt = Button(image = buttimg, colour = BLACK , pos = ((width/2),(height/2 + 50)), size = (294,120), text_inp= 'START', font = alagard)
exitbutt = Button(image =buttimg, colour= BLACK, pos = ((width/2),(height/2+200)), size = (294,120), text_inp= 'EXIT', font = alagard)
selecbutt = Button(image =buttimg, colour= BLACK, pos = ((width/2),(height/2-200)), size = (1000,200),
text_inp= 'SELECT YOUR CHARACTER', font = alagard)

#main menu function ----------------------------------------------------------------------------------------------------------------------
def main_menu():
    global game_state
    global thefade, BOSStheme, MEGAtheme, Gameovertext, gameoverTheme, RevengeanceMode
    mouse_pos = pg.mouse.get_pos()
    def update_screen(screen):
        screen.blit(bg, (0,0))
        startbutt.update(screen)
        exitbutt.update(screen)
        titleanim.update(screen)
        clock.tick(30)
    update_screen(screen)
    thefade.fadein(screen, 10)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if exitbutt.check_clicked(mouse_pos) == True:
                pg.quit()
            if startbutt.check_clicked(mouse_pos) ==True:
                game_state = "fading1"      #moves to the next stage of the game if the startbutton is clicked

        #seriously dont mind this nothing to see here...
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                keycounter[0]+= 1
            if keycounter[0] >=2:
                if event.key == pg.K_DOWN:
                    keycounter[1] +=1
            if keycounter[1] >= 2:
                if event.key == pg.K_LEFT:
                    keycounter[2]+=1
            if keycounter[2] >= 1:
                if event.key == pg.K_RIGHT:
                    keycounter[3]+=1
            if keycounter[3] >= 1:
                if event.key == pg.K_LEFT:
                    keycounter[4]+=1
            if keycounter[4]>=1:
                if event.key == pg.K_RIGHT:
                    keycounter[5]+=1
            if keycounter[5] >= 1:
                if event.key == pg.K_b:
                    keycounter[6]+=1
            if keycounter[6]>=1:
                if event.key == pg.K_a:
                    keycounter[7] += 1
            if keycounter[7] == 1:
                #really dont mind this...
                print("Your Dreams Disappear...")
                print("REVENGEANCE MODE ACTIVATED, GOOD LUCK...")
                BOSStheme = pg.mixer.Sound("sounds\\ITHASTOBETHISWAY.wav")
                BOSStheme.set_volume(0.5)
                MEGAtheme = pg.mixer.Sound("sounds\\Guitarsolo.wav")
                MEGAtheme.set_volume(0.5)
                Gameovertext = pg.image.load("sprites\\gameover.jpg")
                gameoverTheme = pg.mixer.Sound("sounds\\SNAKE.ogg")
                pg.display.set_caption("Pearl Quest Rising: Revengeance")
                RevengeanceMode = True
                alert.play()


#GAMEOVER SCREEN
#pretty simple game over screen
def GAMEOVER():
    global channel1busy
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
    screen.fill('black')
    GameovertextRECT = Gameovertext.get_rect()
    GameovertextRECT.center = (width/2, height/2)
    screen.blit(Gameovertext, GameovertextRECT)
    if channel1busy == False:       #these code blocks that use channel1busy repeats audio when its finished inside of a while loop
        channel1.play(gameoverTheme)
        channel1busy = True
    if channel1.get_busy() == False:
        channel1busy = False
        
#character selection screen
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
    #assigns the char variable to be the character of choice, then just goes to the next game state
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

    
        #seriously dont mind this nothing to see here...
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                keycounter[0]+= 1
            if keycounter[0] >=2:
                if event.key == pg.K_DOWN:
                    keycounter[1] +=1
            if keycounter[1] >= 2:
                if event.key == pg.K_LEFT:
                    keycounter[2]+=1
            if keycounter[2] >= 1:
                if event.key == pg.K_RIGHT:
                    keycounter[3]+=1
            if keycounter[3] >= 1:
                if event.key == pg.K_LEFT:
                    keycounter[4]+=1
            if keycounter[4]>=1:
                if event.key == pg.K_RIGHT:
                    keycounter[5]+=1
            if keycounter[5] >= 1:
                if event.key == pg.K_b:
                    keycounter[6]+=1
            if keycounter[6]>=1:
                if event.key == pg.K_a:
                    keycounter[7] += 1
            if keycounter[7] == 1:
                #really dont mind this...
                print("Your Dreams Disappear...")
                print("REVENGEANCE MODE ACTIVATED, GOOD LUCK...")
                BOSStheme = pg.mixer.Sound("sounds\\ITHASTOBETHISWAY.wav")
                BOSStheme.set_volume(0.5)
                MEGAtheme = pg.mixer.Sound("sounds\\Guitarsolo.wav")
                MEGAtheme.set_volume(0.5)
                Gameovertext = pg.image.load("sprites\\gameover.jpg")
                gameoverTheme = pg.mixer.Sound("sounds\\SNAKE.ogg")
                pg.display.set_caption("Pearl Quest Rising: Revengeance")
                RevengeanceMode = True
                alert.play()



#creates the player class based on what character was chosen
def selectedchar(char): 
    if char == "gunner":
        theplayer = Gunner(gidle, 1,1,wGroup, screen, (72,72), gshoot, eGroup, hGroup, zGroup, MEGAGroup, ProgressGroup, RevengeanceMode)
        return(theplayer)
    elif char == "mage":
        theplayer = Mage(midle, 1,1, wGroup, screen, (70, 72), midle, eGroup, hGroup, zGroup, MEGAGroup, ProgressGroup, RevengeanceMode)
        return(theplayer)
    elif char == "knight":
        theplayer = Knight(widle, 1,1,wGroup, screen, (72,70), wswing, eGroup, hGroup, zGroup, MEGAGroup, ProgressGroup, RevengeanceMode)
        return(theplayer)



#floor maker --------------------------------------------------------------------------------------------------------------------
#clears all sprites on the floor
def ClearFloor():
    wGroup.empty()
    zGroup.empty()
    bGroup.empty()
    fGroup.empty()
    tGroup.empty()
    hGroup.empty()
    eGroup.empty()
    MEGAGroup.empty()
    portalGroup.empty()
    eventhandle2 = [False, False, False, False]
    BossGroup.empty()

#iterates through the map lists and adds sprites to their respective groups
def LoadFloor(mapID, tiles, walls):
    px=0
    py=0
    zx=0
    zy=0
    rowNum=-1
    for row in mapID:
        rowNum+=1       #iterates through columns and rows
        coloumbNum=-1
        for coloumb in row:
            coloumbNum+=1
            if coloumb=='w':
                wGroup.add(obstacle(walls,coloumbNum*72,rowNum*72))     #add the obejct to the group, all these things are inits for the classes
            elif coloumb=='p':                                           #see levels.py for excatly what the strings spawn
                px=coloumbNum*72
                py=rowNum*72
            elif coloumb=='z':
                zGroup.add(troop(pg.transform.scale(ghosts[random.randint(0,5)], (45,75)), coloumbNum*72, rowNum*72, 400, bGroup, screen, char))
            elif coloumb=='1':
                tGroup.add(turret(coloumbNum*72,rowNum*72,'left'))
            elif coloumb=='2':
                tGroup.add(turret(coloumbNum*72,rowNum*72,'right'))
            elif coloumb=='3':
                tGroup.add(turret(coloumbNum*72,rowNum*72,'up'))
            elif coloumb=='4':
                tGroup.add(turret(coloumbNum*72,rowNum*72,'down'))
            elif coloumb=='x':
                hGroup.add(healthTile(coloumbNum*72,rowNum*72,'hurt'))
            elif coloumb=='h':
                hGroup.add(healthTile(coloumbNum*72,rowNum*72,'heal'))
            elif coloumb == "e":
                portalGroup.add(exitportal(coloumbNum*72, rowNum*72))
            elif coloumb == "M":
                MEGAGroup.add(megatroop(coloumbNum*72, rowNum*72, 600, bGroup, screen, char))
            elif coloumb == "B":
                ProgressGroup.add(ProgressObstacle(walls, coloumbNum*72, rowNum*72))
            elif coloumb == "F":
                Boss=boss(coloumbNum*72,rowNum*72, bossimages,bGroup, char)
                BossGroup.add(Boss)
            fGroup.add(FloorTile(tiles, coloumbNum*72, rowNum*72))
    return(px,py)

#the gameplay loop for the floor
def floor(floornum, length, tiles, walls, floorIDs):        #takes the floor ID of the floor from floors as an argument
    global game_state, rNum, reload, n, eventhandle, mageHasShot, hasadd, Boss, channel1busy, RevengeanceMode
    
    #if your hp reaches 0, you die!
    if theplayer.hp <= 0:
        game_state = "gameover"
        channel1busy = False
        channel1.stop()
        ClearFloor()
    
    #if you exit the game, the game exits!
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    #handle individual levels on the floor
    FloorID = floorIDs  
    keys = pg.key.get_pressed()
    floornum = floornum
    #eventhandle represents a list of falses, and switches to true when you enter a level
    if eventhandle[0] == False:
        theplayer.x, theplayer.y = LoadFloor(FloorID[0], tiles, walls)   
        eventhandle[0] = True
    if eventhandle[1]:
        ClearFloor()
        n +=1
        theplayer.x, theplayer.y = LoadFloor(FloorID[n],tiles, walls)
        eventhandle[1] = False
    if eventhandle[2]:
        ClearFloor()
        n +=1
        theplayer.x, theplayer.y = LoadFloor(FloorID[n],tiles, walls)
        eventhandle[2] = False
    if eventhandle[3]:
        ClearFloor()
        n +=1
        theplayer.x, theplayer.y = LoadFloor(FloorID[n],tiles, walls)
        eventhandle[3] = False
    if eventhandle[4]:
        ClearFloor()
        n +=1
        theplayer.x, theplayer.y = LoadFloor(FloorID[n],tiles, walls)
        eventhandle[4] = False
    if theplayer.x > width:
        eventhandle[n+1] = True     #when you move to the next level, it sets the next event handle to be true, which then clears the floor and spawns the next one

    #draw and update all the sprites
    screen.fill(WHITE)
    fGroup.draw(screen) 
    zGroup.draw(screen)
    zGroup.update(theplayer.x,theplayer.y, BoomGroup)
    MEGAGroup.draw(screen)
    wGroup.draw(screen)
    bGroup.draw(screen)
    hGroup.draw(screen)
    BossGroup.draw(screen)
    portalGroup.draw(screen)
    MEGAGroup.update(theplayer.x, theplayer.y, BoomGroup, screen)

    #the sprite groups return true if they contain sprites, so this removes all progress barrier blocks when all ghosts are gone
    if not zGroup and not MEGAGroup:
        if ProgressGroup:
            wewob.play()
        ProgressGroup.empty()
    else:
        ProgressGroup.draw(screen)

    #if there is a boss, run the boss fight code
    if BossGroup:
        bossFight(BossGroup.sprites()[0], eGroup)
        BossGroup.update(screen, BoomGroup)
        #if the boss gets killed, you win!!
        if not BossGroup:
            channel1busy = False
            channel1.fadeout(400)
            game_state = "credits"

    #archer cooldown 
    for turret in tGroup:
        if turret.cd==False:
            eGroup.add(turret.shoot())
            turret.cdstate=True
            turret.cd=120
        else:
            turret.cd-=1         
            if turret.cd==0:
                turret.cdstate=False
    tGroup.draw(screen)

    #draw enemy bullets
    eGroup.draw(screen)
    eGroup.update()

    #player attacks --------------

    
    if keys[pg.K_SPACE] :
        theplayer.charge()
        mageHasShot = True
        if reload == False:
            theplayer.shooting()
            #non mage characters just attack
            if char != "mage":
                bGroup.add(theplayer.attack())
            rNum= theplayer.rNum
            reload=True
        #mage charges up their spell
        if char == "mage":
            if hasadd == False:
                mageGroup.add(chargeicon())
                hasadd = True
            mageGroup.update(theplayer.chargeNum, (theplayer.x, theplayer.y))
            mageGroup.draw(screen)
            
    
    if reload:      #reloading is the system that prevents you from infinitely spamming as knight and gunner, the mage does not use this system
        rNum-=1
        if rNum==0:  
            reload=False

    if char == "mage":      #this spawns a fireball at the end of a cast
        if mageHasShot:
            if not keys[pg.K_SPACE]:
                bGroup.add(theplayer.FIREattack())
                theplayer.fireballsound.play()
                theplayer.chargeNum = 10
                hasadd = False
                mageHasShot = False
                for sprite in mageGroup:
                    sprite.kill()
                    sprite.channelchannel.stop()

    #player projectiles
    bGroup.update(rNum, theplayer.x, theplayer.y, theplayer.direction, theplayer.vec.x)
    pGroup.update()
    pGroup.draw(screen)
    BoomGroup.update()
    BoomGroup.draw(screen)

    #detect if the player enters the portal
    if len(portalGroup.sprites())>0 and pg.sprite.collide_rect(pGroup.sprites()[0], portalGroup.sprites()[0]):
        ClearFloor()
        eventhandle = [False, False, False, False, False, False, False, False]
        n=0
        warpsound.play()
        game_state = "transition"
    
    #99.99 ALERT
    if RevengeanceMode:
        screen.blit(alertgraphic, (800,20))

    
    
    
        


    
#MAIN GAME LOOP --------------------------------------------------------------------------------------------------------------------

while True:
    #handles the background music
    if MEGAGroup:
        if not eventhandle2[1]:
            channel1busy = False
            eventhandle2[1] = True
        if channel1busy == False:
            channel1.play(MEGAtheme)
            channel1busy = True
        if channel1.get_busy() == False:
            channel1busy = False
            eventhandle2[1] = False
    if BossGroup:
        if not eventhandle2[2]:
            channel1busy = False
            eventhandle2[2] = True
        if channel1busy == False:
            channel1.play(BOSStheme)
            channel1busy = True
        if channel1.get_busy() == False:
            channel1busy = False

    if game_state == "menu" or game_state == "char_selec":
        if channel1busy == False:
            channel1.play(mm_theme)
            channel1busy = True
        if channel1.get_busy() == False:
            channel1busy = False
    
    if game_state == "1F" or game_state == "1F load" or game_state == "1F fade":
        if channel1busy == False:
            channel1.play(first_floor_theme)
            channel1busy = True
        if not channel1.get_busy():
            channel1busy = False
    if game_state == "2F" or game_state == "2F load" or game_state =="2F fade":
        if channel1busy == False:
            channel1.play(second_floor_theme)
            channel1busy = True
        if not channel1.get_busy():
            channel1busy = False
    if game_state == "3F" or game_state == "3F load" or game_state =="3F fade":
        if channel1busy == False:
            channel1.play(third_floor_theme)
            channel1busy = True
        if not channel1.get_busy():
            channel1busy = False
    if game_state == "4F" or game_state == "4F load" or game_state =="4F fade":
        if channel1busy == False:
            channel1.play(fourth_floor_theme)
            channel1busy = True
        if not channel1.get_busy():
            channel1busy = False
    if game_state == "5F" or game_state == "5F load" or game_state =="5F fade":
        if channel1busy == False:
            channel1.play(fifth_floor_theme)
            channel1busy = True
        if not channel1.get_busy():
            channel1busy = False


    #main menu
    if game_state == "menu":
        main_menu()
        pg.display.flip()
    #fade 1
    elif game_state == "fading1":
        if thefade.isdone != True:
            main_menu()
            thefade.fadein(screen,10)
            thefade.fadept1()
            pg.display.flip()
        else:
            game_state = "char_selec"
    
    #character select
    elif game_state == "char_selec":
        charaselect()
        thefade.fadeout(screen, 10)
        pg.display.update()
        clock.tick(30)
    #fade 2
    elif game_state == "fade2":
        if has_selected == False:
            thefade.reset((width, height))
            theplayer = selectedchar(char)
            pGroup.add(theplayer)
            has_selected = True

        if thefade.isdone != True:
            charaselect()
            thefade.fadein(screen, 10)
            thefade.fadept1()
            pg.display.flip()
        else:
            channel1.fadeout(1000)
            game_state = "1F load"
        clock.tick(60)
            
    #load first level
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
        thefade.fadeout(screen, 10)
        clock.tick(30)
        pg.display.flip()
    #fade 3
    elif game_state == "1F fade":
        if thefade.isdone != True:
            screen.blit(bg1, (0,0))
            thefade.fadein(screen, 10)
            thefade.fadept1()
            pg.display.flip()
            clock.tick(30)
        else:
            game_state = "1F"
    #level 1
    elif game_state == "1F":
        floor(1, 5, F1tile, F1wall, Floor1ID)
        thefade.fadeout(screen, 10)
        clock.tick(60)
        pg.display.flip()

    #transitional state (determines what level will be next)
    elif game_state == "transition":
        if progress == 0:
            channel1.fadeout(200)
            thefade.reset((width, height))
            game_state = "2F trans"
        if progress == 1:
            channel1.fadeout(200)
            thefade.reset((width, height))
            game_state = "3F trans"
        if progress == 2:
            channel1.fadeout(200)
            thefade.reset((width, height))
            game_state = "4F trans"
        if progress == 3:
            channel1.fadeout(200)
            thefade.reset((width, height))
            game_state = "5F trans"
        if progress == 4:
            channel1.fadeout(200)
            game_state = "credits" 
    #transition to floor 2
    elif game_state == "2F trans":
        if thefade.isdone != True:
            screen.blit(screeneffect, (0,0))
            thefade.fadein(screen, 4)
            thefade.fadept1()
            clock.tick(30)
            pg.display.flip()
        else:
            progress = 1
            game_state = "2F load"

    #more transition to floor 2
    elif game_state == "2F load":
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    thefade.reset((width, height))
                    game_state = "2F fade"
        screen.blit(bg2, (0,0))
        screen.blit(alagardSMOL.render("Press Space To Start", True, WHITE), (20,650))
        thefade.fadeout(screen, 10)
        clock.tick(30)
        pg.display.flip()

    #more transition to floor 2
    elif game_state == "2F fade":
        if thefade.isdone != True:
            screen.blit(bg2, (0,0))
            thefade.fadein(screen,10)
            thefade.fadept1()
            pg.display.flip()
        else:
            game_state = "2F"
    #floor 2
    elif game_state == "2F":
        floor(2, 5,F2tile, F2wall, Floor2ID)
        thefade.fadeout(screen, 10)
        clock.tick(60)
        pg.display.flip()

    #transition to floor 3
    elif game_state == "3F trans":
        if thefade.isdone != True:
            screen.blit(screeneffect, (0,0))
            thefade.fadein(screen,4)
            thefade.fadept1()
            clock.tick(30)
            pg.display.flip()
        else:
            progress = 2
            game_state = "3F load"

    #transition to floor 3
    elif game_state == "3F load":
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    thefade.reset((width, height))
                    game_state = "3F fade"
        screen.blit(bg3, (0,0))
        screen.blit(alagardSMOL.render("Press Space To Start", True, WHITE), (20,650))
        thefade.fadeout(screen, 10)
        clock.tick(30)
        pg.display.flip()

    #transition to floor 3
    elif game_state == "3F fade":
        if thefade.isdone != True:
            screen.blit(bg3, (0,0))
            thefade.fadein(screen,10)
            thefade.fadept1()
            pg.display.flip()
        else:
            game_state = "3F"
    #floor 3
    elif game_state == "3F":
        floor(3, 5, F3tile, F3wall, Floor3ID)
        thefade.fadeout(screen,10)
        clock.tick(60)
        pg.display.flip()

    #transition to floor 4
    elif game_state == "4F trans":
        if thefade.isdone != True:
            screen.blit(screeneffect, (0,0))
            thefade.fadein(screen,4)
            thefade.fadept1()
            clock.tick(30)
            pg.display.flip()
        else:
            progress = 3
            game_state = "4F load"

    #transition to floor 4
    elif game_state == "4F load":
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    thefade.reset((width, height))
                    game_state = "4F fade"
        screen.blit(bg4, (0,0))
        screen.blit(alagardSMOL.render("Press Space To Start", True, WHITE), (20,650))
        thefade.fadeout(screen,10)
        clock.tick(30)
        pg.display.flip()

    #transition to floor 4
    elif game_state == "4F fade":
        if thefade.isdone != True:
            screen.blit(bg4, (0,0))
            thefade.fadein(screen,10)
            thefade.fadept1()
            pg.display.flip()
        else:
            game_state = "4F"

    #floor 4
    elif game_state == "4F":
        floor(3, 5, F4tile, F4wall, Floor4ID)
        thefade.fadeout(screen,10)
        clock.tick(60)
        pg.display.flip()

    #transition to floor 5
    elif game_state == "5F trans":
        if thefade.isdone != True:
            screen.blit(screeneffect, (0,0))
            thefade.fadein(screen,4)
            thefade.fadept1()
            clock.tick(30)
            pg.display.flip()
        else:
            progress = 4
            game_state = "5F load"

    #transition to floor 5
    if game_state == "5F load":
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    thefade.reset((width, height))
                    game_state = "5F fade"
        screen.blit(bg5, (0,0))
        screen.blit(alagardSMOL.render("Press Space To Start", True, WHITE), (20,650))
        thefade.fadeout(screen,10)
        clock.tick(30)
        pg.display.flip()

    #transition to floor 5
    elif game_state == "5F fade":
        if thefade.isdone != True:
            screen.blit(bg5, (0,0))
            thefade.fadein(screen,10)
            thefade.fadept1()
            pg.display.flip()
        else:
            game_state = "5F"
    
    #floor 5
    elif game_state == "5F":
        floor(4, 5, F5tile, F5wall, Floor5ID)
        thefade.fadeout(screen,10)
        clock.tick(60)
        pg.display.flip()
        
    #gameover
    elif game_state == "gameover":
        GAMEOVER()
        clock.tick(60)
        pg.display.flip()

    elif game_state == "credits":
        screen.blit(creditsscreen, (0,0))
        clock.tick(60)
        pg.display.flip()
        thefade.fadeout(screen, 40)

        if channel1busy == False:
            channel1.play(creditstheme)
            channel1busy = True
        if not channel1.get_busy():
            channel1busy = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
