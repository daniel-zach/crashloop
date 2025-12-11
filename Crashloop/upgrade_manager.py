"""
Gerenciamento de upgrades e itens do jogador.
"""
from random import choice, random
from game_state import game_state


class Upgrade:
    """Classe base para upgrades"""
    
    def __init__(self, nome, descricao, icone):
        self.nome = nome
        self.descricao = descricao
        self.icone = icone
        self.nivel = 0
        self.tipo = "upgrade"
    
    def aplicar(self):
        """Aplica o upgrade (implementar nas subclasses)"""
        pass
    
    def get_info(self):
        """Retorna informações do upgrade"""
        return f"{self.nome} Nv.{self.nivel}"


class ItemRecompensa:
    """Representa uma recompensa de item (para ser spawnada)"""
    
    def __init__(self, item_class):
        self.item_class = item_class
        self.nome = item_class.CONFIG.nome
        self.descricao = item_class.CONFIG.descricao
        self.icone = item_class.CONFIG.icone
        self.tipo = "item"  # Identificador de tipo
        self.probabilidade = item_class.CONFIG.probabilidade
    
    def spawnar(self, x, y):
        """Cria uma instância do item na posição especificada"""
        item = self.item_class()
        item.rect.x = x
        item.rect.y = y
        return item


class UpgradeDano(Upgrade):
    """Upgrade que aumenta o dano da bola"""
    
    def __init__(self):
        super().__init__(
            "Dano da Bola",
            "+1 de dano por acerto",
            "item_dano"
        )
    
    def aplicar(self):
        """Aumenta o dano da bola em 1"""
        game_state.bola.dano += 1
        self.nivel += 1
        print(f"Dano da bola aumentado para {game_state.bola.dano}")


class UpgradeVelocidadeRaquete(Upgrade):
    """Upgrade que aumenta a velocidade da raquete"""
    
    def __init__(self):
        super().__init__(
            "Velocidade da Raquete",
            "+1 de velocidade",
            "item_velraquete"
        )
    
    def aplicar(self):
        """Aumenta a velocidade da raquete em 1"""
        game_state.raquete.vel_extra = getattr(
            game_state.raquete, "vel_extra", 0
        ) + 1
        self.nivel += 1
        print(f"Velocidade da raquete aumentada para {7 + game_state.raquete.vel_extra}")


class UpgradeManager:
    """Gerenciador de upgrades e recompensas do jogo"""
    
    def __init__(self):
        self.upgrades_disponiveis = {
            'dano': UpgradeDano(),
            'velocidade': UpgradeVelocidadeRaquete()
        }
        self.upgrades_ativos = []
        self.itens_recompensa = []
        
        self._registrar_itens()
    
    def _registrar_itens(self):
        """Registra os itens disponíveis como recompensas"""
        from items import ITENS_DISPONIVEIS
        
        for item_class in ITENS_DISPONIVEIS:
            self.itens_recompensa.append(ItemRecompensa(item_class))
    
    def gerar_opcoes_recompensa(self, quantidade=3):
        """
        Gera opções aleatórias de recompensa (upgrades + itens).
        Itens aparecem baseado em sua probabilidade.
        """
        opcoes = []
        todos_upgrades = list(self.upgrades_disponiveis.values())
        
        for _ in range(quantidade):
            # Sortear se será upgrade ou item
            if random() < 0.45:  # chance de ser item
                # Escolher item baseado em probabilidade
                itens_possiveis = []
                for item_reward in self.itens_recompensa:
                    if random() * 100 < item_reward.probabilidade:
                        itens_possiveis.append(item_reward)
                
                if itens_possiveis:
                    opcoes.append(choice(itens_possiveis))
                else:
                    # Se nenhum item passou, adicionar um upgrade
                    opcoes.append(choice(todos_upgrades))
            else:
                # Adicionar upgrade
                opcoes.append(choice(todos_upgrades))
        
        return opcoes
    
    def processar_escolha(self, recompensa, spawn_x=400, spawn_y=400):
        """
        Processa a escolha de uma recompensa.
        Se for upgrade, aplica diretamente.
        Se for item, spawna na tela.
        """
        if recompensa.tipo == "upgrade":
            self.aplicar_upgrade(recompensa)
        elif recompensa.tipo == "item":
            return recompensa.spawnar(spawn_x, spawn_y)
    
    def aplicar_upgrade(self, upgrade):
        """Aplica um upgrade escolhido"""
        upgrade.aplicar()
        
        if upgrade not in self.upgrades_ativos:
            self.upgrades_ativos.append(upgrade)
    
    def get_stats_texto(self):
        """Retorna texto formatado com os stats atuais"""
        stats = []
        
        for upgrade in self.upgrades_ativos:
            if upgrade.nivel > 0:
                stats.append(upgrade.get_info())
        
        return stats
    
    def reset_upgrades(self):
        """Reseta todos os upgrades"""
        for upgrade in self.upgrades_disponiveis.values():
            upgrade.nivel = 0
        
        self.upgrades_ativos.clear()
        
        if hasattr(game_state.raquete, "vel_extra"):
            game_state.raquete.vel_extra = 0
        
        if hasattr(game_state.bola, "dano"):
            game_state.bola.dano = 1