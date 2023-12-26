import pygame
import random

class Debris:
    def __init__(self, x, y, dx, dy, life):
        self.x = x
        self.y = y
        self.dx = dx * 8
        self.dy = dy * 8
        self.life = life

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 3
        return self.life <= 0
    
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 1)


class ManageDebris:
    def __init__(self):

        self.debris = []

    def create_debris(self, x, y, num_debris):
        self.debris.append([Debris(x, y, random.uniform(-1, 1), random.uniform(-1, 1), random.randint(10, 20)) for _ in range(num_debris)])

    def update(self, screen):
        if len(self.debris) > 0:
            for d in self.debris:
                for dx in d:
                    dx.update()
                    dx.draw(screen)
                    if dx.life <= 0:
                        d.remove(dx)


