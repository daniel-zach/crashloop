"""
Gerenciamento de itens e seus efeitos.
"""
from random import randint
from game_state import game_state
from game_objects import Item
from sprite_manager import sprite_manager


class ItemManager:
    """Gerenciador de itens do jogo"""
    
    def reset_itens(self):
        """Reseta todos os itens e seus efeitos"""
        # Desfazer efeitos acumulados
        for item in game_state.lista_items:
            if item != 0:
                # Desfaz todos os stacks
                for _ in range(item.stack):
                    if hasattr(item, "desfazer_efeito"):
                        item.desfazer_efeito()

        # Limpar lista de itens
        for i in range(len(game_state.lista_items)):
            game_state.lista_items[i] = 0

        # Resetar bônus da raquete
        if hasattr(game_state.raquete, "vel_extra"):
            game_state.raquete.vel_extra = 0

        # Resetar vidas extras
        game_state.vidas = 0

    def limpar_itens_soltos(self):
        """Remove itens que não estão nos slots"""
        slots = set(game_state.lista_items)
        
        for sprite in list(sprite_manager.sprite_group):
            if isinstance(sprite, Item):
                if sprite not in slots:
                    sprite.kill()

    def limpar_item_vida_se_zerar(self):
        """Remove itens de vida quando as vidas chegam a zero"""
        from items import ItemVida
        
        for i, item in enumerate(game_state.lista_items):
            if item != 0 and isinstance(item, ItemVida):
                if game_state.vidas == 0:
                    # Desfaz todos os stacks restantes
                    for _ in range(item.stack):
                        item.desfazer_efeito()

                    # Remove do slot
                    game_state.lista_items[i] = 0

                    # Remove sprite
                    item.kill()

    def gerar_itens_aleatorios(self, quantidade_min=1, quantidade_max=3):
        """Gera itens aleatórios após completar uma fase"""
        from items import ItemDano, ItemVelRaquete, ItemVida
        
        classes_itens = [ItemDano, ItemVelRaquete, ItemVida]
        quantidade = randint(quantidade_min, quantidade_max)
        
        for x in range(quantidade):
            item_cls = classes_itens[randint(0, len(classes_itens) - 1)]
            item = item_cls()
            item.rect.x = 345 + x * 100
            item.rect.y = 400
