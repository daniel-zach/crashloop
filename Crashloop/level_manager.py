"""
Gerenciamento de níveis e fases do jogo.
"""
from random import randint
from game_objects import Telha
from game_state import game_state
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class LevelManager:
    """Gerenciador de níveis"""
    
    def __init__(self):
        self.telhas = []

    def criar_telhas(self, quant_min, quant_max, y):
        """
        Cria uma linha de telhas.
        
        Args:
            quant_min: Quantidade mínima de telhas
            quant_max: Quantidade máxima de telhas
            y: Posição vertical da linha
        """
        quantidade = randint(quant_min, quant_max)
        
        for i in range(quantidade):
            telha = Telha(level_manager=self)  # Passa como argumento nomeado
            # Centralizar linha de telhas
            inicio_x = (SCREEN_WIDTH - (quantidade * (telha.width + 20))) / 2
            telha.rect.x = inicio_x + i * (telha.width + 20)
            telha.rect.y = y
            self.telhas.append(telha)
            game_state.num_telhas += 1

    def iniciar_fase(self, raquete, bola, telha_min, telha_max, quant_min, quant_max, nivel):
        """
        Inicializa uma nova fase.
        
        Args:
            raquete: Objeto da raquete
            bola: Objeto da bola
            telha_min: Número mínimo de linhas de telhas
            telha_max: Número máximo de linhas de telhas
            quant_min: Quantidade mínima de telhas por linha
            quant_max: Quantidade máxima de telhas por linha
            nivel: Número do nível
        """
        # Resetar contadores
        game_state.num_telhas = 0
        game_state.nivel = nivel
        
        # Posicionar raquete e bola
        raquete.rect.x = SCREEN_WIDTH // 2 - raquete.width // 2
        raquete.rect.y = SCREEN_HEIGHT - 250
        bola.rect.x = SCREEN_WIDTH // 2 - bola.width // 2
        bola.rect.y = SCREEN_HEIGHT - 300
        
        # Criar telhas
        self.telhas.clear()
        num_linhas = randint(telha_min, telha_max)
        for i in range(num_linhas):
            self.criar_telhas(quant_min, quant_max, 60 + i * 60)
        
        # Salvar parâmetros da fase
        game_state.ultimo_nivel = nivel
        game_state.telha_min = telha_min
        game_state.telha_max = telha_max
        game_state.quant_min = quant_min
        game_state.quant_max = quant_max

    def calcular_parametros_nivel(self, nivel):
        """
        Calcula os parâmetros de dificuldade para um nível.
        
        Args:
            nivel: Número do nível
            
        Returns:
            tuple: (telha_min, telha_max, quant_min, quant_max)
        """
        if nivel <= 5:
            telha_max = 2 + nivel
            telha_min = nivel
            quant_max = 2 + nivel
            quant_min = nivel
        else:
            telha_max = 7
            telha_min = (3 * nivel) % 7
            quant_max = 8
            quant_min = 2 + nivel % 6
            
        return telha_min, telha_max, quant_min, quant_max

    def limpar_telhas(self):
        """Remove todas as telhas da fase."""
        from game_objects import Telha
        from sprite_manager import sprite_manager
        
        # Limpar lista de telhas
        for telha in self.telhas[:]:  # Cópia da lista
            if telha.alive():
                telha.kill()
        
        self.telhas.clear()
        game_state.num_telhas = 0
        print("Todas as telhas foram limpas")