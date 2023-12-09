import pygame
import sys
import math
import random
import time
import json
import pygame_textinput

'''
TO DO's:
- Add game over screen
- Add ufo bullet damage
- lage en funksjon for warp-sjekk
'''



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




def warp():
    # Bytte ut alle warp-sjekkene med en funksjon
    pass


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
        self.life = 45
    

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
        self.type = s
        

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
        

class Ufo():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dir = 0
        self.directionChg = ()
        self.bullets = []
        self.bdir = 0 
        self.bdelay = 30
        self.state = "dead"
        self.type = "large"
        self.size = 20
        self.speed = 2
        
        
    def create_ufo(self):
        self.state = "alive"

        # Random size
        if random.randint(0,1000000) == 0:
            self.size = 20
            self.type = "large"
        else:
            self.size = 10
            self.type = "small"
        
        # Random speed
        self.speed = random.uniform(2, 4)
   
        # Tilfeldig plassering
        self.x = random.randint(100, display_width/2)
        self.y = random.randint(100, display_width/2)
        
        # Random direction 
        if self.x == 0:
            self.dir = 0 * math.pi / 180
            self.directionChg = (0, 45, -45)
        else:
            self.dir = 180 * math.pi / 180
            self.directionChg = (180, -180, 135, -135)


    def update_ufo(self):
        self.x += self.speed * math.cos(self.dir)
        self.y += self.speed * math.sin(self.dir)
        

        # Change direction
        if random.randrange(1,100) == 1:
            self.dir = random.choice(self.directionChg)

        # Warping effekt
        if self.x > display_width:
            self.x = 0
        elif self.x < 0:
            self.x = display_width
        elif self.y > display_height:
            self.y = 0
        elif self.y < 0:
            self.y = display_height


        # Skyting
        if self.bdelay == 0:
            # Store ufoer skyter tilfeldig
            if self.type == "large":
                self.bdir = random.randint(0,360)
                self.bullets.append(Bullet(self.x, self.y, self.bdir))
            # Små sikter bedre og bedre for hvert brett.
            elif self.type == "small":
                self.bullets.append(Bullet(self.x, self.y, self.bdir))

            self.bdelay = 30
        else:
            self.bdelay -= 1
            
        
    def draw_ufo(self):
        pygame.draw.polygon(screen, white, [(self.x+self.size,self.y), 
                                            (self.x+self.size/2 ,self.y+self.size/3),
                                            (self.x-self.size/2, self.y+self.size/3),
                                            (self.x-self.size, self.y),
                                            (self.x-self.size/3, self.y-self.size/3),
                                            (self.x+self.size/3, self.y-self.size/3)], width=1)
        pygame.draw.line(screen, white, (self.x-self.size, self.y), (self.x+self.size, self.y))
        pygame.draw.polygon(screen, white, [(self.x-self.size/3, self.y-self.size/3),
                                            (self.x-self.size/5, self.y-(self.size-self.size/4)),
                                            (self.x+self.size/5, self.y-(self.size-self.size/4)),
                                            (self.x+self.size/3, self.y-self.size/3)], width=1)


class HighScore():
    def __init__(self, filepath):
        self.filepath = filepath
        self.highScore = []
        self.sortedHighScore = []
        self.pName = ["_", "_", "_"]
        
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
        manager = pygame_textinput.TextInputManager(validator=lambda input: len(input) <= 3)
        textInput = pygame_textinput.TextInputVisualizer(manager=manager)

        running = True
        while running:
            screen.fill(black)
            drawText("POENGSUMMEN DIN ER EN AV DE TI BESTE.", display_width/10, 60, 30, white, orient="left")
            drawText("SKRIV SKRIV INN TRE INITIALER.", display_width/10, 90, 30, white, orient="left")
            drawText("TRYKK ENTER NÅR DU ER FERIDG.", display_width/10, 120, 30, white, orient="left")
       
            drawText(self.pName[0], display_width/2, display_height/2, 30, white)
            drawText(self.pName[1], display_width/2+20, display_height/2, 30, white)
            drawText(self.pName[2], display_width/2+40, display_height/2, 30, white)

            events = pygame.event.get() 

            textInput.update(events)

            if len(textInput.value) == 1:
                self.pName = [textInput.value[0], "_", "_"]
            elif len(textInput.value) == 2:
                self.pName = [textInput.value[0], textInput.value[1], "_"]
            elif len(textInput.value) == 3:
                self.pName = [textInput.value[0], textInput.value[1], textInput.value[2]]
            else:
                self.pName = ["_", "_", "_"]

            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False
                        break

            pygame.display.update()
        if self.pName == ["_", "_", "_"]:
            self.pName = [" "," "," "]


    def evaluateScore(self, pScore):
        break_flag = False  
        for hs in self.highScore:
            if break_flag:
                break
            for key, value in hs.items():
                if pScore > value:
                    self.getName()
                    self.highScore.insert(self.highScore.index(hs), {''.join(self.pName):pScore})
                    break_flag = True
                    break
                elif len(self.highScore) < 10:
                    self.getName()
                    self.highScore.append({''.join(self.pName):pScore})
                    break_flag = True
                    break
        if len(self.highScore) >= 11:
            self.highScore.pop()
                
                    
        self.sortHighScore()
        self.saveHighScore()
        print(self.highScore)


