import pygame
from toro import Toro

class Pamp(pygame.sprite.Sprite):
    standing, running, jumping= range(3)
    stop, run,jump,coll,j=range(5)
    def __init__(self, llista_imatges, pos, vel, toro):
        super().__init__()
        self.llista_im = llista_imatges
        self.image = self.llista_im[0][0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.count=0
        self.nframes=len(self.llista_im[0])
        self.vel=vel
        self.life=1
        self.toro=toro
        self.die=False
        self.end=False
        self.collided=False
        self.on_obstacle=False
        self.standing=True
        self.running=False
        self.jumping=False

    def collide(self):
        hits=pygame.sprite.collide_mask(self, self.toro)
        if hits!=None:
            self.die=True


    def update(self):
        self.collide()
        self.count = self.count + 1
        fila=0
        if self.running==True and self.jumping==False and self.standing==True:
            fila=1
            self.rect.left=self.rect.left
            if self.rect.topleft[0]<350:
                self.rect.left=self.rect.left+6
        
        if self.count == self.nframes * 2:
            self.count = 0
        columna = self.count // 2
        self.image = self.llista_im[fila][columna]
        if self.standing==True and self.running==False:
            fila=0
            self.rect.left=self.rect.left-19
            columna=0
            self.image = self.llista_im[fila][0]

        if self.jumping==True:
            if self.on_obstacle==True:
                self.vel[1]=0
                fila=1
                if self.count == self.nframes * 2:
                    self.count = 0
                columna = self.count // 2
                self.image = self.llista_im[1][columna]
            else:
                fila=2
                columna=0
                self.rect.left=self.rect.left+self.vel[0]
                self.image = self.llista_im[fila][0]
                self.rect.top=self.rect.top+self.vel[1]
                if self.vel[1]<=20:
                    self.vel[1]=self.vel[1]+2
                else:
                    self.vel[1]=self.vel[1]
            if self.vel[1]>0 and self.rect.topleft[1]>=395:
                self.jumping=False
                self.vel[1]=0

        if self.jumping==False:
            self.vel[1]=0
        if self.collided==True:
            if self.on_obstacle==False:
                self.running=False
        
            
        if self.rect.topleft[0]<-200:
            self.die=True


    def change_state(self, transition=None):
        if transition==self.run:
            self.running=True
        elif transition==self.stop:
            self.standing=True
            self.running=False
        elif transition==self.jump:
            self.jumping=True
            self.vel[1]=-30
        elif transition==self.coll:
            self.jumping=False

        else:
            raise ValueError('Transició {} desconeguda'.format(transicio))
        if transition!=None:
            self.count=0
