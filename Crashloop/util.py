import pygame
import os
path = os.path.split(os.path.abspath(__file__))[0]
assets = os.path.join(path, "assets")

class renderSprites():
    pygame.init()
    pygame.display.set_mode((960,720))
    listaSprites = pygame.sprite.Group()

    def carregarimagens(nome, width, height, colorkey=None):
        localimagem = os.path.join(assets, nome)
        imagem = pygame.image.load(localimagem)

        tamanho = imagem.get_size()
        tamanho = (tamanho[0] * (width / tamanho[0]), tamanho[1] * (height / tamanho[1]))
        imagem = pygame.transform.scale(imagem, tamanho)

        imagem = imagem.convert()
        if colorkey is not None:
            if colorkey == -1:
                colorkey = imagem.get_at((0,0))
            imagem.set_colorkey(colorkey, pygame.RLEACCEL)
        return imagem, imagem.get_rect()

class gameState():
    numTelhas = 0
    # maioria disso é salvo no main para ser utilizado em multiplas funções.
    gamestate = 0
    nivel = 0
    ultimonivel = 0
    raquete = ()
    bola = ()
    listaitems = [0,0,0]
    listacaixa = []
    telhamin = 0
    telhamax = 0
    quantmin = 0
    quantmax = 0
    quantidadedeItems = 0
    pontos = 0

class Cores():
    WHITE = (255,255,255)
    BLACK = (0,0,0)