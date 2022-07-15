import pygame
import conf
from pamp import Pamp

class Porta(pygame.sprite.Sprite):
    def __init__(self, temps_inici,pam):
        super().__init__()
        self.image = pygame.image.load('porta.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = conf.amplada_pantalla
        self.velh = 18
        self.rect.top = 75
        self.t_inici = temps_inici
        self.pam = pam

    def collide(self):
        hits=pygame.sprite.collide_mask(self, self.pam)
        x=0
        if hits!=None:
            x+=1
            if x>=1:
                self.pam.end=True
        elif hits!=None and self.pam.vel[1]>0:
            self.pam.on_obstacle=True
        else:
            self.pam.collided=False
           
    def update(self):
        self.collide()
        if pygame.time.get_ticks()- self.t_inici>60000:
            self.rect.right = self.rect.right - self.velh
