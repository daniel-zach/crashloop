"""
Módulo de gerenciamento do estado global do jogo.
"""

class GameState:
    """Classe para gerenciar o estado global do jogo"""
    
    def __init__(self):
        self.num_telhas = 0
        self.game_state = 0
        self.nivel = 0
        self.ultimo_nivel = 0
        self.raquete = None
        self.bola = None
        self.lista_items = [0, 0, 0]
        self.lista_caixa = []
        self.telha_min = 0
        self.telha_max = 0
        self.quant_min = 0
        self.quant_max = 0
        self.quantidade_items = 0
        self.pontos = 0
        self.pontos_acumulados = 0
        self.vidas = 0

    def reset_items(self):
        """Reseta os itens para o estado inicial"""
        self.lista_items = [0, 0, 0]
        self.lista_caixa = []

    def reset_nivel(self):
        """Reseta informações do nível"""
        self.num_telhas = 0

    def reset_completo(self):
        """Reseta todo o estado do jogo"""
        self.num_telhas = 0
        self.nivel = 1
        self.ultimo_nivel = 0
        self.pontos = 0
        self.pontos_acumulados = 0
        self.vidas = 0


# Instância global do estado do jogo
game_state = GameState()
