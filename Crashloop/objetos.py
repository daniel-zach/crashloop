import pygame
from random import randint
WHITE = (255,255,255)
BLACK = (0,0,0)

class Raquete(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.width = width
        self.height = height

        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

    def mover(self, pixels):
        self.rect.x += pixels
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > 900:
            self.rect.x = 900
        
class Bola(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        self.velocidade = [randint(2,4),randint(-6,8)]

        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocidade[0]
        self.rect.y += self.velocidade[1]

    def colidir(self):
        self.velocidade[0] = -self.velocidade[0]
        self.velocidade[1] = randint(-6,8)