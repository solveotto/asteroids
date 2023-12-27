import random
import math

from library import bullets
from library.utils import *


class Ufo():
    def __init__(self):
        """
        Initialize the UFO object with default attributes.
        """
        self.x = 0
        self.y = 0
        self.dir = 0
        self.directionChg = ()
        self.bullets = []
        self.bdir = 0 
        self.bdelay = 30
        self.spawn_time = 300
        self.state = "dead"
        self.type = "large"
        self.size = 20
        self.speed = 2
        self.small_ufo_acc = 10
        
        
    def create_ufo(self, player_score):
        """
        Create a UFO with random attributes based on the player's score.

        Parameters:
        - player_score (int): The score of the player.
        """
        self.state = "alive"
        self.spawn_time = 120

        # Størrelse
        if player_score < 40000:
            if random.randint(0,1) == 0:
                self.size = 20
                self.type = "large"
            else:
                self.size = 10
                self.type = "small"
        else:
            self.size = 10
            self.type = "small"
        
        # Hastighet
        self.speed = random.uniform(2, 4)
   
        # Tilfeldig plassering
        self.x = random.randint(100, int(DISPLAY_WIDTH/2))
        self.y = random.randint(100, int(DISPLAY_WIDTH/2))
        

        # Tilfeldig retning
        if self.x == 0:
            self.dir = 0 * math.pi / 180
            self.directionChg = (0, 45, -45)
        else:
            self.dir = 180 * math.pi / 180
            self.directionChg = (180, -180, 135, -135)


    def update_ufo(self):
        """
        Update the position and behavior of the UFO.
        """
        self.x += self.speed * math.cos(self.dir)
        self.y += self.speed * math.sin(self.dir)
        

        # Ufo kan endre retning tilfeldig
        if random.randrange(1,100) == 1:
            self.dir = random.choice(self.directionChg)

        # Warp-effekt:
        self.x, self.y = check_warp(self.x, self.y)


        # Skyting
        if self.bdelay == 0:
            # Store ufoer skyter tilfeldig
            if self.type == "large":
                self.bdir = random.randint(0,360)
                self.bullets.append(bullets.Bullet(self.x, self.y, self.bdir))
            # Små sikter bedre og bedre for hvert brett.
            elif self.type == "small":
                self.bullets.append(bullets.Bullet(self.x, self.y, self.bdir))

            self.bdelay = 30
        else:
            self.bdelay -= 1

    def get_ufo_score(self):
        """
        Get the score value of the UFO based on its type.

        Returns:
        int: The score value of the UFO.
        """
        if self.type == "large":
            return 200
        else:
            return 1000
        
            
        
    def draw_ufo(self):
        """
        Draw the UFO on the screen.
        """
        pygame.draw.polygon(SCREEN, WHITE, [(self.x+self.size,self.y), 
                                            (self.x+self.size/2 ,self.y+self.size/3),
                                            (self.x-self.size/2, self.y+self.size/3),
                                            (self.x-self.size, self.y),
                                            (self.x-self.size/3, self.y-self.size/3),
                                            (self.x+self.size/3, self.y-self.size/3)], width=1)
        pygame.draw.line(SCREEN, WHITE, (self.x-self.size, self.y), (self.x+self.size, self.y))
        pygame.draw.polygon(SCREEN, WHITE, [(self.x-self.size/3, self.y-self.size/3),
                                            (self.x-self.size/5, self.y-(self.size-self.size/4)),
                                            (self.x+self.size/5, self.y-(self.size-self.size/4)),
                                            (self.x+self.size/3, self.y-self.size/3)], width=1)

