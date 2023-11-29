import pygame
import sys
import math
import random
import time
import json
import pygame_textinput

pygame.init()
clock = pygame.time.Clock()


# Skjerm
display_width  = 800
display_height = 600
screen = pygame.display.set_mode((display_width, display_height))


# Farger
white = (255, 255, 255)
yellow = (231, 245, 39)
black = (0, 0, 0)


class ufo():
    def __init__(self, size):
        self.x = random.randrange(0, display_width)
        self.y = random.randrange(0, display_width)
        
        
        self.size = size
        self.angle = random.randrange(0, 360) * math.pi / 180
        
        
    def update_ufo(self):
        pygame.draw.polygon(screen, white, [(50,100), (48, 106), (58, 106), (56, 100)], width=1)



    
ufo1 = ufo("large")      
runing = True
while runing:
    screen.fill(black)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
    
    ufo1.update_ufo()   
    
    pygame.display.flip()

pygame.quit()
sys.exit()