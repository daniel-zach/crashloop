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

    #def upgrade(self):
    #    rand = randint(0,2)
    #    match rand:
    #        case 0:
    #            print("Sem Upgrade")
    #            return
    #        case 1:
    #            self.dano += randint(1, int(gameState.nivel / 2))
    #            print("Upgrade Dano")
    #        case 2:
    #            self.maxvelocidade += randint(1, 2)
    #            print("Update Velocidade")
                    

class Telha(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image, self.rect = renderSprites.carregarimagens("telha.png", width, height, -1)
        self.width = width
        self.height = height
        if gameState.nivel == 1:
            self.vida = 1
        else:
            self.vida = randint(gameState.nivel, int(gameState.nivel * 1.5))

        renderSprites.listaSprites.add(self)

    def tomardano(self, dano):
        self.vida -= dano
        print(dano)
        if self.vida <= 0:
            gameState.numTelhas -= 1
            self.kill()

class Item(pygame.sprite.Sprite):
    def __init__(self, width, height, nome):
        super().__init__()
        self.image, self.rect = renderSprites.carregarimagens(str(nome + ".png"), width, height, -1)
        self.nome = nome
        self.width = width
        self.height = height
        self.estado = 0
        self.triggers = 0
        self.location = 0
        renderSprites.listaSprites.add(self)

    def moveritem(self):
        mousepos = pygame.mouse.get_pos()
        if self.estado == 1 or self.estado == 0:
            if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(mousepos):
                self.rect.x = (mousepos[0] - (self.width / 2))
                self.rect.y = (mousepos[1] - (self.height / 2))
                self.estado = 1
            else:
                self.estado = 0

    def detectarcaixa(self):
            for x in gameState.listacaixa:
                if pygame.sprite.collide_mask(self, x):
                    if self.estado == 0 and gameState.listaitems[x.location] == 0:
                        gameState.listaitems[x.location] = self
                        self.location = x.location
                        self.slotcaixa(x)
                        gameState.listaitems[x.location].item()


    def slotcaixa(self, caixa):
        self.estado = 2
        self.rect.x = caixa.rect.x + (caixa.width / 6)
        self.rect.y = caixa.rect.y + (caixa.height / 6)

    def deletarself(self):
        if self.estado == 2:
            mousepos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[2] and self.rect.collidepoint(mousepos):
                gameState.listaitems[self.location] = 0
                self.desfazerefeito()
                self.kill()

    def item(self):
        # essa função é utilizado no itens.py para definir a função de cada item.
        # roda a cada frame.
        pass

    def desfazerefeito(self):
        # essa função é utilizada para desfazer os efeitos da função de item.
        # roda quando é destruido o item.
        pass

    def update(self):
        self.moveritem()
        self.detectarcaixa()
        self.deletarself()
    
class Caixas(pygame.sprite.Sprite):
    def __init__(self, width, height, x):
        super().__init__()
        self.image, self.rect = renderSprites.carregarimagens("caixaitem.png", width, height, -1)
        self.width = width
        self.height = height
        self.rect.y = 600
        self.rect.x = 130 + x * (self.width + 50)
        self.location = x
        renderSprites.listaSprites.add(self)
        gameState.listacaixa.append(self)
        
class ObjetosDefault():
    bola = Bola(10, 10, 6, 1)
    raquete = Raquete(100, 10)
    caixa1 = Caixas(100, 100, 0)
    caixa2 = Caixas(100, 100, 1)
    caixa3 = Caixas(100, 100, 2)
    caixa4 = Caixas(100, 100, 3)
    caixa5 = Caixas(100, 100, 4)
