"""
Implementação dos diferentes tipos de itens do jogo.
"""
from game_objects import Item, Telha, BolaClone
from game_state import game_state
from constants import *
from audio_manager import audio_manager
from sprite_manager import sprite_manager
import pygame
import random
import math


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
        probabilidade=8,
        descricao="Permite continuar jogando se perder a bola",
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
        descricao="Um dash na direção do movimento",
        tipo=ItemTypes.ACTIVE
    )
    
    def __init__(self, width=ITEM_WIDTH, height=ITEM_HEIGHT):
        super().__init__(width, height, self.CONFIG.icone)
        self.dash_distance = DASH_DISTANCE
        self.cooldown_max = 450  # Em FPS, 60 = 1 segundo
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
        
        if any(tecla[k] for k in MOVE_LEFT_KEYS):
            direcao = -1
        if any(tecla[k] for k in MOVE_RIGHT_KEYS):
            direcao = 1
        else:
            direcao = random.choice([-1, 1])
        
        nova_pos = game_state.raquete.rect.x + (self.dash_distance * direcao)
        nova_pos = max(0, min(nova_pos, SCREEN_WIDTH - game_state.raquete.width))
        
        game_state.raquete.rect.x = nova_pos
        audio_manager.tocar_sfx("sfx_dash")
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


