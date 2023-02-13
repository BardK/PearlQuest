import pygame as pg
class Button:
    def __init__(self, image, colour, pos, size, text_inp, font):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.image = pg.transform.scale(image, size)
        self.colour = colour
        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))
        self.text = font.render(text_inp, True, self.colour)
        self.text_rect = self.text.get_rect(center = (self.x_pos, self.y_pos))
        
    #updates screen with button (obviously)
    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
    
    #checks if its clicked
    def check_clicked(self, mousepos):
        if mousepos[0] in range (self.rect.left, self.rect.right) and mousepos[1] in range (self.rect.top, self.rect.bottom):
            return True
        else:
            return False

#fade class 
class fade():
    def __init__(self, size):
        self.image = pg.Surface(size)
        self.image.fill((0,0,0))
        self.image.set_alpha(0)
        self.op = 0
        self.isfade = False
        self.isdone = False
        self.fadeoutdone = False

    def fadept1(self):
        self.isfade = True

    #fades the screen TO black
    def fadein(self, screen, speed):
        if self.op <= 300 and self.isfade == True:
            self.image.set_alpha(self.op)
            screen.blit(self.image, (0,0))
            self.op += speed
        elif self.op > 300 and self.isfade == True:
            screen.blit(self.image, (0,0))
            self.isdone = True

    #fades the screen OUT OF black
    def fadeout(self, screen, speed):
        self.isfade = False
        if self.op >= 0:
            self.image.set_alpha(self.op)
            self.op -= speed
        elif self.op <=1:
            self.op = 0  
            self.image.set_alpha(self.op)
            self.fadeoutdone = True
        screen.blit(self.image, (0,0))
    
    #resets attributes for repeated use
    def reset(self, size):
        self.image = pg.Surface(size)
        self.image.fill((0,0,0))
        self.image.set_alpha(0)
        self.op = 0
        self.isfade = False
        self.isdone = False

