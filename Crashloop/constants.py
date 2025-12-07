"""
Constantes utilizadas no jogo.
"""

# Dimensões da tela
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

# FPS
FPS = 60

# Cores
class Colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

# Estados do jogo
class GameStates:
    MENU = 0
    PLAYING = 1
    PAUSED = 2

# Estados dos itens
class ItemStates:
    FREE = 0
    DRAGGING = 1
    SLOTTED = 2

# Velocidades
RAQUETE_VEL_BASE = 7
BOLA_VEL_MAX = 6
BOLA_DANO_INICIAL = 1

# Dimensões dos objetos
RAQUETE_WIDTH = 100
RAQUETE_HEIGHT = 10

BOLA_WIDTH = 10
BOLA_HEIGHT = 10

TELHA_WIDTH = 90
TELHA_HEIGHT = 30

ITEM_WIDTH = 70
ITEM_HEIGHT = 70

CAIXA_WIDTH = 100
CAIXA_HEIGHT = 100
CAIXA_Y = 600
CAIXA_START_X = 280
CAIXA_SPACING = 50