class ItemBolaExplosiva(Item):
    """Item que faz a bola causar dano em área (ATIVO)"""
    
    CONFIG = ItemConfig(
        nome="Bola Explosiva",
        icone="item_explosiva",
        limite=3,
        probabilidade=25,
        descricao="Próximo hit causa dano em área",
        tipo=ItemTypes.ACTIVE
    )
    
    def __init__(self, width=ITEM_WIDTH, height=ITEM_HEIGHT):
        super().__init__(width, height, self.CONFIG.icone)
        self.cooldown_max = 600  # x 60 FPS
        self.input_buffer = 6
        self.limite = self.CONFIG.limite
        self.tipo_item = self.CONFIG.tipo
        self.raio_explosao = 100  # Raio de dano em pixels
        
        # Sistema de múltiplos cooldowns (um por stack)
        self.cooldowns = []
        
        # Controle de input
        self.ultimo_input = 0
        self.tecla_pressionada_anterior = False
        
        # Estado da explosão
        self.explosao_pendente = False

    def aplicar_efeito(self):
        """Adiciona uma nova carga de explosão"""
        self.cooldowns.append(0)  # Nova carga disponível
        print(f"Carga de Bola Explosiva adicionada! Total de cargas: {len(self.cooldowns)}")

        # Registrar este item na bola para callback
        if not hasattr(game_state.bola, 'itens_explosivos'):
            game_state.bola.itens_explosivos = []
        if self not in game_state.bola.itens_explosivos:
            game_state.bola.itens_explosivos.append(self)
        

    def item(self):
        """Verifica se a tecla do slot foi pressionada para ativar"""
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
                    self._tentar_ativar()
            self.tecla_pressionada_anterior = tecla_pressionada

    def _tentar_ativar(self):
        """Tenta ativar uma carga de explosão se houver disponível"""
        # Impedir ativação ao mesmo tempo por outro item
        if hasattr(game_state.bola, 'explosao_ativa') and game_state.bola.explosao_ativa:
            return

        for i in range(len(self.cooldowns)):
            if self.cooldowns[i] <= 0 and self.get_cargas_disponiveis() > 0:
                self._ativar_explosao(i)
                return
        
        # Nenhuma carga disponível
        print("Bola Explosiva em cooldown!")

    def _ativar_explosao(self, indice_carga):
        """Ativa uma carga de explosão - próximo hit será explosivo"""
        # Marcar na bola que há uma explosão pendente
        if not hasattr(game_state.bola, 'explosao_ativa'):
            game_state.bola.explosao_ativa = False
        
        game_state.bola.explosao_ativa = True
        self.explosao_pendente = True

        self.cooldowns[indice_carga] = self.cooldown_max
        self.ultimo_input = self.input_buffer
        print("Bola Explosiva ativada! Próximo hit causará explosão!")

    def notificar_colisao_telha(self, telha_atingida):
            """Callback chamado quando a bola colide com uma telha"""
            if not self.explosao_pendente:
                return
            
            # Resetar flags
            self.explosao_pendente = False
            if hasattr(game_state.bola, 'explosao_ativa'):
                game_state.bola.explosao_ativa = False
            
            # Executar explosão usando a telha atingida como epicentro
            self._executar_explosao(telha_atingida)

    def _executar_explosao(self, telha_epicentro):
        """Executa o dano em área na telha atingida"""
        
        if not telha_epicentro or not telha_epicentro.alive():
            return
        
        # Posição do epicentro (telha atingida)
        epicentro_x = telha_epicentro.rect.centerx
        epicentro_y = telha_epicentro.rect.centery
        
        print(f"EXPLOSÃO em ({epicentro_x}, {epicentro_y})!")
        
        audio_manager.tocar_sfx("sfx_explosao")
        
        # Encontrar todas as telhas dentro do raio
        telhas_atingidas = []
        
        # Usar level_manager se disponível
        if hasattr(game_state, 'level_manager') and game_state.level_manager:
            telhas_para_verificar = game_state.level_manager.telhas
        else:
            # Fallback: buscar em todos os sprites
            telhas_para_verificar = [s for s in sprite_manager.sprite_group if isinstance(s, Telha)]
        
        for telha in telhas_para_verificar:
            if not telha.alive() or telha == telha_epicentro:
                continue
            
            # Calcular distância entre o epicentro e o centro da telha
            telha_x = telha.rect.centerx
            telha_y = telha.rect.centery
            
            distancia = math.sqrt((epicentro_x - telha_x)**2 + (epicentro_y - telha_y)**2)
            
            if distancia <= self.raio_explosao:
                telhas_atingidas.append(telha)
        
        # Aplicar dano a todas as telhas atingidas
        dano_explosao = game_state.bola.dano
        
        for telha in telhas_atingidas:
            if telha.alive():
                telha.tomar_dano(dano_explosao)
                print(f"  Telha em ({telha.rect.x}, {telha.rect.y}) atingida pela explosão!")
        
        print(f"Explosão atingiu {len(telhas_atingidas)} telhas!")

    def desfazer_efeito(self):
        """Remove uma carga de explosão"""
        if self.cooldowns:
            self.cooldowns.pop()
            if not self.cooldowns:
                if hasattr(game_state.bola, 'itens_explosivos') and self in game_state.bola.itens_explosivos:
                    game_state.bola.itens_explosivos.remove(self)


    def get_cargas_disponiveis(self):
        """Retorna quantas cargas estão disponíveis (cooldown = 0)"""
        return sum(1 for cd in self.cooldowns if cd <= 0) 

    def get_menor_cooldown(self):
        """Retorna o menor cooldown entre as cargas em recarga"""
        cooldowns_ativos = [cd for cd in self.cooldowns if cd > 0]
        return min(cooldowns_ativos) if cooldowns_ativos else 0


