import math
import pygame

from library.utils import *



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
        
        pygame.draw.circle(SCREEN, WHITE, (int(self.x), int(self.y)), self.size)
        
        self.life -= 1

        # Warp-effekt:
        self.x, self.y = check_warp(self.x, self.y)