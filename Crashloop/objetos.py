import pygame
import numpy as np
from random import randint
from util import renderSprites, Cores, gameState

class Raquete(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image, self.rect = renderSprites.carregarimagens("raquete.png", width, height, -1)
        self.width = width
        self.height = height

        renderSprites.listaSprites.add(self)

    def mover(self, pixels):
        self.rect.x += pixels
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > 860:
            self.rect.x = 860
        
class Bola(pygame.sprite.Sprite):
    def __init__(self, width, height, maxvelocidade, dano):
        super().__init__()
        self.image, self.rect = renderSprites.carregarimagens("bola.png", width, height, -1)
        self.width = width
        self.height = height
        self.velocidade = 0
        self.estado = 0
        self.maxvelocidade = maxvelocidade
        self.dano = dano

        renderSprites.listaSprites.add(self)

    def bounce(self, raquete):
        # se o estado da bola estiver 1, ela pode mover normalmente
        # se não, ela está grudada na raquete.
        # é utilizado no começo de uma fase pra não ser injusto ao usuario
        tecla = pygame.key.get_pressed()
        if self.estado == 1:
            self.rect.x += self.velocidade[0]
            self.rect.y += self.velocidade[1]
            self.capvelocidade()
        else:
            self.rect.x = raquete.rect.x + (raquete.width / 2)
            self.rect.y = raquete.rect.y - self.height
            if tecla[pygame.K_SPACE]:
                self.velocidade = [0,self.maxvelocidade * -1]
                self.estado = 1

    def capvelocidade(self):
        if self.velocidade[0] >= self.maxvelocidade or self.velocidade[0] <= (self.maxvelocidade * -1):
            self.velocidade[0] = int(self.maxvelocidade * np.sign(self.velocidade[0]))
        if self.velocidade[1] >= self.maxvelocidade or self.velocidade[1] <= (self.maxvelocidade * -1):
            self.velocidade[1] = int(self.maxvelocidade * np.sign(self.velocidade[1]))

    def colidirbolacomobjetos(self, bola, obj, intensidade, tipo):
        if pygame.sprite.collide_mask(bola, obj):
            match tipo:
                case 1:
                    # usado mais para a raquete, não ficou muito bom com as telhas
                    centro = obj.rect.x + (obj.width / 2)
                    bola.velocidade[0] = (bola.rect.x - centro) / (10 / intensidade)
                    bola.velocidade[1] = -bola.velocidade[1]
                case 2:
                    ladodireito = obj.rect.x + obj.width
                    if bola.rect.x < obj.rect.x or bola.rect.x > (ladodireito - 5):
                        bola.velocidade[0] = -bola.velocidade[0]
                    else:
                        bola.velocidade[1] = -bola.velocidade[1]
                    

class Telha(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image, self.rect = renderSprites.carregarimagens("telha.png", width, height, -1)
        self.width = width
        self.height = height
        if gameState.nivel == 1:
            self.vida = 1
        else:
            self.vida = randint(gameState.nivel, gameState.nivel * 2)

        renderSprites.listaSprites.add(self)

    def tomardano(self, dano):
        self.vida -= dano
        if self.vida <= 0:
            gameState.numTelhas -= 1
            self.kill()

class ObjetosDefault():
    bola = Bola(10, 10, 6, 1)
    raquete = Raquete(100, 10)