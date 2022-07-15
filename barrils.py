import pygame
import conf
import random
from pamp import Pamp

class Barrils(pygame.sprite.OrderedUpdates):
    def __init__(self, temps_inici,pam):
        super().__init__()
        self.seguent = pygame.time.get_ticks() + 1000
        self.t_inici = temps_inici
        self.pam=pam


    def update(self):
        super().update()
        if 25000 < pygame.time.get_ticks()- self.t_inici < 55000:
            if pygame.time.get_ticks() > self.seguent:
                self.add(Barril(self.pam))
                self.seguent = pygame.time.get_ticks() + random.randint(1000,2200)

        elif 0 < pygame.time.get_ticks()- self.t_inici < 25000:
            if pygame.time.get_ticks() > self.seguent:
                self.add(Barril(self.pam))
                self.seguent = pygame.time.get_ticks() + random.randint(2500,3500)
                

class Barril(pygame.sprite.Sprite):
    def __init__(self,pam):
        super().__init__()
        self.l = ['barrils.png','tanca1.png','botiga.png']
        imatge=self.l[random.randint(0,2)]
        self.image = pygame.image.load(imatge).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = conf.amplada_pantalla
        self.velh = 19
        self.pam=pam
        if imatge=='barrils.png':
            self.rect.top = 400
        elif imatge=='tanca1.png':
            self.rect.top = 420
        elif imatge=='botiga.png':
            self.rect.top = 310
        
    def collide(self,pos_ant):
        hits=pygame.sprite.collide_mask(self, self.pam)

        if hits!=None and self.pam.vel[1]>0:
            self.pam.on_obstacle=True
            self.pam.vel[1]=0
        
        elif hits!=None:
            self.pam.collided=True

        else:
            self.pam.collided=False
            self.pam.on_obstacle=False


            
    def update(self):
        pos_ant=self.pam.on_obstacle
        self.rect.right=self.rect.right-self.velh
        self.collide(pos_ant)


        if self.rect.right<0:
            self.kill()

