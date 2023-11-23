import pygame
import sys
import math
import random
import time

pygame.init()


### Initital Constants ###
# Movement settings
fd_fric = 0.5
bd_fric = 0.1
player_max_speed = 20.0
player_max_rtspeed = 10

# Screen settings
display_width  = 800
display_height = 600
screen = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

# Farger
white = (255, 255, 255)
yellow = (231, 245, 39)


def kollisjonssjekk(x, y, x2, y2, size):
    if x > x2 - size and x < x2 + size and y > y2 - size and y < y2 + size:
        return True
    return False

def drawText(msg, x, y, size, color, centered=True):
    text = pygame.font.SysFont("Calibri", size).render(msg, True, color)
    screen.blit(text, (x,y))


class Player():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.hspeed = 0
        self.vspeed = 0
        self.rtspeed = 0
        self.dir = -90
        self.thrust = False
        self.score = 0
        
        self.size = 10
        self.life = 3
    
    
    def updatePlayer(self):
        
        # Hastighetsstyring
        speed = math.sqrt(self.hspeed**2 + self.vspeed**2)
        if self.thrust == True:
            if speed < player_max_speed:
                self.hspeed += fd_fric * math.cos(self.dir * math.pi / 180)
                self.vspeed += fd_fric * math.sin(self.dir * math.pi / 180)
            else:
                # BUG: Styringen endrer seg når skipet kommer i topphastiget.
                self.hspeed = player_max_speed * math.cos(self.dir * math.pi / 180)
                self.vspeed = player_max_speed * math.sin(self.dir * math.pi / 180)
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

        
        # Warp-effekt:
        if self.y < 0:
            self.y = display_height
        elif self.y > display_height:
            self.y = 0
        elif self.x < 0:
            self.x = display_width
        elif self.x > display_width:
            self.x = 0
        
        # Oppdaterer posisjon og rotasjon
        self.x += self.hspeed
        self.y += self.vspeed
        self.dir += self.rtspeed


    def drawPlayer(self):
        angle = math.radians(self.dir)
        size = self.size
        x = self.x
        y = self.y

        # Tegner romskipet:
        # Venstre strek.
        pygame.draw.line(screen, white,
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
        pygame.draw.line(screen, white,
                         # Øverste punktet på streken.
                         (x + size * math.cos(angle), 
                          y + size * math.sin(angle)),
                         # Nederste punktet på streken.
                         (x - (size * math.sqrt(130) / 12) * math.cos(math.atan(7 / 9) - angle),
                          y + (size * math.sqrt(130) / 12) * math.sin(math.atan(7 / 9) - angle)))
        # Nederste strek.
        pygame.draw.line(screen, white,
                         # Venstre punkt.
                         (x - (size * math.sqrt(2) / 2) * math.cos(math.pi / 4 + angle),
                          y - (size * math.sqrt(2) / 2) * math.sin(math.pi / 4 + angle)),
                         # Høyre punkt.
                         (x - (size * math.sqrt(2) / 2) * math.cos(math.pi / 4 + -angle),
                          y + (size * math.sqrt(2) / 2) * math.sin(math.pi / 4 + -angle)))
        
        # Hvis det blir gitt thrust, så tegnes det en stikkflamme.
        if self.thrust:
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
            

    def resetPlayer(self):
        self.x = display_width // 2
        self.y = display_height // 2
        self.hspeed = 0
        self.vspeed = 0
        self.rtspeed = 0
        self.dir = -90
        self.thrust = False
        
            
            
class deadPlayer():
    def __init__(self, x, y, l):
        self.x = x
        self.y = y
        self.length = l
        self.angle = random.randrange(0, 360) * math.pi / 180
        self.dir = random.randrange(0, 360) * math.pi / 180
        self.rtsp = random.uniform(-0.25, 0.25)
        self.speed = random.randint(2,8)


    def updateDeadPlayer(self):
            pygame.draw.line(screen, white, 
                                (self.x + self.length * math.cos(self.angle) / 2,
                                self.y + self.length * math.sin(self.angle) / 2),
                                (self.x - self.length * math.cos(self.angle) / 2,
                                self.y - self.length * math.sin(self.angle) / 2))
            
            self.x += self.speed * math.cos(self.dir)
            self.y += self.speed * math.sin(self.dir)
            self.angle += self.rtsp
        

class Bullet():
    def __init__(self, x, y, dir) -> None:
        self.x = x
        self.y = y
        self.dir = dir
        self.size = 2
        self.speed = 15
        self.life = 40
    

    def update_bullet(self):
        
        self.x += self.speed * math.cos(self.dir * math.pi / 180)
        self.y += self.speed * math.sin(self.dir * math.pi / 180)
        
        pygame.draw.circle(screen, white, (int(self.x), int(self.y)), self.size)
        
        self.life -= 1


class Asteroid():
    def __init__(self, x, y, s):
        self.pos = 400
        self.x = x
        self.y = y
        if s == "large":
            self.size = 30
        elif s == "medium":
            self.size = 20
        else:
            self.size = 10
        self.s = s
        

        # Setter random retning og fart
        self.dir = random.randrange(0,360) * math.pi / 180
        self.speed = random.randrange(1,5)

        full_circle = random.uniform(18,36)
        dist = random.uniform(self.size / 2, self.size)
        self.vectors = []
        while full_circle < 360:
            self.vectors.append([dist, full_circle])
            full_circle += random.uniform(18,36)
            dist = random.uniform(self.size / 2, self.size)


    def update_asteroide(self):
        # Move asteroide  
        self.x += self.speed * math.cos(self.dir)
        self.y += self.speed * math.sin(self.dir)

        # Check for wrapping
        if self.x > display_width:
            self.x = 0
        elif self.x < 0:
            self.x = display_width
        elif self.y > display_height:
            self.y = 0
        elif self.y < 0:
            self.y = display_height

        for v in range(len(self.vectors)):
            if v == len(self.vectors) -1:
                next_v = self.vectors[0]
            else:
                next_v = self.vectors[v + 1]
            this_v = self.vectors[v]

            pygame.draw.line(screen, white, (self.x + this_v[0] * math.cos(this_v[1] * math.pi / 180),
                                             self.y + this_v[0] * math.sin(this_v[1] * math.pi / 180)),
                                             (self.x + next_v[0] * math.cos(next_v[1] * math.pi / 180),
                                              self.y + next_v[0] * math.sin(next_v[1] * math.pi / 180)))
        



def gameloop():
    # Initial variables
    player = Player(display_width // 2, display_height // 2)
    bullets = []
    asteroides = []
    player_pieces = []
    player_state = "alive"
    player_death_timer = 0
    player_blink = 0
    player_spawn_dur = 0
    stage = 1
    
    
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
                if event.key == pygame.K_SPACE and player_state == "alive":
                    bullets.append(Bullet(player.x, player.y, player.dir))


        screen.fill((0, 0, 0))
        
        player.updatePlayer()
        
        
        # sjekker om spiller spawner
        if player_spawn_dur != 0:
            player_spawn_dur -= 1
        else:
            player_state = "alive"
        
        
        # Genererer Asteroider vekk fra senter
        if len(asteroides) == 0 and player_state == "alive":
            dw = display_width
            dh = display_height       
            for x in range(stage+3):
                xSpwn = dw / 2
                ySpwn = dh / 2
                while xSpwn - dw / 2 < dw / 4 and ySpwn - dh < dh /4:
                    xSpwn = random.randrange(0, dw)
                    ySpwn = random.randrange(0, dh)
                asteroides.append(Asteroid(xSpwn, ySpwn, "large"))

                

        # Asteroides
        for a in asteroides:
            a.update_asteroide()
            if player_state != "dead":
                if kollisjonssjekk(player.x, player.y, a.x, a.y, a.size):
                    player_pieces.append(deadPlayer(player.x, player.y, 5 * player.size / (2 * math.cos(math.atan(1 / 3)))))
                    player_pieces.append(deadPlayer(player.x, player.y, player.size))
                    player_pieces.append(deadPlayer(player.x, player.y, player.size / 2))

                    # Spiller dør
                    player_state = "dead"
                    player_spawn_dur  = 120
                    player_death_timer = 30
                    player.life -= 1
                    player.resetPlayer()
                    
                for b in bullets:
                    if kollisjonssjekk(b.x, b.y, a.x, a.y, a.size):
                        bullets.remove(b)
                        if a.s == "large":
                            player.score += 100
                            asteroides.append(Asteroid(a.x, a.y, "medium"))
                            asteroides.append(Asteroid(a.x, a.y, "medium"))
                        elif a.s == "medium":
                            player.score += 150
                            asteroides.append(Asteroid(a.x, a.y, "small"))
                            asteroides.append(Asteroid(a.x, a.y, "small"))
                        else:
                            player.score += 200
                        asteroides.remove(a)
                        

        for fragmet in player_pieces:
            fragmet.updateDeadPlayer()
        
        

        # Bullets
        if len(bullets) > 0:
            for bullet in bullets:
                bullet.update_bullet()
                if bullet.life == 0:
                    bullets.remove(bullet)


        # Tegne spiller
        if player_state == "dead":
            if player_death_timer == 0:
                if player_blink < 5:
                    if player_blink == 0:
                        player_blink = 10
                    else:
                        player.drawPlayer()
                player_blink -= 1
            else:
                player_death_timer -= 1
        else:
            player.drawPlayer()
            
        
        # Tegne poengsum
        drawText(x=20,y=20,size=30, msg="Poeng: "+str(player.score), color=white, centered=False)
        

        pygame.display.flip()
        clock.tick(30)
        
gameloop()

pygame.quit()
sys.exit()