import pygame
import sys
import math
import time

pygame.init()


### Initital Constants ###

# Movement settings
fd_fric = 0.5
bd_fric = 0.1
player_max_speed = 20
player_max_rtspeed = 10

# Screen settings
display_width  = 800
display_height = 600
screen = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

# Farger
white = (255, 255, 255)


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
        a = math.radians(self.dir)
        x = self.x
        y = self.y
        s = self.size


        print((x - (s * math.sqrt(130) / 12) * math.cos(math.atan(7 / 9) + a),
                          y - (s * math.sqrt(130) / 12) * math.sin(math.atan(7 / 9) + a)),
                         (x + s * math.cos(a), y + s * math.sin(a)))

        pygame.draw.line(screen, white, (300, -200), (300, -200))

        # Tegner romskipet:
        # Venstre del
        pygame.draw.line(screen, white,
                         (x - (s * math.sqrt(130) / 12) * math.cos(math.atan(7 / 9) + a),
                          y - (s * math.sqrt(130) / 12) * math.sin(math.atan(7 / 9) + a)),
                         (x + s * math.cos(a), y + s * math.sin(a)))
        # Høyre del
        pygame.draw.line(screen, white,
                         (x - (s * math.sqrt(130) / 12) * math.cos(math.atan(7 / 9) - a),
                          y + (s * math.sqrt(130) / 12) * math.sin(math.atan(7 / 9) - a)),
                         (x + s * math.cos(a), y + s * math.sin(a)))
        # Nederste del av romskipet
        pygame.draw.line(screen, white,
                         (x - (s * math.sqrt(2) / 2) * math.cos(a + math.pi / 4),
                          y - (s * math.sqrt(2) / 2) * math.sin(a + math.pi / 4)),
                         (x - (s * math.sqrt(2) / 2) * math.cos(-a + math.pi / 4),
                          y + (s * math.sqrt(2) / 2) * math.sin(-a + math.pi / 4)))


class Bullet():
    pass

class Asteroid():
    pass



def gameloop():
    # Initial variables
    player = Player(display_width // 2, display_height // 2)
    

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



        player.updatePlayer()

        # Draw triangle
        screen.fill((0, 0, 0))
        player.drawPlayer()
        
        pygame.display.flip()
        clock.tick(30)
        
gameloop()

pygame.quit()
sys.exit()
