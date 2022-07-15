# Pygame
import pygame
from pygame.locals import *
# PGU
from pgu import engine
# Mòduls propis
import conf
from sprite_sheets import *
from toro import Toro
from scroll import Scroller
from pamp import Pamp
from porta import Porta

from barrils import Barrils
from barrils import Barril
# Classe joc
class Joc(engine.Game):
    # Initialize screen, pygame modules, clock... and states.
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode(conf.mides_pantalla, SWSURFACE)
        self.crono = pygame.time.Clock()
        self.menu = Menu(self)
        self.cred = Credits(self)
        self.play=Play(self)

    # Creates and stores all states as attributes
    def run(self): 
        super().run(self.menu, self.screen)
    # Tick is called once per frame. It shoud control de timing.
    def change_state(self, transition=None):
        """
        Implements the automat for changing the state of the game.
        Given self.state and an optional parameter indicating 
        the kind of transition, computes and returns the new state
        """
        if self.state is self.menu:
            if transition == 'CREDITS':
                new_state = self.cred
            elif transition == 'PLAY':
                self.play.init()
                new_state = self.play
            elif transition == 'EXIT':
                new_state = pgu.engine.Quit(self)
            else:
                raise ValueError('Unknown transition indicator')
        elif self.state is self.cred:
            new_state = self.menu
            self.menu.init()
        elif self.state is self.play:
            if transition == 'GAMEOVER':
                new_state = self.menu
                self.menu.init()
            elif transition == 'CREDITS':
                new_state = self.cred
            else:
                raise ValueError('Unknown transition indicator')
        else:
            raise ValueError('Unknown game state value')
        return new_state
    def tick(self):
        self.crono.tick(conf.fps)   # Limits the maximum FPS
        # print(self.crono.get_fps())
# A state may subclass engine.State.
class Menu(engine.State):
    def init(self):
        self.image = pygame.image.load("images/menu.png")
        
    
    def update(self, s):
        s.fill(conf.color_fons_menu)
        rect = self.image.get_rect()
        rect.center = s.get_rect().center
        s.blit(self.image, rect)
        pygame.display.flip()
        

    def event(self,e): 
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_c:
                return self.game.change_state('CREDITS')
            if e.key == pygame.K_RETURN:
                return self.game.change_state('PLAY')
            if e.key == pygame.K_ESCAPE:
                return self.game.change_state('EXIT')

class Credits(engine.State):
    def init(self):
        self.image = pygame.image.load("credits.png")
    
    def paint(self, s):
        s.fill(conf.color_fons_menu)
        rect = self.image.get_rect()
        rect.center = s.get_rect().center
        s.blit(self.image, rect)
        pygame.display.flip()
        
    def event(self,e): 
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                return self.game.change_state('MENU')



        
    
class Play(engine.State):
    # The init method should load data, etc.  The __init__ method
    # should do nothing but record the parameters.  If the init method
    # returns a value, it becomes the new state.
    def init(self):
        self.temps=pygame.time.get_ticks()
        grup = pygame.sprite.OrderedUpdates() # grup de Sprites ordenat
        imfons = pygame.image.load(conf.imatge_fons).convert_alpha()
        fons = Scroller(imfons, conf.amplada_pantalla)
        grup.add(fons)
        toros = pygame.image.load(conf.sprite_sheet_toro).convert_alpha()
        lims_toros = crea_llista_imatges(toros,
                                          conf.nombre_imatges_sprite_sheet_toro)
        o1 = Toro( lims_toros, (-200, 310), 850 )
        grup.add(o1)
        im = pygame.image.load(conf.sprite_sheet_pamp).convert_alpha()
        mat_im = crea_matriu_imatges(im, *conf.nombre_imatges_sprite_sheet_pamp)
        self.pl = Pamp( mat_im, (350, 395),  [0,0],o1)
        grup.add(self.pl)
        self.porta=Porta(self.temps,self.pl)
        grup.add(self.porta)
        self.barrils = Barrils(self.temps,self.pl)
        grup.add(self.barrils)
        self.all_sprites = grup
    # The paint method is called once.  If you call repaint(), it
    # will be called again.
    def paint(self,screen):
        self.update(screen)
    # Loop is called once a frame.  It should contain all the logic.
    # If the loop method returns a value it will become the new state.
    def event(self,e): 
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                 return self.game.change_state('GAMEOVER')
            elif e.key == pygame.K_RIGHT:
                self.pl.running=True
                if e.key== pygame.K_SPACE:
                    self.pl.jumping==True
            if self.pl.vel[1]==0:
                if e.key==pygame.K_SPACE:
                    self.pl.change_state(self.pl.jump)
                    if self.pl.on_obstacle==True:
                        self.pl.change_state(self.pl.jump)

        elif e.type ==pygame.KEYUP:
            if e.key == pygame.K_RIGHT:
                self.pl.running=False
                
    def loop(self):
        self.all_sprites.update()
        self.barrils.update()
        if self.pl.die==True:
            return self.game.change_state('GAMEOVER')
        if self.pl.end==True:
            return self.game.change_state('GAMEOVER')
    # Update is called once a frame.  It should update the display.
    def update(self, screen):
        self.all_sprites.draw(screen)
        self.barrils.draw(screen)
        pygame.display.flip()

# Programa principal
def main():
    game = Joc()
    game.run()
# Crida el programa principal només si s'executa el mòdul:
#   python3 main_anim.py
#
# o bé
#
#   python3 -m main_anim
#
# Importa les funcions i les classes, però no executa el programa
# principal si s'importa el mòdul:
#
 
#   import joc
if __name__ == "__main__":
    main()

