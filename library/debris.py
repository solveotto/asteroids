import pygame
import random
import time

class Debris:
    def __init__(self, x, y, dx, dy, life):
        """
        Initialize a Debris object.
        """
        self.x = x
        self.y = y
        self.dx = dx * 8
        self.dy = dy * 8
        self.life = life

    def update(self):
        """
        Update the position and life of the debris.

        Returns:
            bool: True if the debris's life is less than or equal to 0, False otherwise.
        """
        self.x += self.dx
        self.y += self.dy
        self.life -= 3
        return self.life <= 0
    
    def draw(self, screen):
        """
        Draw the debris on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the debris on.

        Returns:
            None
        """
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 1)


class ManageDebris:
    def __init__(self):
        """
        Initialize a ManageDebris object.
        """
        self.debris = []

    def create_debris(self, x, y, num_debris):
        """
        Create debris objects and add them to the debris list.

        Args:
            x (float): The x-coordinate of the debris.
            y (float): The y-coordinate of the debris.
            num_debris (int): The number of debris objects to create.
        """
        for _ in range(num_debris):
            self.debris.append(Debris(x, y, random.uniform(-1, 1), random.uniform(-1, 1), random.randint(10, 20)))

    def update(self, screen):
        """
        Update and draw the debris objects on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the debris on.
        """
        
        if len(self.debris) > 0:
            for d in self.debris:
                d.update()
                d.draw(screen)
                if d.life <= 0:
                    self.debris.remove(d)


