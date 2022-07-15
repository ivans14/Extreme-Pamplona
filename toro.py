import pygame
class Toro(pygame.sprite.Sprite):
    def __init__(self, llista_imatges, pos, vel):
        super().__init__()
        self.llista_im = llista_imatges
        self.image = self.llista_im[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.vel = vel
    def update(self):
        t = pygame.time.get_ticks()
        ta = t % self.vel
        idx = (ta * len(self.llista_im)) // self.vel
 
        self.image = self.llista_im[idx]
