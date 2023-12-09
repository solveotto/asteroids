import pygame
import sys
import math
import random
import time
import json
import pygame_textinput




class ufo():
    def __init__(self):
        self.x = random.randrange(100, display_width/2)
        self.y = random.randrange(100, display_width/2)
        self.speed = random.uniform(0.12,0.3)
        self.bullets = []
        self.bdir = 0 
        
        
        # Random size
        if random.randint(0,1) == 0:
            self.size = 20
            self.type = "large"
        else:
            self.size = 10
            self.type = "small"
   
        
        # Random direction 
        if self.x == 0:
            self.dir = 0
            self.directionChg = [0, 45, -45]
        else:
            self.dir = 180
            self.directionChg = [180, -180, 135, -135]

        
    
  
    def update_ufo(self):
        self.x += self.speed * math.cos(self.dir)
        self.y += self.speed * math.sin(self.dir)
        

        # Change direction
        if random.randrange(1,1000) == 1:
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


        # Shooting
        
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



if __name__ == "__main__":    

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

    
    ufo1 = ufo()      
    runing = True
    while runing:
        screen.fill(black)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runing = False
        
        ufo1.update_ufo()
        ufo1.draw_ufo()   
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()