import pygame as pg

#these are just the classes for the blocks that make up the levels
class obstacle(pg.sprite.Sprite):
    def __init__(self,image,px,py):
        super().__init__()
        self.image=pg.transform.scale(image, (72,72))
        self.rect=self.image.get_rect()
        self.rect.topleft=((px,py))

class FloorTile(pg.sprite.Sprite):
    def __init__(self, image, px, py):
        super().__init__()
        self.image = pg.transform.scale(image, (72,72))
        self.rect = self.image.get_rect()
        self.rect.topleft = ((px,py))

#these blocks get killed when you defeat all the ghosts
class ProgressObstacle(pg.sprite.Sprite):
    def __init__(self,image, px,py):
        super().__init__()
        self.image=pg.transform.scale(image, (72,72))
        self.rect=self.image.get_rect()
        self.rect.topleft=((px,py))

