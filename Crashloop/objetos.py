import pygame
from random import randint
from util import renderSprites, Cores

class Raquete(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(Cores.BLACK)
        self.image.set_colorkey(Cores.BLACK)
        self.width = width
        self.height = height

        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        renderSprites.listaSprites.add(self)

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
        self.image.fill(Cores.BLACK)
        self.image.set_colorkey(Cores.BLACK)
        self.width = width
        self.height = height

        # refazer para ter velocidade maxima e ser menos aleatorio
        self.velocidade = [randint(2,4),randint(-6,8)]

        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        renderSprites.listaSprites.add(self)

    def update(self):
        self.rect.x += self.velocidade[0]
        self.rect.y += self.velocidade[1] 

    def colidirbolacomobjetos(self, bola, obj, intensidade):
        if pygame.sprite.collide_mask(bola, obj):
            centro = obj.rect.x + (obj.width / 2)
            bola.velocidade[0] = (bola.rect.x - centro) / (6 / intensidade)
                
            bola.velocidade[1] = -bola.velocidade[1]
            print("colisão")

class Telha(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(Cores.BLACK)
        self.image.set_colorkey(Cores.BLACK)
        self.width = width
        self.height = height
        renderSprites.listaSprites.add(self)

        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

class ObjetosDefault():
    bola = Bola(Cores.WHITE, 10, 10)
    raquete = Raquete(Cores.WHITE, 100, 10)
    telha = Telha(Cores.WHITE, 0, 0)