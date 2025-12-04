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
        self.ui = UI(self.screen)
        self.running = True
        gameState.gamestate = 1
        gameState.vidas = 0

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
            # texto do nível
            nivel_surface = self.fonte.render(f"Nível: {gameState.nivel}", True, Cores.WHITE)
            self.screen.blit(nivel_surface, (10, 650))
            # texto dos pontos
            pontos_surface = self.fonte.render(f"{gameState.pontos}", True, Cores.WHITE)
            pontos_x = 960 - pontos_surface.get_width() - 10
            self.screen.blit(pontos_surface, (pontos_x, 650))

            renderSprites.listaSprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def iniciarfase(self, raquete, bola, telhamin, telhamax, quantmin, quantmax, nivel):
        # define a criação de uma fase
        # telhamin e telhamax define quantas linhas de telhas existe
        # quantmin e quantmax define quantas telhas existem por linha
        gameState.numTelhas = 0
        gameState.nivel = nivel
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
                quantmax = 2 + nivel
                quantmin = nivel
            else:
                telhamax = 7
                telhamin = (3 * nivel)%7
                quantmax = 8
                quantmin = 2 + nivel%6

            self.iniciarfase(raquete, bola, telhamin, telhamax, quantmin, quantmax, nivel)
        else:
            self.iniciarfase(raquete, bola, gameState.telhamin, gameState.telhamax, gameState.quantmin, gameState.quantmax, nivel)

    def reset_total(self, bola):
        # usado quando o jogador não tem vidas sobrando
        self.limpar_sprites()  # limpa telhas e itens
        self.telhas.empty()
        bola.estado = 0
        self.running = False
        gameState.pontos = 0

    def reset_parcial(self, bola):
        # limpa apenas as telhas
        for spr in list(renderSprites.listaSprites):
            if isinstance(spr, Telha):
                spr.kill()

        self.telhas.empty()
        gameState.numTelhas = 0

        # reseta apenas a bola para o estado inicial
        bola.estado = 0
        bola.velocidade = [0, 0]
        bola.rect.x = gameState.raquete.rect.x + (gameState.raquete.width / 2)
        bola.rect.y = gameState.raquete.rect.y - bola.height


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
        vel = 7 + getattr(player, "vel_extra", 0)

        if tecla[pygame.K_LEFT]:
            player.mover(-vel)
        if tecla[pygame.K_RIGHT]:
            player.mover(vel)
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
            # perdeu a bola
            if gameState.vidas > 0:
                gameState.vidas -= 1
                self.limpar_item_vida_se_zerar()
                self.reset_parcial(bola)
                self.proximonivel(gameState.raquete, gameState.bola, gameState.nivel)
                return

            # morreu SEM vidas extra
            self.reset_total(bola)
            self.reset_itens()
            gameState.nivel = 1
            gameState.ultimonivel = 0

            self.ui.tela_derrota()
            self.ui.esperar_tecla()
            self.proximonivel(gameState.raquete, gameState.bola, gameState.nivel)

    def limpar_sprites(self):
        # remove tudo exceto raquete, bola e caixas
        for spr in list(renderSprites.listaSprites):
            if isinstance(spr, Telha) or isinstance(spr, Item):
                spr.kill()
        gameState.numTelhas = 0

    def reset_itens(self):
        # limpa efeitos acumulados
        for item in gameState.listaitems:
            if item != 0:
                # desfaz todos os stacks
                for _ in range(item.stack):
                    if hasattr(item, "desfazerefeito"):
                        item.desfazerefeito()

        # limpa lista de itens
        for i in range(len(gameState.listaitems)):
            gameState.listaitems[i] = 0

        # resetar bônus da raquete
        if hasattr(gameState.raquete, "vel_extra"):
            gameState.raquete.vel_extra = 0

        # resetar vidas extras
        gameState.vidas = 0

    def limpar_itens_soltos(self):
        # remove somente itens que não estão nos slots
        slots = set(gameState.listaitems)

        for spr in list(renderSprites.listaSprites):
            if isinstance(spr, Item):
                if spr not in slots:
                    spr.kill()

    def limpar_item_vida_se_zerar(self):
        # percorre todos os slots
        for i, item in enumerate(gameState.listaitems):
            if item != 0 and isinstance(item, itens.ItemVida):
                if gameState.vidas == 0:
                    # desfaz todos os stacks restantes
                    for _ in range(item.stack):
                        item.desfazerefeito()

                    # remove do slot
                    gameState.listaitems[i] = 0

                    # remove sprite
                    item.kill()

    def concluirnivel(self):
        if gameState.numTelhas <= 0:
            self.reset_parcial(gameState.bola)
            self.telhas.empty()   # limpa lista de telhas

            self.ui.tela_vitoria()
            self.ui.esperar_tecla()

            gameState.ultimonivel = gameState.nivel
            gameState.nivel += 1

            self.escolheritems()

    def escolheritems(self):
        from itens import ItemDano, ItemVelRaquete, ItemVida
        classes = [ItemDano, ItemVelRaquete, ItemVida]

        for x in range(randint(1,3)):
            item_cls = classes[randint(0, 2)]
            item = item_cls()
            item.rect.x = 345 + x * (100)
            item.rect.y = 400

        self.proximonivel(gameState.raquete, gameState.bola, gameState.nivel)

    def colidirbolacomtelha(self, bola):
        listacolisao = pygame.sprite.spritecollide(bola, self.telhas, False)
        for telha in listacolisao:
            bola.colidirbolacomobjetos(bola, telha, 1, 2)
            telha.tomardano(bola.dano)

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 96)
        self.font_text  = pygame.font.Font(None, 48)

    def desenhar_texto(self, texto, y, fonte, cor=Cores.WHITE):
        surface = fonte.render(texto, True, cor)
        rect = surface.get_rect(center=(480, y))
        self.screen.blit(surface, rect)

    def tela_inicio(self):
        self.screen.fill(Cores.BLACK)
        self.desenhar_texto("CRASHLOOP", 200, self.font_title)
        self.desenhar_texto("Pressione ENTER para começar", 350, self.font_text)

        fonte_controles = pygame.font.Font(None, 30)
        self.desenhar_texto("Setas: mover", 480, fonte_controles)
        self.desenhar_texto("Mouse: arrastar itens", 520, fonte_controles)
        self.desenhar_texto("Botão direito: deletar item", 560, fonte_controles)
        pygame.display.flip()


    def tela_vitoria(self):
        self.screen.fill(Cores.BLACK)
        self.desenhar_texto("Fase concluída!", 250, self.font_title)
        self.desenhar_texto("Pressione ENTER para continuar", 400, self.font_text)
        pygame.display.flip()

    def tela_derrota(self):
        self.screen.fill(Cores.BLACK)
        self.desenhar_texto("Você perdeu!", 250, self.font_title)
        self.desenhar_texto("Pressione ENTER para tentar novamente", 400, self.font_text)
        pygame.display.flip()

    def esperar_tecla(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            tecla = pygame.key.get_pressed()
            if tecla[pygame.K_RETURN]:
                return


if __name__ == "__main__":
    jogo = Jogo()
    jogo.ui.tela_inicio()
    jogo.ui.esperar_tecla()
    jogo.iniciarfase(ObjetosDefault.raquete, ObjetosDefault.bola, 1, 2, 1, 4, 1)