class ItemCameraLenta(Item):
    """Item que reduz a velocidade da bola temporariamente (ATIVO)"""
    
    CONFIG = ItemConfig(
        nome="Câmera Lenta",
        icone="item_camera_lenta",
        limite=1,
        probabilidade=20,
        descricao="Reduz velocidade da bola por alguns segundos",
        tipo=ItemTypes.ACTIVE
    )
    
    def __init__(self, width=ITEM_WIDTH, height=ITEM_HEIGHT):
        super().__init__(width, height, self.CONFIG.icone)
        self.cooldown_max = 1200  # 1 segundo x 60
        self.input_buffer = 6
        self.limite = self.CONFIG.limite
        self.tipo_item = self.CONFIG.tipo
        self.duracao_efeito = 150  # 2.5 segundos
        self.reducao_velocidade = 0.5  # Reduz para 50% da velocidade
        
        # Sistema de múltiplos cooldowns (um por stack)
        self.cooldowns = []
        
        # Controle de input
        self.ultimo_input = 0
        self.tecla_pressionada_anterior = False
        
        # Estado do efeito
        self.efeito_ativo = False
        self.tempo_restante = 0
        self.velocidade_original = None

    def aplicar_efeito(self):
        """Adiciona uma nova carga de câmera lenta"""
        self.cooldowns.append(0)  # Nova carga disponível
        print(f"Carga de Câmera Lenta adicionada! Total de cargas: {len(self.cooldowns)}")

    def item(self):
        """Verifica se a tecla do slot foi pressionada para ativar"""
        if self.estado != ItemStates.SLOTTED:
            return
        
        # Atualizar todos os cooldowns
        for i in range(len(self.cooldowns)):
            if self.cooldowns[i] > 0:
                self.cooldowns[i] -= 1
        
        # Atualizar buffer
        if self.ultimo_input > 0:
            self.ultimo_input -= 1

        # Atualizar efeito ativo
        if self.efeito_ativo:
            self.tempo_restante -= 1
            if self.tempo_restante <= 0:
                self._desativar_efeito()

        # Verificar se a tecla do slot foi pressionada
        tecla = pygame.key.get_pressed()
        tecla_slot = SLOT_KEYS.get(self.location)
        
        if tecla_slot:
            tecla_pressionada = tecla[tecla_slot]
            if tecla_pressionada and not self.tecla_pressionada_anterior:
                # Tecla acabou de ser pressionada
                if self.ultimo_input <= 0:
                    self._tentar_ativar()
            self.tecla_pressionada_anterior = tecla_pressionada

    def _tentar_ativar(self):
        """Tenta ativar uma carga de câmera lenta se houver disponível"""
        # Não ativar se já há um efeito ativo
        if self.efeito_ativo:
            print("Câmera Lenta já está ativa!")
            return

        for i in range(len(self.cooldowns)):
            if self.cooldowns[i] <= 0:
                self._ativar_efeito(i)
                return
        
        # Nenhuma carga disponível
        print("Câmera Lenta em cooldown!")

    def _ativar_efeito(self, indice_carga):
        """Ativa o efeito de câmera lenta"""
        if not game_state.bola:
            return
        
        # Salvar velocidade original
        self.velocidade_original = game_state.bola.velocidade.copy()
        
        # Reduzir velocidade
        game_state.bola.velocidade[0] *= self.reducao_velocidade
        game_state.bola.velocidade[1] *= self.reducao_velocidade
        
        # Ativar efeito
        self.efeito_ativo = True
        self.tempo_restante = self.duracao_efeito

        audio_manager.tocar_sfx("sfx_camera_lenta_on")
        
        # Iniciar cooldown
        self.cooldowns[indice_carga] = self.cooldown_max
        self.ultimo_input = self.input_buffer

        print(f"Câmera Lenta ativada! Velocidade reduzida para {self.reducao_velocidade*100}% por {self.duracao_efeito/60:.1f}s")

    def _desativar_efeito(self):
        """Desativa o efeito de câmera lenta"""
        if not game_state.bola or not self.velocidade_original:
            self.efeito_ativo = False
            return
        
        # Restaurar velocidade proporcional
        # Calcular o fator de aumento baseado na velocidade reduzida
        fator_restauracao = 1.0 / self.reducao_velocidade
        game_state.bola.velocidade[0] *= fator_restauracao
        game_state.bola.velocidade[1] *= fator_restauracao
        
        # Resetar estado
        self.efeito_ativo = False
        self.velocidade_original = None

        audio_manager.tocar_sfx("sfx_camera_lenta_off")
        
        print("Câmera Lenta desativada! Velocidade restaurada.")

    def desfazer_efeito(self):
        """Remove uma carga de câmera lenta"""
        # Se o efeito está ativo e é a última carga, desativar
        if self.efeito_ativo and len(self.cooldowns) == 1:
            self._desativar_efeito()
        
        if self.cooldowns:
            self.cooldowns.pop()
            print(f"Carga de Câmera Lenta removida! Cargas restantes: {len(self.cooldowns)}")

    def get_cargas_disponiveis(self):
        """Retorna quantas cargas estão disponíveis (cooldown = 0)"""
        if self.efeito_ativo:
            return 0  # Nenhuma carga disponível enquanto efeito está ativo
        return sum(1 for cd in self.cooldowns if cd <= 0)

    def get_menor_cooldown(self):
        """Retorna o menor cooldown entre as cargas em recarga"""
        cooldowns_ativos = [cd for cd in self.cooldowns if cd > 0]
        return min(cooldowns_ativos) if cooldowns_ativos else 0
    

