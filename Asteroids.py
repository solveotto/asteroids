import pygame
import sys
import math
import random
import json
import pygame_textinput



'''
TO DO's: 
- lage en funksjon for warp-sjekk
- Flytte flere spillervariabler i klassen
- Gjøre om main loop til en klasse.
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


# Lyder
snd_fire = pygame.mixer.Sound("sounds/fire.wav")
snd_thrust = pygame.mixer.Sound("sounds/thrust.wav")
snd_bang_large = pygame.mixer.Sound("sounds/bangLarge.wav") 




def collision(x, y, x2, y2, size):
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
         
            
class DeadPlayer():
    def __init__(self, x, y, l):
        self.x = x
        self.y = y
        self.length = l
        self.angle = random.randrange(0, 360) * math.pi / 180
        self.dir = random.randrange(0, 360) * math.pi / 180
        self.rtsp = random.uniform(-0.25, 0.25)
        self.speed = random.randint(2,8)
        

    def update_dead_player(self):
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
        self.life = 25
    

    def update_bullet(self):
        
        self.x += self.speed * math.cos(self.dir * math.pi / 180)
        self.y += self.speed * math.sin(self.dir * math.pi / 180)
        
        pygame.draw.circle(screen, white, (int(self.x), int(self.y)), self.size)
        
        self.life -= 1

        # Warp-effekt:
        if self.y < 0:
            self.y = display_height
        elif self.y > display_height:
            self.y = 0
        elif self.x < 0:
            self.x = display_width
        elif self.x > display_width:
            self.x = 0



class Rocks():
    def __init__(self, x, y, s):
        self.pos = 400
        self.x = x
        self.y = y
        if s == "large":
            self.size = 30
        elif s == "medium":
            self.size = 20
        elif s == "small":
            self.size = 10
        self.type = s
        

        # Setter random retning og fart
        self.dir = random.randrange(0,360) * math.pi / 180
        self.speed = random.randrange(1,5)

        # Lager tilfeldige vektorer helt til det danner en hel sirkel
        full_circle = random.uniform(18,36)
        dist = random.uniform(self.size / 2, self.size)
        self.vectors = []
        while full_circle < 360:
            self.vectors.append([dist, full_circle])
            full_circle += random.uniform(18,36)
            dist = random.uniform(self.size / 2, self.size)


    def update_asteroide(self):
        # MBeveger astroide 
        self.x += self.speed * math.cos(self.dir)
        self.y += self.speed * math.sin(self.dir)

        # Wrapping
        if self.x > display_width:
            self.x = 0
        elif self.x < 0:
            self.x = display_width
        elif self.y > display_height:
            self.y = 0
        elif self.y < 0:
            self.y = display_height

        
        # Tegner astroiden basert til vektorene som alt er laget
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
        self.spawn_time = 200
        self.state = "dead"
        self.type = "large"
        self.size = 20
        self.speed = 2
        
        
    def create_ufo(self):
        self.state = "alive"
        self.spawn_time = 120

        # Størrelse
        if random.randint(0,1) == 0:
            self.size = 20
            self.type = "large"
        else:
            self.size = 10
            self.type = "small"
        
        # Hastighet
        self.speed = random.uniform(2, 4)
   
        # Tilfeldig plassering
        self.x = random.randint(100, int(display_width/2))
        self.y = random.randint(100, int(display_width/2))
        

        # Tilfeldig retning
        if self.x == 0:
            self.dir = 0 * math.pi / 180
            self.directionChg = (0, 45, -45)
        else:
            self.dir = 180 * math.pi / 180
            self.directionChg = (180, -180, 135, -135)


    def update_ufo(self):
        self.x += self.speed * math.cos(self.dir)
        self.y += self.speed * math.sin(self.dir)
        

        # Ufo kan endre retning tilfeldig
        if random.randrange(1,100) == 1:
            self.dir = random.choice(self.directionChg)

        # Warping
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

    def get_ufo_score(self):
        if self.type == "large":
            return 200
        else:
            return 1000
        
            
        
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

        # Highscore loop
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


    # Sjekker om poengsummen er en highscore
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




# HighScore
try:
    highScore = HighScore(saveFilePath)
    highScore.loadHighScore()
    highScore.sortHighScore()
    highScoreLoaded = True
except FileNotFoundError:
    highScoreLoaded = False


def mainMenu():
    mainMenuRunnig = True
    asteroides = []
    menuChoice = "none"

    while mainMenuRunnig:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                
                mainMenuRunnig = False

            if event.type == pygame.KEYDOWN:
                mainMenuRunnig = False
                asteroides = []
                menuChoice = "play"

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

        
        # Astroide i bakgrunnen
        if len(asteroides) == 0:     
            for x in range(4):
                xSpwn = random.randint(0, int(display_width/2))
                ySpwn = random.randint(0, int(display_height/2))
                asteroides.append(Rocks(xSpwn, ySpwn, "large"))
        for a in asteroides:
            a.update_asteroide()
 

        pygame.display.update()
        clock.tick(30)
        
    if menuChoice == "play":
        gameloop("playing")


def gameloop(startingState):
    # Initial variables
    gameState = startingState
    highScoreLoaded = None
    player = Player(display_width // 2, display_height // 2)
    ufo = Ufo()
    player_bullets = []
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
    nextLvlDelay  = 30
    gameOverDelay = 120
    small_ufo_acc = 10
    hyperspace = 0

    print("Game Starting")




    # Main loop
    while gameState != "exit":

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
                    player_bullets.append(Bullet(player.x, player.y, player.dir))
                    snd_fire.play()
                if event.key == pygame.K_LSHIFT and player_state == "alive":
                    hyperspace = 30
        

        screen.fill((0, 0, 0))
        player.updatePlayer()

        # GFX           
        # Current score
        drawText(x=15,y=10,size=26, msg="Poeng: "+str(player_score), color=white, orient="none")
        
        # Current lives
        for x in range(player_lives):
            Player((40+(x*20)),65).drawPlayer()


        # PLAYER LOGIC
        for fragmet in player_pieces:
            fragmet.update_dead_player()
    

        # Bullets
        if len(player_bullets) > 0:
            for bullet in player_bullets:
                bullet.update_bullet()
                if bullet.life == 0:
                    player_bullets.remove(bullet)

        # Hyperspace
        if hyperspace != 0:
            player_state = "dead"
            hyperspace -= 1
            print("hyperspace")
            if hyperspace == 1:
                player.x = random.randrange(0, display_width)
                player.x = random.randrange(0, display_height)


        ## UFO LOGIKK ##
        if ufo.state == "dead":
            if ufo.spawn_time == 0 and player_state == "alive":
                if random.randrange(0,1000) == 0:
                    ufo.create_ufo()
                    print("ufo created")
            else:
                ufo.spawn_time -= 1
        else:
            # Ufo nøyaktighet og kuleretning
            acc = small_ufo_acc * 4 / stage
            ufo.bdir = math.degrees(math.atan2(-ufo.y + player.y, -ufo.x + player.x) + 
                                    math.radians(random.uniform(acc, -acc)))

            ufo.update_ufo()
            ufo.draw_ufo()
            
            # Sjekk UFOs kollisjon med spiller
            if player_state != "dead":
                if collision(player.x, player.y, ufo.x, ufo.y, ufo.size):
                    ufo.state = "dead"

                    player_score += ufo.get_ufo_score()
                    
                    player_pieces.append(DeadPlayer(player.x, player.y, 5 * player.size / (2 * math.cos(math.atan(1 / 3)))))
                    player_pieces.append(DeadPlayer(player.x, player.y, player.size))
                    player_pieces.append(DeadPlayer(player.x, player.y, player.size / 2))
                    player_state = "dead"
                    player_spawn_dur  = 120
                    player_death_timer = 30
                    player_lives -= 1
                    player.resetPlayer()
            

            # Sjekker om UFO kolliderer med astroider
            for a in asteroides:
                if collision(a.x, a.y, ufo.x, ufo.y, a.size):
                    ufo.state = "dead"
                    if a.type == "large":
                        asteroides.append(Rocks(a.x,a.y, "medium"))
                        asteroides.append(Rocks(a.x,a.y, "medium"))
                    elif a.type == "medium":
                        asteroides.append(Rocks(a.x,a.y, "small"))
                        asteroides.append(Rocks(a.x,a.y, "small"))

                    asteroides.remove(a)

            
            # UFO kuler
            for b in ufo.bullets:
                b.update_bullet()

                # Sjekker om kule treffer spiller
                if collision(player.x, player.y, b.x, b.y, player.size):
                    ufo.bullets.remove(b)
                    ufo.state = "dead"

                    player_pieces.append(DeadPlayer(player.x, player.y, 5 * player.size / (2 * math.cos(math.atan(1 / 3)))))
                    player_pieces.append(DeadPlayer(player.x, player.y, player.size))
                    player_pieces.append(DeadPlayer(player.x, player.y, player.size / 2))
                    player_state = "dead"
                    player_spawn_dur  = 120
                    player_death_timer = 30
                    player_lives -= 1
                    player.resetPlayer()
                    break

                # Sjekker om kuler treffer astroide
                for a in asteroides:
                    if collision(b.x, b.y, a.x, a.y, a.size):
                        asteroides.remove(a)
                        ufo.bullets.remove(b)
                        if a.type == "large":
                            asteroides.append(Rocks(a.x,a.y, "medium"))
                            asteroides.append(Rocks(a.x,a.y, "medium"))
                        elif a.type == "medium":
                            asteroides.append(Rocks(a.x,a.y, "small"))
                            asteroides.append(Rocks(a.x,a.y, "small"))   
                        break                   
                        

                # Fjerner kule etter gitt tid    
                if b.life <= 0 and b in ufo.bullets:
                    ufo.bullets.remove(b)
                        

            # Sjekke spillers kuler mot UFO
            for b in player_bullets:
                if collision(b.x, b.y, ufo.x, ufo.y, ufo.size):
                    ufo.state = "dead"
                    player_score += ufo.get_ufo_score()
                    
                    



        ## ASTROIDE LOGIKK ##

        # Genererer Asteroider vekk fra senter
        if len(asteroides) == 0 and player_state == "alive":
            if nextLvlDelay >= 0:
                nextLvlDelay -= 1
            else:
                dw = display_width
                dh = display_height
                for x in range(stage+3):
                    xSpwn = dw / 2
                    ySpwn = dh / 2
                    while xSpwn - dw / 2 < dw / 4 and ySpwn - dh / 2 < dh /4:
                        xSpwn = random.randrange(0, dw)
                        ySpwn = random.randrange(0, dh)
                    asteroides.append(Rocks(xSpwn, ySpwn, "large"))
                nextLvlDelay = 30

        for a in asteroides:
            a.update_asteroide()
            if player_state != "dead":
                if collision(player.x, player.y, a.x, a.y, a.size):
                    player_pieces.append(DeadPlayer(player.x, player.y, 5 * player.size / (2 * math.cos(math.atan(1 / 3)))))
                    player_pieces.append(DeadPlayer(player.x, player.y, player.size))
                    player_pieces.append(DeadPlayer(player.x, player.y, player.size / 2))

                    # Spiller dør
                    player_state = "dead"
                    player_spawn_dur  = 120
                    player_death_timer = 30
                    player_lives -= 1
                    player.resetPlayer()
                
                # Sjekker om spillers kuler treffer astroide
                for b in player_bullets:
                    if collision(b.x, b.y, a.x, a.y, a.size):
                        player_bullets.remove(b)
                        if a.type == "large":
                            player_score += 20
                            asteroides.append(Rocks(a.x, a.y, "medium"))
                            asteroides.append(Rocks(a.x, a.y, "medium"))
                        elif a.type == "medium":
                            player_score += 50
                            asteroides.append(Rocks(a.x, a.y, "small"))
                            asteroides.append(Rocks(a.x, a.y, "small"))
                        else:
                            player_score += 100
                        asteroides.remove(a)
                        

            # Tegne spiller
        if gameState != "gameOver":
            
            # sjekker om spiller spawner
            if player_spawn_dur != 0:
                player_spawn_dur -= 1
            else:
                player_state = "alive"

            if player_state == "dead":
                if hyperspace == 0:
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



        # Is game over
        if player_lives == 0:
            gameState = "gameOver"
            if gameOverDelay > 0:
                drawText(x=300, y=400,size=40, msg="Game Over", color=white, orient="none")
                gameOverDelay -= 1
            else:
                highScore.evaluateScore(player_score)
                gameState = "exit"
                




        pygame.display.flip()
        clock.tick(30)
    
    print("exit Game Loop")
    mainMenu()



if __name__ == "__main__":
        
    mainMenu()


    pygame.quit()
    sys.exit()