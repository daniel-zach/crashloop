"""
Constantes utilizadas no jogo.
"""

# Dimensões da tela
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 930

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
    
    # Cores para telhas
    TILE_PURPLE = (113, 29, 176)
    TILE_MAGENTA = (194, 18, 146)
    TILE_RED = (239, 64, 64)
    TILE_GREEN = (65, 166, 126)
    TILE_YELLOW = (252, 199, 55)

    TILE_COLORS = [TILE_PURPLE, TILE_MAGENTA, TILE_RED, TILE_YELLOW, TILE_GREEN]
    
    # Cores de fundo
    DARK_GREEN = (15, 40, 25)
    DARK_PURPLE = (25, 15, 40)
    DARK_BLUE = (15, 25, 45)
    DARK_RED = (40, 15, 20)
    DARK_CYAN = (15, 35, 40)
    DARK_PINK = (40, 15, 30)
    
    BACKGROUND_COLORS = [DARK_GREEN, DARK_PURPLE, DARK_BLUE, DARK_RED, DARK_CYAN, DARK_PINK]

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

# Mapeamento de teclas para movimentação
MOVE_SLOW_KEYS = [
    pygame.K_LSHIFT,
    pygame.K_RSHIFT,
    pygame.K_SPACE,
    pygame.K_LALT,
    pygame.K_RALT
]

MOVE_LEFT_KEYS = [
    pygame.K_a,
    pygame.K_LEFT,
    pygame.K_KP_4
]

MOVE_RIGHT_KEYS = [
    pygame.K_d,
    pygame.K_RIGHT,
    pygame.K_KP_6
]