def gameloop(startingState):
    # Initial variables
    gameState = startingState
    highScoreLoaded = None
    player = Player(display_width // 2, display_height // 2)
    ufo = Ufo()
    bullets = []
    asteroides = []
    player_pieces = []
    player_state = "alive"
    player_lives = 3
    player_score = 0
    player_death_timer = 0
    player_blink = 0
    player_spawn_dur = 0
    player_extraLifeMulti = 1
    stage = 1
    nextLvlDelay  = 0
    small_ufo_acc = 10


    
    try:
        highScore = HighScore(saveFilePath)
        highScore.loadHighScore()
        highScore.sortHighScore()
        highScoreLoaded = True
    except FileNotFoundError:
        highScoreLoaded = False

    
    # Main game loop
    while gameState != "exit":
        while gameState == "mainMenu" and gameState != "exit":
            screen.fill(black)
            drawText("Asteroides", display_width/2, 100, 100, white)
            drawText(f"Highscores", display_width/2, 200, 34, white)
            drawText(f"1 COIN 1 PLAY", display_width/2, 550, 26, white)  
            
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
                    
                        
            if len(asteroides) == 0:     
                for x in range(4):
                    xSpwn = random.randint(0, display_width/2)
                    ySpwn = random.randint(0, display_height/2)
                    asteroides.append(Asteroid(xSpwn, ySpwn, "large"))
            for a in asteroides:
                a.update_asteroide()
            
            if gameState == "playing":
                # Tilbakestiller astroider fra mainMenu   
                asteroides = []                    


            pygame.display.update()
            clock.tick(30)




        while gameState == "playing" and gameState != "exit":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameState = "exit"
                    
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
                if nextLvlDelay < 30:
                    nextLvlDelay += 1
                else:
                    dw = display_width
                    dh = display_height
                    for x in range(stage+6):
                        xSpwn = dw / 2
                        ySpwn = dh / 2
                        while xSpwn - dw / 2 < dw / 4 and ySpwn - dh / 2 < dh /4:
                            xSpwn = random.randrange(0, dw)
                            ySpwn = random.randrange(0, dh)
                        asteroides.append(Asteroid(xSpwn, ySpwn, "large"))


            ## UFO LOGIKK ##
            if ufo.state == "dead":
                if random.randrange(0,100) == 0:
                    ufo.create_ufo()
                    print("ufo created")
            else:
                # UFO-kontroll
            
                acc = small_ufo_acc * 4 / stage
                ufo.bdir = math.degrees(math.atan2(-ufo.y + player.y, -ufo.x + player.x) + 
                                        math.radians(random.uniform(acc, -acc)))

                ufo.update_ufo()
                ufo.draw_ufo()
                
                # Sjekk UFOs kollisjon med spiller
                if player_state != "dead":
                    if kollisjonssjekk(player.x, player.y, ufo.x, ufo.y, ufo.size):
                        ufo.state = "dead"
                        
                        player_pieces.append(deadPlayer(player.x, player.y, 5 * player.size / (2 * math.cos(math.atan(1 / 3)))))
                        player_pieces.append(deadPlayer(player.x, player.y, player.size))
                        player_pieces.append(deadPlayer(player.x, player.y, player.size / 2))
                        player_state = "dead"
                        player_spawn_dur  = 120
                        player_death_timer = 30
                        player_lives -= 1
                        player.resetPlayer()
                

                # Sjekker om UFO kolliderer med astroider
                for a in asteroides:
                    if kollisjonssjekk(a.x, a.y, ufo.x, ufo.y, a.size):
                        #ufo.bullets.remove(b)opiojk,msv c

                        print("UFO COLLIDED WITH ASTROIDE")
                        ufo.state = "dead"

                        if a.type == "large":
                            asteroides.append(Asteroid(a.x,a.y, "small"))
                            asteroides.append(Asteroid(a.x,a.y, "small"))
                        else:
                            pass

                        asteroides.remove(a)

                
                # UFO kuler
                for b in ufo.bullets:
                    b.update_bullet()

                    # Sjekker treff mot spiller
                    if kollisjonssjekk(player.x, player.y, b.x, b.y, player.size):
                        ufo.bullets.remove(b)
                        player_pieces.append(deadPlayer(player.x, player.y, 5 * player.size / (2 * math.cos(math.atan(1 / 3)))))
                        player_pieces.append(deadPlayer(player.x, player.y, player.size))
                        player_pieces.append(deadPlayer(player.x, player.y, player.size / 2))
                        player_state = "dead"
                        player_spawn_dur  = 120
                        player_death_timer = 30
                        player_lives -= 1
                        player.resetPlayer()

                    # Sjekker treff mot astroide
                    for a in asteroides:
                        if kollisjonssjekk(b.x, b.y, a.x, a.y, a.size):
                            if a.type == "large":
                                asteroides.remove(a)
                                asteroides.append(Asteroid(a.x,a.y, "small"))
                                asteroides.append(Asteroid(a.x,a.y, "small"))
                            else:
                                asteroides.remove(a)
                                
                    if b.life <= 0:
                        ufo.bullets.remove(b)
                            

                # Sjekker 

                # Sjekke spillers kuler mot UFO



                                


                    



            # Astroide-kontroll
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
                            if a.type == "large":
                                player_score += 100
                                asteroides.append(Asteroid(a.x, a.y, "medium"))
                                asteroides.append(Asteroid(a.x, a.y, "medium"))
                            elif a.type == "medium":
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
            if player_state != "gameOver":
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

            if player_lives == 0:
                gameState = "mainMenu"
                highScore.evaluateScore(player_score)
                gameloop("mainMenu") 
            
            # Tegne poengsum
            drawText(x=15,y=10,size=26, msg="Poeng: "+str(player_score), color=white, orient="none")
            
            
            # Tegne antall liv
            for x in range(player_lives):
                Player((40+(x*20)),65).drawPlayer()

            pygame.display.flip()
            clock.tick(30)

        
gameloop("mainMenu")


pygame.quit()
sys.exit()