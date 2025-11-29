import pygame
from objetos import Raquete, Bola, Telha, ObjetosDefault
from random import randint
from util import renderSprites, Cores

class Jogo:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((960,720))
        self.clock = pygame.time.Clock()
        self.telhas = pygame.sprite.Group()

    def main(self, raquete, bola):
        while self.running:
            # fechar quando apertar o X
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.moverraquete(raquete)
            self.colidirbolacomparedes(bola)
            bola.colidirbolacomobjetos(bola, raquete, 1)
            self.colidirbolacomtelha(bola)

            renderSprites.listaSprites.update()
            self.screen.fill(Cores.BLACK)
            renderSprites.listaSprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def iniciarfase(self, raquete, bola):
        raquete.rect.x = 480
        raquete.rect.y = 600
        bola.rect.x = 480
        bola.rect.y = 500
        for i in range(randint(3,6)):
            self.criartelhas(60 + i * 60)
        self.running = True
        self.main(raquete, bola)

    def criartelhas(self, y):
        rand = randint(4,8)
        for i in range(rand):
            telha = Telha(Cores.WHITE, 90, 30)
            telha.rect.x = (480 - (rand * (telha.width + 20) / 2)) + i * (telha.width + 20)
            telha.rect.y = y
            self.telhas.add(telha)

    def moverraquete(self, player):
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_LEFT]:
            player.mover(-5)
        if tecla[pygame.K_RIGHT]:
            player.mover(5)

    def colidirbolacomparedes(self, bola):
        if bola.rect.x >= (int(self.screen.get_width()) - 15):
            bola.velocidade[0] = abs(bola.velocidade[0]) * -1
            print("parede direita")
        if bola.rect.x <= 0:
            bola.velocidade[0] = abs(bola.velocidade[0])
            print("parede esquerda")
        if bola.rect.y <= 0:
            bola.velocidade[1] = -bola.velocidade[1]
            print("parede cima")
        if bola.rect.y >= int(self.screen.get_height()):
            # melhorar em breve zzz
            print("morte")
            for telha in self.telhas:
                telha.kill()
            self.running = False
            jogo.iniciarfase(ObjetosDefault.raquete, ObjetosDefault.bola)
            

    def colidirbolacomtelha(self, bola):
        listacolisao = pygame.sprite.spritecollide(bola, self.telhas, False)
        for telha in listacolisao:
            bola.colidirbolacomobjetos(bola, telha, 0.5)
            telha.kill()
            print("colisão telha")

            

if __name__ == "__main__":
    jogo = Jogo()
    jogo.iniciarfase(ObjetosDefault.raquete, ObjetosDefault.bola)
