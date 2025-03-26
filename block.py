import pygame as pg

class Block():
    def __init__(self,x,y,Block_map,process_name):
        pg.sprite.Sprite.__init__(self)
        self.image = Block_map
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.move_dir_x = 0
        self.move_dir_y = 0
        self.process = process_name
    def update(self):
        x,y = self.rect.center
        x+= self.move_dir_x
        y+= self.move_dir_y
        self.rect.center = (x,y)
    def draw(self, surface):
        surface.blit(self.image, self.rect)