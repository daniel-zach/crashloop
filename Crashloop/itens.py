import pygame
from util import gameState
from objetos import Item

class ItemDano(Item):
    def __init__(self, width=70, height=70, nome="item_dano"):
        super().__init__(width, height, nome)

    def aplicar_efeito(self):
        # aplica UMA unidade de aumento de dano
        gameState.bola.dano += 1

    def item(self):
        # chamada inicial ao ser colocado no slot
        if self.triggers < 1:
            self.aplicar_efeito()
            self.triggers = 1

    def desfazerefeito(self):
        # remove UMA unidade de dano (chamada a cada remoção de stack)
        gameState.bola.dano -= 1


class ItemVelRaquete(Item):
    def __init__(self, width=70, height=70, nome="item_velraquete"):
        super().__init__(width, height, nome)
        self._vel_por_unidade = 1

    def aplicar_efeito(self):
        # aplica UMA unidade de velocidade extra
        gameState.raquete.vel_extra = getattr(gameState.raquete, "vel_extra", 0) + self._vel_por_unidade

    def item(self):
        if self.triggers < 1:
            self.aplicar_efeito()
            self.triggers = 1

    def desfazerefeito(self):
        # remove UMA unidade de velocidade extra
        gameState.raquete.vel_extra = getattr(gameState.raquete, "vel_extra", 0) - self._vel_por_unidade
        if gameState.raquete.vel_extra < 0:
            gameState.raquete.vel_extra = 0


class ItemVida(Item):
    def __init__(self, width=70, height=70, nome="item_vida"):
        super().__init__(width, height, nome)

    def aplicar_efeito(self):
        # adiciona UMA vida extra
        gameState.vidas = getattr(gameState, "vidas", 0) + 1

    def item(self):
        if self.triggers < 1:
            self.aplicar_efeito()
            self.triggers = 1

    def desfazerefeito(self):
        # remove UMA vida (chamada quando uma unidade é deletada)
        gameState.vidas = getattr(gameState, "vidas", 0) - 1
        if gameState.vidas < 0:
            gameState.vidas = 0