import pygame
from util import gameState
from objetos import Item

class itemlegal(Item):
    def __init__(self, width=70, height=70, nome="itemlegal"):
        super().__init__(width, height, nome)

    def item(self):
        if self.triggers < 1:
            gameState.bola.dano += 1
            self.triggers += 1
        else:
            return
        
    def desfazerefeito(self):
        gameState.bola.dano -= 1