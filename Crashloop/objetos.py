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
                    # colisão baseada no centro relativo
                    centro_bola = bola.rect.centerx
                    if centro_bola < obj.rect.left or centro_bola > obj.rect.right:
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
        self.font = pygame.font.Font(None, 28)
        if gameState.nivel == 1:
            self.vida = 1
        else:
            self.vida = randint(gameState.nivel, int(gameState.nivel * 1.25))

        renderSprites.listaSprites.add(self)

    def update(self):
        # recriar imagem original para não acumular textos antigos
        self.image, _ = renderSprites.carregarimagens("telha.png", self.width, self.height, -1)

        # texto da vida
        texto = self.font.render(str(self.vida), True, Cores.BLACK)

        # centralizar
        x = (self.width - texto.get_width()) // 2
        y = (self.height - texto.get_height()) // 2

        self.image.blit(texto, (x, y))


    def tomardano(self, dano):
        gameState.pontos += min(dano, self.vida)   # +1 ponto por dano causado
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
        self.stack = 0
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
        # só tenta encaixar se não estiver sendo arrastado (estado 0)
        if self.estado != 0:
            return

        for x in gameState.listacaixa:
            if pygame.sprite.collide_mask(self, x):
                slot_item = gameState.listaitems[x.location]

                # slot vazio → ocupa normalmente
                if slot_item == 0:
                    gameState.listaitems[x.location] = self
                    self.location = x.location
                    self.slotcaixa(x)
                    self.stack = 1
                    # aplica 1 vez o efeito (subclasses devem implementar aplicar_efeito)
                    # e sinaliza que já foi ativado
                    if hasattr(self, "aplicar_efeito"):
                        self.aplicar_efeito()
                    self.triggers = 1
                    return

                # slot com item do mesmo tipo → empilha
                if isinstance(slot_item, self.__class__):
                    # adiciona 1 ao stack do item que já está no slot
                    slot_item.stack += 1
                    # aplica mais 1 unidade de efeito ao item já no slot
                    if hasattr(slot_item, "aplicar_efeito"):
                        slot_item.aplicar_efeito()
                    # destrói o item "solto" que foi colocado (não precisa ficar no mundo)
                    self.kill()
                    return

    def slotcaixa(self, caixa):
        self.estado = 2
        self.rect.x = caixa.rect.x + (caixa.width / 6)
        self.rect.y = caixa.rect.y + (caixa.height / 6)

    def deletarself(self):
        if self.estado == 2:
            mousepos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[2] and self.rect.collidepoint(mousepos):
                if self.stack > 1:
                    # reduz 1 efeito e mantem item
                    self.stack -= 1
                    self.desfazerefeito()
                    return

                # se stack chegar a 0, remove item do slot e deleta
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

        # desenhar texto no canto inferior direito
        if not hasattr(self, "font"):
            self.font = pygame.font.Font(None, 24)

        valor = self.stack if self.estado == 2 else 0
        texto = self.font.render(str(valor), True, Cores.WHITE)

        x = self.width - texto.get_width() - 4
        y = self.height - texto.get_height() - 4

        # recriar imagem base para não sobrepor texto antigo
        self.image, _ = renderSprites.carregarimagens(str(self.nome + ".png"), self.width, self.height, -1)

        self.image.blit(texto, (x, y))

    
class Caixas(pygame.sprite.Sprite):
    def __init__(self, width, height, x):
        super().__init__()
        self.image, self.rect = renderSprites.carregarimagens("caixaitem.png", width, height, -1)
        self.width = width
        self.height = height
        self.rect.y = 600
        self.rect.x = 280 + x * (self.width + 50)
        self.location = x
        renderSprites.listaSprites.add(self)
        gameState.listacaixa.append(self)
        
class ObjetosDefault():
    bola = Bola(10, 10, 6, 1)
    raquete = Raquete(100, 10)
    caixa1 = Caixas(100, 100, 0)
    caixa2 = Caixas(100, 100, 1)
    caixa3 = Caixas(100, 100, 2)