class ItemCloneBola(Item):
    """Item que clona a bola (ATIVO)"""
    
    CONFIG = ItemConfig(
        nome="Clone",
        icone="item_clone_bola",
        limite=1,
        probabilidade=15,
        descricao="Cria um clone da bola",
        tipo=ItemTypes.ACTIVE
    )
    
    def __init__(self, width=ITEM_WIDTH, height=ITEM_HEIGHT):
        super().__init__(width, height, self.CONFIG.icone)
        self.cooldown_max = 900  # 15 segundos
        self.input_buffer = 6
        self.limite = self.CONFIG.limite
        self.tipo_item = self.CONFIG.tipo
        
        # Sistema de múltiplos cooldowns (um por stack)
        self.cooldowns = []
        
        # Controle de input
        self.ultimo_input = 0
        self.tecla_pressionada_anterior = False

    def aplicar_efeito(self):
        """Adiciona uma nova carga de clone"""
        self.cooldowns.append(0)  # Nova carga disponível
        print(f"Carga de Clone de Bola adicionada! Total de cargas: {len(self.cooldowns)}")

    def item(self):
        """Verifica se a tecla do slot foi pressionada para ativar"""
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
                    self._tentar_ativar()
            self.tecla_pressionada_anterior = tecla_pressionada

    def _tentar_ativar(self):
        """Tenta ativar uma carga de clone se houver disponível"""
        # Verificar se já existe um clone vivo
        if self._clone_existe():
            print("Clone de Bola: já existe um clone ativo!")
            return
        
        for i in range(len(self.cooldowns)):
            if self.cooldowns[i] <= 0:
                self._criar_clone(i)
                return
        
        # Nenhuma carga disponível
        print("Clone de Bola em cooldown!")

    def _clone_existe(self):
        """Verifica se já existe um clone vivo"""
        from game_objects import BolaClone
        
        for sprite in sprite_manager.sprite_group:
            if isinstance(sprite, BolaClone) and sprite.alive():
                return True
        return False

    def _criar_clone(self, indice_carga):
        """Cria um clone da bola"""
        if not game_state.bola or game_state.bola.estado != 1:
            print("Não é possível clonar: bola não está em movimento!")
            return
        
        # Criar bola clone
        clone = BolaClone(
            width=game_state.bola.width,
            height=game_state.bola.height,
            max_velocidade=game_state.bola.max_velocidade,
            dano=game_state.bola.dano
        )
        
        # Posicionar no mesmo lugar da bola original
        clone.rect.x = game_state.bola.rect.x
        clone.rect.y = game_state.bola.rect.y
        
        # Copiar velocidade com X invertido
        clone.velocidade = [-game_state.bola.velocidade[0], game_state.bola.velocidade[1]]
        clone.estado = 1
        
        audio_manager.tocar_sfx("sfx_clone_bola")
        
        # Iniciar cooldown
        self.cooldowns[indice_carga] = self.cooldown_max
        self.ultimo_input = self.input_buffer
        
        print(f"Clone de bola criado! Velocidade: {clone.velocidade}")

    def desfazer_efeito(self):
        """Remove uma carga de clone"""
        if self.cooldowns:
            self.cooldowns.pop()
            print(f"Carga de Clone de Bola removida! Cargas restantes: {len(self.cooldowns)}")

    def get_cargas_disponiveis(self):
        """Retorna quantas cargas estão disponíveis (cooldown = 0)"""
        # Se há um clone vivo, nenhuma carga disponível
        if self._clone_existe():
            return 0
        return sum(1 for cd in self.cooldowns if cd <= 0)

    def get_menor_cooldown(self):
        """Retorna o menor cooldown entre as cargas em recarga"""
        cooldowns_ativos = [cd for cd in self.cooldowns if cd > 0]
        return min(cooldowns_ativos) if cooldowns_ativos else 0

# Lista de todas as classes de itens disponíveis
ITENS_DISPONIVEIS = [ItemVida, ItemDash, ItemBolaExplosiva, ItemCameraLenta, ItemCloneBola]