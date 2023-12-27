import random
import math
from library.utils import *


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
        self.small_ufo_acc = 10
        

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
        if self.x > DISPLAY_WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = DISPLAY_WIDTH
        elif self.y > DISPLAY_HEIGHT:
            self.y = 0
        elif self.y < 0:
            self.y = DISPLAY_HEIGHT

        
        # Tegner astroiden basert til vektorene som alt er laget
        for v in range(len(self.vectors)):
            if v == len(self.vectors) -1:
                next_v = self.vectors[0]
            else:
                next_v = self.vectors[v + 1]
            this_v = self.vectors[v]

            pygame.draw.line(SCREEN, WHITE, (self.x + this_v[0] * math.cos(this_v[1] * math.pi / 180),
                                             self.y + this_v[0] * math.sin(this_v[1] * math.pi / 180)),
                                             (self.x + next_v[0] * math.cos(next_v[1] * math.pi / 180),
                                              self.y + next_v[0] * math.sin(next_v[1] * math.pi / 180)))
        
class ManageRocks():
    def __init__(self):
        self.asteroids = []



    def spawn_asteroids(self, stage, player_):
        '''Spawns asteroids away from center of screen'''
        
        dw = DISPLAY_WIDTH
        dh = DISPLAY_HEIGHT
        for x in range(stage+3):
            xSpwn = dw / 2
            ySpwn = dh / 2
            while xSpwn - dw / 2 < dw / 4 and ySpwn - dh / 2 < dh /4:
                xSpwn = random.randrange(0, dw)
                ySpwn = random.randrange(0, dh)
            self.asteroids.append(Rocks(xSpwn, ySpwn, "large"))
        nextLvlDelay = 30
    
    def split_asteroid(self, ast):
        '''Splits asteroids into smaller ones'''
        if ast.type == "large":
            self.asteroids.append(Rocks(ast.x, ast.y, "medium"))
            self.asteroids.append(Rocks(ast.x, ast.y, "medium"))
            SND_CHANNEL_OTHER.play(SND_BANG_LARGE)
        elif ast.type == "medium":
            self.asteroids.append(Rocks(ast.x, ast.y, "small"))
            self.asteroids.append(Rocks(ast.x, ast.y, "small"))
            SND_CHANNEL_OTHER.play(SND_BANG_MEDIUM)
        elif ast.type == "small":
            SND_CHANNEL_OTHER.play(SND_BANG_SMALL)