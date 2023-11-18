import pygame
import sys
import math
import time

import random

pygame.init()


### Initital Constants ###

# Movement settings
fd_fric = 0.5
bd_fric = 0.1
player_max_speed = 10
player_max_rtspeed = 10

# Screen settings
display_width  = 800
display_height = 600
screen = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

# Farger
white = (255, 255, 255)
yellow = (231, 245, 39)


class Player():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.hspeed = 0
        self.vspeed = 0
        self.rtspeed = 0
        self.size = 15
        self.dir = -90
        self.thrust = False
    
    
    def updatePlayer(self):
        speed = speed = math.sqrt(self.hspeed**2 + self.vspeed**2)
        if self.thrust == True:
            if speed < player_max_speed:
                self.hspeed += fd_fric * math.cos(self.dir * math.pi / 180)
                self.vspeed += fd_fric * math.sin(self.dir * math.pi / 180)
                
               
            else:
                player_max_speed * math.cos(self.dir * math.pi / 180)
        else:
            if speed - bd_fric > 0:
                chg_hspeed = (bd_fric * math.cos(self.vspeed / self.hspeed))
                chg_vspeed = (bd_fric * math.sin(self.vspeed / self.hspeed))
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

        
        # Forhindrer warp:
        if self.y < 0:
            self.y = display_height
        elif self.y > display_height:
            self.y = 0
        elif self.x < 0:
            self.x = display_width
        elif self.x > display_width:
            self.x = 0
        
        # Oppdaterer posisjon of rotasjon
        self.x += self.hspeed
        self.y += self.vspeed
        self.dir += self.rtspeed
         

    def drawPlayer(self):
        angle = math.radians(self.dir)
        size = self.size
        x = self.x
        y = self.y

        '''
            Forklaring:
            math.cos = horisontal
            math.sin = vertikal
        '''



        # Tegner romskipet:
        # Venstre del
        pygame.draw.line(screen, white,
                         # Startpunkt
                         (x - (size * math.sqrt(130) / 12) * math.cos(math.atan(7 / 9) + angle),
                          y - (size * math.sqrt(130) / 12) * math.sin(math.atan(7 / 9) + angle)),
                          # Sluttpunkt
                         (x + size * math.cos(angle), y + size * math.sin(angle)))
        # Høyre del
        pygame.draw.line(screen, white,
                         (x - (size * math.sqrt(130) / 12) * math.cos(math.atan(7 / 9) - angle),
                          y + (size * math.sqrt(130) / 12) * math.sin(math.atan(7 / 9) - angle)),
                         (x + size * math.cos(angle), y + size * math.sin(angle)))
        # Nederste del av romskipet
        pygame.draw.line(screen, white,
                         (x - (size * math.sqrt(2) / 2) * math.cos(angle + math.pi / 4),
                          y - (size * math.sqrt(2) / 2) * math.sin(angle + math.pi / 4)),
                         (x - (size * math.sqrt(2) / 2) * math.cos(-angle + math.pi / 4),
                          y + (size * math.sqrt(2) / 2) * math.sin(-angle + math.pi / 4)))
        if self.thrust:
            print("Thrust")

            # Venstre strek
            pygame.draw.line(screen, yellow,     
                             # Startpunkt (X, Y)
                             (x - size * math.cos(angle), y - size * math.sin(angle)),
                             # Sluttpunkt (X, Y)
                             (x - (size * math.sqrt(5) / 4) * math.cos(angle + math.pi / 6),
                              y - (size * math.sqrt(5) / 4) * math.sin(angle + math.pi / 6)))
            
            # Høyre strek
            pygame.draw.line(screen, yellow,
                             # Startpunkt (X, Y)
                             (x - size * math.cos(angle), y + size * math.sin(-angle)),
                             # Sluttpunkt (X, Y)
                             (x - (size * math.sqrt(5) / 4) * math.cos(-angle + math.pi / 6),
                              y + (size * math.sqrt(5) / 4) * math.sin(-angle + math.pi / 6)))
            
        
        
class Bullet():
    def __init__(self, x, y, dir) -> None:
        self.x = x
        self.y = y
        self.dir = dir
        self.size = 1
        self.speed = 15
        self.life = 55
    

    def update_bullet(self):
        
        self.x += self.speed * math.cos(self.dir * math.pi / 180)
        self.y += self.speed * math.sin(self.dir * math.pi / 180)
        
        pygame.draw.circle(screen, white, (int(self.x), int(self.y)), self.size)
        
        self.life -= 1




class Asteroid():
        full_circle = random.uniform(18, 36)
        dist = random.uniform(self.size / 2, self.size)
        self.vertices = []
        while full_circle < 360:
            self.vertices.append([dist, full_circle])
            dist = random.uniform(self.size / 2, self.size)
            full_circle += random.uniform(18, 36)



def gameloop():
    # Initial variables
    player = Player(display_width // 2, display_height // 2)
    bullets = []
    

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.thrust = True
                if event.key == pygame.K_LEFT:
                    player.rtspeed = -player_max_rtspeed
                if event.key == pygame.K_RIGHT:
                    player.rtspeed = player_max_rtspeed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.thrust = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    player.rtspeed = 0
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player.x, player.y, player.dir))


        screen.fill((0, 0, 0))
        
        player.updatePlayer()
        if len(bullets) > 0:
            for bullet in bullets:
                bullet.update_bullet()
                if bullet.life == 0:
                    bullets.remove(bullet)
                
        
        
        
        player.drawPlayer()
               
        pygame.display.flip()
        clock.tick(30)
        
gameloop()

pygame.quit()
sys.exit()
