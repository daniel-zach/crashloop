"""
Implementação dos diferentes tipos de itens do jogo.
"""
from game_objects import Item
from game_state import game_state
from constants import *
import pygame
import random


class ItemConfig:
    """Configurações base para itens"""
    def __init__(self, nome, icone, limite, probabilidade, descricao, tipo):
        self.nome = nome
        self.icone = icone
        self.limite = limite  # Limite de stacks
        self.probabilidade = probabilidade  # Chance de aparecer (0-100)
        self.descricao = descricao
        self.tipo = tipo  # ItemTypes.PASSIVE ou ItemTypes.ACTIVE


class ItemVida(Item):
    """Item que concede uma vida extra (PASSIVO)"""
    
    CONFIG = ItemConfig(
        nome="Vida Extra",
        icone="item_vida",
        limite=2,
        probabilidade=10,
        descricao="+1 vida",
        tipo=ItemTypes.PASSIVE
    )
    
    def __init__(self, width=ITEM_WIDTH, height=ITEM_HEIGHT):
        super().__init__(width, height, self.CONFIG.icone)
        self.limite = self.CONFIG.limite
        self.tipo_item = self.CONFIG.tipo

    def aplicar_efeito(self):
        """Adiciona 1 vida extra"""
        game_state.vidas = getattr(game_state, "vidas", 0) + 1
        print(f"Vida adicionada! Total: {game_state.vidas}")

    def item(self):
        """Método chamado a cada frame - passivos não precisam de lógica aqui"""
        pass

    def desfazer_efeito(self):
        """Remove 1 vida"""
        game_state.vidas = max(0, getattr(game_state, "vidas", 0) - 1)
        print(f"Vida removida! Total: {game_state.vidas}")


class ItemDash(Item):
    """Item que permite dash da raquete (ATIVO)"""
    
    CONFIG = ItemConfig(
        nome="Dash",
        icone="item_dash",
        limite=2,
        probabilidade=25,
        descricao="Dash rápido",
        tipo=ItemTypes.ACTIVE
    )
    
    def __init__(self, width=ITEM_WIDTH, height=ITEM_HEIGHT):
        super().__init__(width, height, self.CONFIG.icone)
        self.dash_distance = DASH_DISTANCE
        self.cooldown_max = 300  # Em FPS, 60 = 1 segundo
        self.input_buffer = 6
        self.limite = self.CONFIG.limite
        self.tipo_item = self.CONFIG.tipo
        
        # Sistema de múltiplos cooldowns (um por stack)
        self.cooldowns = []

        # Controle de input
        self.ultimo_input = 0
        self.tecla_pressionada_anterior = False

    def aplicar_efeito(self):
        """Adiciona uma nova carga de dash"""
        self.cooldowns.append(0)  # Nova carga disponível
        print(f"Carga de dash adicionada! Total de cargas: {len(self.cooldowns)}")

    def item(self):
        """Verifica se a tecla do slot foi pressionada para fazer dash"""
        if self.estado != ItemStates.SLOTTED:
            return
        
        # Atualizar todos os cooldowns
        for i in range(len(self.cooldowns)):
            if self.cooldowns[i] > 0:
                self.cooldowns[i] -= 1
        
        # Atualizar buffer
        if self.ultimo_input > 0:
            self.ultimo_input -= 1

        # Verificar se a tecla do slot foi pressionada
        tecla = pygame.key.get_pressed()
        tecla_slot = SLOT_KEYS.get(self.location)
        
        if tecla_slot:
            tecla_pressionada = tecla[tecla_slot]
            if tecla_pressionada and not self.tecla_pressionada_anterior:
                # Tecla acabou de ser pressionada
                if self.ultimo_input <= 0:
                    self._tentar_dash()
            self.tecla_pressionada_anterior = tecla_pressionada

    def _tentar_dash(self):
        """Tenta executar um dash se houver carga disponível"""
        for i in range(len(self.cooldowns)):
            if self.cooldowns[i] <= 0:
                self._executar_dash()
                self.cooldowns[i] = self.cooldown_max
                self.ultimo_input = self.input_buffer
                return
        
        # Nenhuma carga disponível
        print("Dash em cooldown!")

    def _executar_dash(self):
        """Executa o dash na direção do movimento"""
        if not game_state.raquete:
            return
        
        tecla = pygame.key.get_pressed()
        direcao = 0
        
        if tecla[pygame.K_LEFT]:
            direcao = -1
        elif tecla[pygame.K_RIGHT]:
            direcao = 1
        else:
            direcao = random.choice([-1, 1])
        
        # Distância fixa independente de stacks
        nova_pos = game_state.raquete.rect.x + (self.dash_distance * direcao)
        nova_pos = max(0, min(nova_pos, SCREEN_WIDTH - game_state.raquete.width))
        
        game_state.raquete.rect.x = nova_pos
        print(f"Dash executado! Distância: {self.dash_distance}px")

    def desfazer_efeito(self):
        """Remove uma carga de dash"""
        if self.cooldowns:
            self.cooldowns.pop()
            print(f"Carga de dash removida! Cargas restantes: {len(self.cooldowns)}")

    def get_cargas_disponiveis(self):
        """Retorna quantas cargas estão disponíveis (cooldown = 0)"""
        return sum(1 for cd in self.cooldowns if cd <= 0)

    def get_menor_cooldown(self):
        """Retorna o menor cooldown entre as cargas em recarga"""
        cooldowns_ativos = [cd for cd in self.cooldowns if cd > 0]
        return min(cooldowns_ativos) if cooldowns_ativos else 0


# Lista de todas as classes de itens disponíveis
ITENS_DISPONIVEIS = [ItemVida, ItemDash]