import pygame
import random
from circleshape import CircleShape
from constants import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen, color):
        pygame.draw.circle(screen, color, self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt
    
    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        random_angle = random.uniform(20, 50)
        
        a = self.velocity.rotate(random_angle)
        b = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = a * 1.2
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = b * 1.2


class HealPack(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.position = pygame.Vector2(x, y)
        self.size = 30
        self.thickness = 6
        self.color = (0, 255, 0)
        
    def draw(self, screen, color):
        vertical = pygame.Rect(self.position.x - self.thickness // 2, self.position.y - self.size // 2, self.thickness, self.size)

        horizontal = pygame.Rect(self.position.x - self.size // 2, self.position.y - self.thickness // 2, self.size, self.thickness)

        pygame.draw.rect(screen, self.color, vertical)
        pygame.draw.rect(screen, self.color, horizontal)
