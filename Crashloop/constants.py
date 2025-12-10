"""
Constantes utilizadas no jogo.
"""

# Dimensões da tela
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 960

# FPS
FPS = 60

# Cores
class Colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    ORANGE = (255, 165, 0)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    GREEN = (0, 255, 0)
    GRAY = (82, 82, 82)
    BOX_PURPLE = (34, 32, 52)

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

# Tipos de itens
class ItemTypes:
    PASSIVE = "passivo"  # Efeito contínuo
    ACTIVE = "ativo"     # Ativado por tecla

# Velocidades
RAQUETE_VEL_BASE = 7
BOLA_VEL_MAX = 7
BOLA_DANO_INICIAL = 1
DASH_DISTANCE = 100

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
CAIXA_Y = SCREEN_HEIGHT - 120
CAIXA_START_X = 280
CAIXA_SPACING = 50

# Mapeamento de teclas para slots
import pygame
SLOT_KEYS = {
    0: pygame.K_j,  # Slot esquerdo
    1: pygame.K_k,  # Slot meio
    2: pygame.K_l   # Slot direito
}

SLOT_KEY_NAMES = {
    0: "J",
    1: "K",
    2: "L"
}