import random
import math
import pygame
from library.utils import *

#SCREEN = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))


class Player():
    '''Creates an controls the player.
    
    Has a function for creating the player en a function for drawing the player
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 10
        self.hspeed = 0
        self.vspeed = 0
        self.rtspeed = 0
        self.dir = -90
        self.thrust = False
        self.score = 0
        self.lives = 3
        self.bullets = []
        self.player_pieces = []
        self.extra_lives_multiplier = 1

        self.blink = 0
        self.invisible_dur = 0
        self.spawn_dur = 0
        self.state = "alive"
        self.hyperspace = 0
        

    def updatePlayer(self):        
        '''Updates the position, rotation and speed of the player object'''
        speed = math.sqrt(self.hspeed**2 + self.vspeed**2)
        if self.thrust == True:
            if speed < PLAYER_MAX_SPEED:
                self.hspeed += FD_FRIC * math.cos(self.dir * math.pi / 180)
                self.vspeed += FD_FRIC * math.sin(self.dir * math.pi / 180)
            else:
                # BUG: Styringen endrer seg når skipet kommer i topphastiget.
                self.hspeed = PLAYER_MAX_SPEED * math.cos(self.dir * math.pi / 180)
                self.vspeed = PLAYER_MAX_SPEED * math.sin(self.dir * math.pi / 180)
        else:
            if speed - BD_FRIC > 0:
                chg_hspeed = (BD_FRIC * math.cos(self.vspeed / self.hspeed))
                chg_vspeed = (BD_FRIC * math.sin(self.vspeed / self.hspeed))
                if self.hspeed != 0:
                    if chg_hspeed / abs(chg_hspeed) == self.hspeed / abs(self.hspeed):
                        self.hspeed -= chg_hspeed
                    else:
                        self.hspeed += chg_hspeed
                if self.vspeed != 0:
                    if chg_vspeed / abs(chg_vspeed) == self.vspeed / abs(self.vspeed):
                        self.vspeed -= chg_vspeed
                    else:
                        self.vspeed += chg_vspeed
            else:
                self.hspeed = 0
                self.vspeed = 0

        
        # Warp-effekt:
        self.x, self.y = check_warp(self.x, self.y)

        
        # Oppdaterer posisjon og rotasjon
        self.x += self.hspeed
        self.y += self.vspeed
        self.dir += self.rtspeed


    def drawPlayer(self):
        '''Draws the player on the screen'''
        angle = math.radians(self.dir)
        size = self.size
        x = self.x
        y = self.y

        # Tegner romskipet:
        # Venstre strek.
        pygame.draw.line(SCREEN, WHITE,
                         # Øverste punktet på streken.
                         # Forklaring: x/y-koordinat * størrelse * vinkelen. 
                         # Lager et nytt punkt basert på størrelse og vinkel
                         (x + size * math.cos(angle), 
                          y + size * math.sin(angle)),
                         # Nederste punktet på streken.
                         # Forklaring: En konstat vinkel + justert vinkel * konstant størrelse - x/y-koordinat
                         (x - (size * math.sqrt(130) / 12) * math.cos(math.atan(7 / 9) + angle),
                          y - (size * math.sqrt(130) / 12) * math.sin(math.atan(7 / 9) + angle)))
        # Høyre strek.
        pygame.draw.line(SCREEN, WHITE,
                         # Øverste punktet på streken.
                         (x + size * math.cos(angle), 
                          y + size * math.sin(angle)),
                         # Nederste punktet på streken.
                         (x - (size * math.sqrt(130) / 12) * math.cos(math.atan(7 / 9) - angle),
                          y + (size * math.sqrt(130) / 12) * math.sin(math.atan(7 / 9) - angle)))
        # Nederste strek.
        pygame.draw.line(SCREEN, WHITE,
                         # Venstre punkt.
                         (x - (size * math.sqrt(2) / 2) * math.cos(math.pi / 4 + angle),
                          y - (size * math.sqrt(2) / 2) * math.sin(math.pi / 4 + angle)),
                         # Høyre punkt.
                         (x - (size * math.sqrt(2) / 2) * math.cos(math.pi / 4 + -angle),
                          y + (size * math.sqrt(2) / 2) * math.sin(math.pi / 4 + -angle)))
        
        # Hvis det blir gitt thrust, så tegnes det en stikkflamme.
        if self.thrust:
            # Venstre strek
            pygame.draw.line(SCREEN, YELLOW,     
                             # Startpunkt (X, Y)
                             (x - size * math.cos(angle), y - size * math.sin(angle)),
                             # Sluttpunkt (X, Y)
                             (x - (size * math.sqrt(5) / 4) * math.cos(angle + math.pi / 6),
                              y - (size * math.sqrt(5) / 4) * math.sin(angle + math.pi / 6)))
            
            # Høyre strek
            pygame.draw.line(SCREEN, YELLOW,
                             # Startpunkt (X, Y)
                             (x - size * math.cos(angle), y + size * math.sin(-angle)),
                             # Sluttpunkt (X, Y)
                             (x - (size * math.sqrt(5) / 4) * math.cos(-angle + math.pi / 6),
                              y + (size * math.sqrt(5) / 4) * math.sin(-angle + math.pi / 6)))
               

    def resetPlayer(self):
        self.x = DISPLAY_WIDTH // 2
        self.y = DISPLAY_HEIGHT // 2
        self.hspeed = 0
        self.vspeed = 0
        self.rtspeed = 0
        self.dir = -90
        self.thrust = False
         
            
class DeadPlayer():
    def __init__(self, x, y, l):
        self.x = x
        self.y = y
        self.length = l
        self.angle = random.randrange(0, 360) * math.pi / 180
        self.dir = random.randrange(0, 360) * math.pi / 180
        self.rtsp = random.uniform(-0.25, 0.25)
        self.speed = random.randint(2,8)
        self.pieces = []
        self.pieces_dur = 10
        

    def update_dead_player(self):
        pygame.draw.line(SCREEN, WHITE, 
                            (self.x + self.length * math.cos(self.angle) / 2,
                            self.y + self.length * math.sin(self.angle) / 2),
                            (self.x - self.length * math.cos(self.angle) / 2,
                            self.y - self.length * math.sin(self.angle) / 2))
        
        self.x += self.speed * math.cos(self.dir)
        self.y += self.speed * math.sin(self.dir)
        self.angle += self.rtsp

        if self.pieces_dur > 10:
            self.pieces_dur -= 1
        
