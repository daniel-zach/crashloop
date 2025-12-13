"""
Gerenciamento de níveis e fases do jogo.
"""
import os
from random import randint, choice
from game_objects import Telha
from game_state import game_state
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, Colors


class LevelManager:
    """Gerenciador de níveis"""
    
    def __init__(self):
        self.telhas = []
        self.cores_usadas = []

    def criar_telhas(self, quant_min, quant_max, y):
        """
        Cria uma linha de telhas.
        
        Args:
            quant_min: Quantidade mínima de telhas
            quant_max: Quantidade máxima de telhas
            y: Posição vertical da linha
        """
        quantidade = randint(quant_min, quant_max)
        
        # Escolher uma cor para a linha
        cores_disponiveis = [cor for cor in Colors.TILE_COLORS if cor not in self.cores_usadas]

        # Se todas as cores já foram usadas resetar a lista
        if not cores_disponiveis:
            self.cores_usadas.clear()
            cores_disponiveis = Colors.TILE_COLORS.copy()

        cor_linha = choice(cores_disponiveis)
        self.cores_usadas.append(cor_linha)
        
        for i in range(quantidade):


            telha = Telha(level_manager=self, cor=cor_linha)  # Passa como argumento nomeado
            # Centralizar linha de telhas
            espacamento = 10
            largura_total = (quantidade * telha.width) + ((quantidade - 1) * espacamento)
            inicio_x = (SCREEN_WIDTH - largura_total) / 2
            telha.rect.x = inicio_x + i * (telha.width + 10)
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
        
        self.cores_usadas.clear()

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
        """Calcula os parâmetros de dificuldade para um nível"""
        if nivel <= 5:
            telha_max = 1 + nivel
            telha_min = max(2, nivel-1)
            quant_max = 2 + nivel
            quant_min = max(2, nivel)
        else:
            telha_max = min(nivel,9)
            telha_min = max(3, (3 * nivel) % 7)
            quant_max = 9
            quant_min = 2 + nivel % 6
            
        return telha_min, telha_max, quant_min, quant_max

    def limpar_telhas(self):
        """Remove todas as telhas da fase"""
        from game_objects import Telha
        from sprite_manager import sprite_manager
        
        # Limpar lista de telhas
        for telha in self.telhas[:]:  # Cópia da lista
            if telha.alive():
                telha.kill()
        
        self.telhas.clear()
        self.cores_usadas.clear()
        game_state.num_telhas = 0
        print("Todas as telhas foram limpas")