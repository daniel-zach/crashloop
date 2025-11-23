import pygame
import numpy as np
from objetos import Raquete, Bola
WHITE = (255,255,255)

# não sei onde botar isso então fica aqui fora mesmo
raquete = Raquete(WHITE, 100, 10)
raquete.rect.x = 350
raquete.rect.y = 560
bola = Bola(WHITE, 10, 10)
bola.rect.x = 345
bola.rect.y = 195

class Jogo:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000,600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.listaSprites = pygame.sprite.Group()

    def main(self):
        self.listaSprites.add(raquete)
        self.listaSprites.add(bola)
        while self.running:
            # fechar quando apertar o X
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.moverraquete(raquete)
            self.colidirbolacomparedes(bola)
            self.colidirbolacomobjetos(bola, raquete)

            self.listaSprites.update()
            self.screen.fill("black")
            self.listaSprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def moverraquete(self, player):
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_LEFT]:
            player.mover(-10)
        if tecla[pygame.K_RIGHT]:
            player.mover(10)

    def colidirbolacomparedes(self, bola):
        if bola.rect.x >= 985:
            bola.velocidade[0] = -bola.velocidade[0]
        if bola.rect.x <= 0:
            bola.velocidade[0] = -bola.velocidade[0]
        if bola.rect.y >= 600:
            bola.velocidade[1] = -bola.velocidade[1]
        if bola.rect.y < 0:
            bola.velocidade[1] = -bola.velocidade[1]

    def colidirbolacomobjetos(self, bola, raquete):
        if pygame.sprite.collide_mask(bola, raquete):
            centro = raquete.rect.x + (raquete.width / 2)
            bola.velocidade[0] = (bola.rect.x - centro) / 10
                
            bola.velocidade[1] = -bola.velocidade[1]
            print("colisão")

if __name__ == "__main__":
    jogo = Jogo()
    jogo.main()
