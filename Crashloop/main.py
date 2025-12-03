import pygame
from objetos import Telha, Item, ObjetosDefault
from random import randint
from util import renderSprites, Cores, gameState
import itens

class Jogo:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((960,720))
        self.caption = pygame.display.set_caption("Crashloop")
        self.clock = pygame.time.Clock()
        self.telhas = pygame.sprite.Group()
        self.fonte = pygame.font.Font(None, 64)
        gameState.gamestate = 1

    def main(self, raquete, bola, nivel):
        # salvar para o gamestate
        gameState.nivel = nivel
        gameState.raquete = raquete
        gameState.bola = bola
        print(gameState.nivel)
        while self.running:
            # fechar quando apertar o X
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            if gameState.gamestate == 1:
                self.moverraquete(raquete)
                self.colidirbolacomparedes(bola)
                bola.bounce(raquete)
                bola.colidirbolacomobjetos(bola, raquete, 1, 1)
                self.colidirbolacomtelha(bola)
                self.concluirnivel()

            renderSprites.listaSprites.update()
            self.screen.fill(Cores.BLACK)
            renderSprites.listaSprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def iniciarfase(self, raquete, bola, telhamin, telhamax, quantmin, quantmax, nivel):
        # define a criação de uma fase
        # telhamin e telhamax define quantas linhas de telhas existe
        # quantmin e quantmax define quantas telhas existem por linha
        raquete.rect.x = 480
        raquete.rect.y = 550
        bola.rect.x = 480
        bola.rect.y = 500
        for i in range(randint(telhamin,telhamax)):
            self.criartelhas(quantmin, quantmax, (60 + i * 60))
        # salvar dados para o gamestate
        gameState.ultimonivel = nivel
        gameState.telhamin = telhamin
        gameState.telhamax = telhamax
        gameState.quantmin = quantmin
        gameState.quantmax = quantmax
        self.running = True
        self.main(raquete, bola, nivel)

    def proximonivel(self, raquete, bola, nivel):
        # define as propriedades da fase dependendo do nivel
        if gameState.nivel != gameState.ultimonivel:
            if nivel <= 5:
                telhamax = 2 + nivel
                telhamin = nivel
            else:
                telhamax = 7
                telhamin = (3 * nivel)%7
            quantmax = 8
            quantmin = 2 + nivel%6
            self.iniciarfase(raquete, bola, telhamin, telhamax, quantmin, quantmax, nivel)
        else:
            self.iniciarfase(raquete, bola, gameState.telhamin, gameState.telhamax, gameState.quantmin, gameState.quantmax, nivel)

    def resetjogo(self, bola):
        for telha in self.telhas:
                telha.kill()
        gameState.numTelhas = 0
        self.telhas.empty()
        bola.estado = 0
        self.running = False

    def criartelhas(self, quantmin, quantmax, y):
        rand = randint(quantmin,quantmax)
        for i in range(rand):
            telha = Telha(90, 30)
            telha.rect.x = (480 - (rand * (telha.width + 20) / 2)) + i * (telha.width + 20)
            telha.rect.y = y
            self.telhas.add(telha)  
            gameState.numTelhas += 1

    def moverraquete(self, player):
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_LEFT]:
            player.mover(-7)
        if tecla[pygame.K_RIGHT]:
            player.mover(7)
        # para debug
        if tecla[pygame.K_1]:
            gameState.numTelhas = 0

    def colidirbolacomparedes(self, bola):
        if bola.rect.x >= (int(self.screen.get_width()) - 15):
            bola.velocidade[0] = abs(bola.velocidade[0]) * -1
        if bola.rect.x <= 0:
            bola.velocidade[0] = abs(bola.velocidade[0])
        if bola.rect.y <= 0:
            bola.velocidade[1] = -bola.velocidade[1]
        if bola.rect.y >= int(self.screen.get_height()):
            # melhorar em breve zzz
            self.resetjogo(bola)
            self.proximonivel(gameState.raquete, gameState.bola, gameState.nivel)

    def concluirnivel(self):
        if gameState.numTelhas <= 0:
            self.resetjogo(gameState.bola)
            gameState.ultimonivel = gameState.nivel
            gameState.nivel += 1
            self.resetjogo(gameState.bola)
            self.escolheritems()

    def escolheritems(self):
        for x in range(3):
            rand = randint(1,1)
            match rand:
                case 1:
                    item = itens.itemlegal()
                    item.rect.x = 200 * x
                    item.rect.y = 400
        self.proximonivel(gameState.raquete, gameState.bola, gameState.nivel)

    def colidirbolacomtelha(self, bola):
        listacolisao = pygame.sprite.spritecollide(bola, self.telhas, False)
        for telha in listacolisao:
            bola.colidirbolacomobjetos(bola, telha, 1, 2)
            telha.tomardano(bola.dano)

if __name__ == "__main__":
    jogo = Jogo()
    jogo.iniciarfase(ObjetosDefault.raquete, ObjetosDefault.bola, 1, 3, 2, 8, 1)
