import pygame
import sys
import math
import random
import time
import json

pygame.init()
clock = pygame.time.Clock()

### Konstanter ###
# Fysikk
fd_fric = 0.5
bd_fric = 0.1
player_max_speed = 20.0
player_max_rtspeed = 10


# Skjerm
display_width  = 800
display_height = 600
screen = pygame.display.set_mode((display_width, display_height))


# Lagring
saveFilePath = "highscore.json"
font_path = 'fonts/Hyperspace-JvEM.ttf'  # Replace with the path to your font file
font_size = 36  # You can set this to any size you want
custom_font = pygame.font.Font(font_path, font_size)


# Farger
white = (255, 255, 255)
yellow = (231, 245, 39)
black = (0, 0, 0)


def kollisjonssjekk(x, y, x2, y2, size):
    if x > x2 - size and x < x2 + size and y > y2 - size and y < y2 + size:
        return True
    return False

def drawText(msg, x, y, size, color, orient="centered"):
    text = pygame.font.Font(font_path, size).render(msg, True, color)
    if orient == "centered":
        # lager et rektangel med koordinatene til texten
        rect = text.get_rect()
        rect.center = (x, y)
    elif orient == "right":
        rect = text.get_rect()
        rect.right = x
        rect.y = y
    elif orient == "left":
        rect = text.get_rect()
        rect.left = x
        rect.y = y
    else:
        rect = (x,y)
    screen.blit(text, rect)


class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 10
        self.hspeed = 0
        self.vspeed = 0
        self.rtspeed = 0
        self.dir = -90
        self.thrust = False
        

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
        
    
class HighScore():
    def __init__(self, filepath):
        self.filepath = filepath
        self.highScore = []
        self.sortedHighScore = []
        
        
    def loadHighScore(self):
        with open(self.filepath, 'r') as file:
            data = json.load(file)
        self.highScore = data

    def saveHighScore(self):
        with open(self.filepath, 'w') as file:
            json.dump(self.highScore, file, indent=4)
    
    def sortHighScore(self):
        self.highScore = sorted(self.highScore, key=lambda x: list(x.values())[0], reverse=True)

    def getName(self):
        print("get name")
        running = True
        while running:
            drawText('''YOUR SCORE IS ONE OF THE TEN BEST\nPLEASE ENTER YOUR INITIALS''',
                    60,20,20, white)
            
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    running = False
                    break

    def evaluateScore(self, pScore, pName):
        break_flag = False  
        for hs in self.highScore:
            if break_flag:
                break
            for key, value in hs.items():
                print(pScore, value)
                if pScore > value:
                    self.getName()
                    if len(self.highScore) <= 11:
                        self.highScore.pop()
                    else:
                        self.highScore.insert(self.highScore.index(hs), {pName:pScore})
                        break_flag = True
                        break
                elif len(self.highScore) < 10:
                        self.getName()
                        self.highScore.append({pName:pScore})
                        break_flag = True
                        break
                
                    

        self.saveHighScore()
        print(self.highScore)


def gameloop(startingState):
    # Initial variables
    gameState = startingState
    highScoreLoaded = None
    player = Player(display_width // 2, display_height // 2)
    bullets = []
    asteroides = []
    player_pieces = []
    player_state = "alive"
    player_lives = 3
    player_score = 0
    player_name = "NEW"
    player_death_timer = 0
    player_blink = 0
    player_spawn_dur = 0
    player_extraLifeMulti = 1
    stage = 1
    
    try:
        highScore = HighScore(saveFilePath)
        highScore.loadHighScore()
        highScore.sortHighScore()
        highScoreLoaded = True
    except FileNotFoundError:
        highScoreLoaded = False
    
    # Main game loop
    while gameState != "exit":
        while gameState == "mainMenu":
            screen.fill(black)
            drawText("Asteroides", display_width/2, 100, 100, white)
            drawText(f"Highscores", display_width/2, 200, 34, white)
            
            highScoreNumber = 1
            highScorePos = 10

            if highScoreLoaded:
                for item in highScore.highScore:
                    for name, score in item.items():
                        drawText(f"{highScoreNumber}.", display_width/2 - 120, 220+(highScorePos * highScoreNumber*2+10), 22, white, orient="right")
                        drawText(f"{score}  {name}", display_width/2 + 120, 220+(highScorePos * highScoreNumber*2+10), 22, white, orient="right")
                        highScoreNumber += 1
            else:
                drawText(f"ERROR - NO DATA", display_width/2, 320, 30, white, orient="centered")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameState = "exit"
                if event.type == pygame.KEYDOWN:
                    gameState = "playing"
            pygame.display.update()
            clock.tick(5)
            

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = "exit"
                print("Break")
                break
                
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
                    player_lives -= 1
                    player.resetPlayer()
                    
                for b in bullets:
                    if kollisjonssjekk(b.x, b.y, a.x, a.y, a.size):
                        bullets.remove(b)
                        if a.s == "large":
                            player_score += 100
                            asteroides.append(Asteroid(a.x, a.y, "medium"))
                            asteroides.append(Asteroid(a.x, a.y, "medium"))
                        elif a.s == "medium":
                            player_score += 150
                            asteroides.append(Asteroid(a.x, a.y, "small"))
                            asteroides.append(Asteroid(a.x, a.y, "small"))
                        else:
                            player_score += 200
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
        drawText(x=15,y=10,size=26, msg="Poeng: "+str(player_score), color=white, orient="none")
        
        
        # Tegne antall liv
        for x in range(player_lives):
            Player((40+(x*20)),65).drawPlayer()

        pygame.display.flip()
        clock.tick(30)

    highScore.evaluateScore(player_score, player_name)

    
        
        
gameloop("mainMenu")


pygame.quit()
sys.exit()