"""
Implementação dos diferentes tipos de itens do jogo.
"""
from game_objects import Item
from game_state import game_state
from constants import ITEM_WIDTH, ITEM_HEIGHT


class ItemDano(Item):
    """Item que aumenta o dano da bola."""
    
    def __init__(self, width=ITEM_WIDTH, height=ITEM_HEIGHT, nome="item_dano"):
        super().__init__(width, height, nome)

    def aplicar_efeito(self):
        """Aumenta o dano da bola em 1 unidade."""
        game_state.bola.dano += 1

    def item(self):
        """Chamada inicial ao ser colocado no slot."""
        if self.triggers < 1:
            self.aplicar_efeito()
            self.triggers = 1

    def desfazer_efeito(self):
        """Remove 1 unidade de dano."""
        game_state.bola.dano -= 1


class ItemVelRaquete(Item):
    """Item que aumenta a velocidade da raquete."""
    
    def __init__(self, width=ITEM_WIDTH, height=ITEM_HEIGHT, nome="item_velraquete"):
        super().__init__(width, height, nome)
        self._vel_por_unidade = 1

    def aplicar_efeito(self):
        """Aumenta a velocidade da raquete em 1 unidade."""
        game_state.raquete.vel_extra = getattr(
            game_state.raquete, "vel_extra", 0
        ) + self._vel_por_unidade

    def item(self):
        """Chamada inicial ao ser colocado no slot."""
        if self.triggers < 1:
            self.aplicar_efeito()
            self.triggers = 1

    def desfazer_efeito(self):
        """Remove 1 unidade de velocidade."""
        game_state.raquete.vel_extra = max(
            0, 
            getattr(game_state.raquete, "vel_extra", 0) - self._vel_por_unidade
        )


class ItemVida(Item):
    """Item que concede uma vida extra."""
    
    def __init__(self, width=ITEM_WIDTH, height=ITEM_HEIGHT, nome="item_vida"):
        super().__init__(width, height, nome)

    def aplicar_efeito(self):
        """Adiciona 1 vida extra."""
        game_state.vidas = getattr(game_state, "vidas", 0) + 1

    def item(self):
        """Chamada inicial ao ser colocado no slot."""
        if self.triggers < 1:
            self.aplicar_efeito()
            self.triggers = 1

    def desfazer_efeito(self):
        """Remove 1 vida."""
        game_state.vidas = max(0, getattr(game_state, "vidas", 0) - 1)
