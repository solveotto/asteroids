import math
import pygame

from library.utils import *


class Bullet():
    def __init__(self, x, y, dir) -> None:
        """
        Initialize a Bullet object.

        Args:
            x (float): The x-coordinate of the bullet's starting position.
            y (float): The y-coordinate of the bullet's starting position.
            dir (float): The direction in degrees in which the bullet will travel.
        """
        self.x = x
        self.y = y
        self.dir = dir
        self.size = 2
        self.speed = 15
        self.life = 25
    

    def update_bullet(self):
        """
        Update the position and appearance of the bullet.

        This method updates the position of the bullet based on its direction and speed.
        It also draws the bullet on the screen and decreases its life by 1.
        """
        self.x += self.speed * math.cos(self.dir * math.pi / 180)
        self.y += self.speed * math.sin(self.dir * math.pi / 180)
        
        pygame.draw.circle(SCREEN, WHITE, (int(self.x), int(self.y)), self.size)
        
        self.life -= 1

        # Warp-effekt:
        self.x, self.y = check_warp(self.x, self.y)