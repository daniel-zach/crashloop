"""
Objetos principais do jogo (Raquete, Bola, Telha, Item, Caixa).
"""
import pygame
import numpy as np
from random import randint
from sprite_manager import sprite_manager
from game_state import game_state
from constants import *


class Raquete(pygame.sprite.Sprite):
    """Raquete controlada pelo jogador"""
    
    def __init__(self, width=RAQUETE_WIDTH, height=RAQUETE_HEIGHT):
        super().__init__()
        self.image, self.rect = sprite_manager.carregar_imagem(
            "raquete.png", width, height, -1
        )
        self.width = width
        self.height = height
        self.vel_extra = 0
        sprite_manager.sprite_group.add(self)

    def mover(self, pixels):
        """Move a raquete horizontalmente."""
        self.rect.x += pixels
        # Limitar movimento às bordas da tela
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.width))


class Bola(pygame.sprite.Sprite):
    """Bola que quica pela tela"""
    
    def __init__(self, width=BOLA_WIDTH, height=BOLA_HEIGHT, 
                 max_velocidade=BOLA_VEL_MAX, dano=BOLA_DANO_INICIAL):
        super().__init__()
        self.image, self.rect = sprite_manager.carregar_imagem(
            "bola.png", width, height, -1
        )
        self.width = width
        self.height = height
        self.velocidade = [0, 0]
        self.estado = 0  # 0: grudada na raquete, 1: em movimento
        self.max_velocidade = max_velocidade
        self.dano = dano
        sprite_manager.sprite_group.add(self)

    def bounce(self, raquete):
        """Controla o movimento e lançamento da bola"""
        tecla = pygame.key.get_pressed()
        
        if self.estado == 1:
            # Bola em movimento
            self.rect.x += self.velocidade[0]
            self.rect.y += self.velocidade[1]
            self._limitar_velocidade()
        else:
            # Bola grudada na raquete
            self.rect.x = raquete.rect.x + (raquete.width / 2)
            self.rect.y = raquete.rect.y - self.height
            
            if tecla[pygame.K_SPACE]:
                self.velocidade = [0, -self.max_velocidade]
                self.estado = 1

    def _limitar_velocidade(self):
        """Limita a velocidade da bola ao máximo permitido"""
        for i in range(2):
            if abs(self.velocidade[i]) >= self.max_velocidade:
                self.velocidade[i] = int(self.max_velocidade * np.sign(self.velocidade[i]))

    def colidir_com_objeto(self, obj, intensidade=1, tipo=1):
        """
        Verifica e trata colisão com objetos.
        
        Args:
            obj: Objeto com o qual colidir
            intensidade: Intensidade da resposta
            tipo: Tipo de colisão (1: raquete, 2: telha)
        """
        if not pygame.sprite.collide_mask(self, obj):
            return False
            
        if tipo == 1:
            # Colisão com raquete - baseada na posição de impacto
            centro = obj.rect.x + (obj.width / 2)
            self.velocidade[0] = (self.rect.x - centro) / (10 / intensidade)
            self.velocidade[1] = -self.velocidade[1]
        elif tipo == 2:
            # Colisão com telha - baseada no lado do impacto
            centro_bola = self.rect.centerx
            if centro_bola < obj.rect.left or centro_bola > obj.rect.right:
                self.velocidade[0] = -self.velocidade[0]
            else:
                self.velocidade[1] = -self.velocidade[1]
                
        return True


class Telha(pygame.sprite.Sprite):
    """Telha que pode ser destruída pela bola"""
    
    def __init__(self, width=TELHA_WIDTH, height=TELHA_HEIGHT, level_manager=None):
        super().__init__()
        self.image, self.rect = sprite_manager.carregar_imagem(
            "telha.png", width, height, -1
        )
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 28)
        self.level_manager = level_manager
        
        # Vida baseada no nível
        if game_state.nivel == 1:
            self.vida = 1
        else:
            self.vida = randint(game_state.nivel, int(game_state.nivel * 1.25))
            
        sprite_manager.sprite_group.add(self)

    def update(self):
        """Atualiza a aparência da telha com o texto de vida"""
        # Recarregar imagem base
        self.image, _ = sprite_manager.carregar_imagem(
            "telha.png", self.width, self.height, -1
        )
        
        # Renderizar vida no centro
        texto = self.font.render(str(self.vida), True, Colors.BLACK)
        x = (self.width - texto.get_width()) // 2
        y = (self.height - texto.get_height()) // 2
        self.image.blit(texto, (x, y))

    def tomar_dano(self, dano):
        """Causa dano à telha"""
        # Adicionar pontos (limitado à vida restante)
        game_state.pontos += min(dano, self.vida)
        self.vida -= dano
        
        print(f"Dano: {dano}, Vida restante: {self.vida}")
        
        if self.vida <= 0:
            game_state.num_telhas -= 1
            # Remove da lista do level_manager se existir
            if self.level_manager and self in self.level_manager.telhas:
                self.level_manager.telhas.remove(self)
            self.kill()
            print(f"Telha destruída! Telhas restantes: {game_state.num_telhas}")


class Item(pygame.sprite.Sprite):
    """Classe base para itens coletáveis"""
    
    def __init__(self, width=ITEM_WIDTH, height=ITEM_HEIGHT, nome="item"):
        super().__init__()
        self.image, self.rect = sprite_manager.carregar_imagem(
            f"{nome}.png", width, height, -1
        )
        self.nome = nome
        self.width = width
        self.height = height
        self.estado = ItemStates.FREE
        self.triggers = 0
        self.location = 0
        self.stack = 0
        self.font = pygame.font.Font(None, 24)
        sprite_manager.sprite_group.add(self)

    def mover_item(self):
        """Permite arrastar o item"""
        mouse_pos = pygame.mouse.get_pos()
        
        if self.estado in [ItemStates.FREE, ItemStates.DRAGGING]:
            if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(mouse_pos):
                self.rect.x = mouse_pos[0] - (self.width / 2)
                self.rect.y = mouse_pos[1] - (self.height / 2)
                self.estado = ItemStates.DRAGGING
            else:
                self.estado = ItemStates.FREE

    def detectar_caixa(self):
        """Detecta se o item foi solto em uma caixa"""
        if self.estado != ItemStates.FREE:
            return

        for caixa in game_state.lista_caixa:
            if not pygame.sprite.collide_mask(self, caixa):
                continue
                
            slot_item = game_state.lista_items[caixa.location]

            # Slot vazio
            if slot_item == 0:
                game_state.lista_items[caixa.location] = self
                self.location = caixa.location
                self._posicionar_na_caixa(caixa)
                self.stack = 1
                
                if hasattr(self, "aplicar_efeito"):
                    self.aplicar_efeito()
                self.triggers = 1
                return

            # Empilhar item do mesmo tipo
            if isinstance(slot_item, self.__class__):
                slot_item.stack += 1
                if hasattr(slot_item, "aplicar_efeito"):
                    slot_item.aplicar_efeito()
                self.kill()
                return

    def _posicionar_na_caixa(self, caixa):
        """Posiciona o item dentro da caixa"""
        self.estado = ItemStates.SLOTTED
        self.rect.x = caixa.rect.x + (caixa.width / 6)
        self.rect.y = caixa.rect.y + (caixa.height / 6)

    def deletar_self(self):
        """Permite remover o item com botão direito do mouse"""
        if self.estado != ItemStates.SLOTTED:
            return
            
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[2] and self.rect.collidepoint(mouse_pos):
            if self.stack > 1:
                # Reduzir stack
                self.stack -= 1
                self.desfazer_efeito()
            else:
                # Remover item completamente
                game_state.lista_items[self.location] = 0
                self.desfazer_efeito()
                self.kill()

    def item(self):
        """Função executada a cada frame (override em subclasses)"""
        pass

    def desfazer_efeito(self):
        """Desfaz o efeito do item (override em subclasses)"""
        pass

    def update(self):
        """Atualiza o estado do item"""
        self.mover_item()
        self.detectar_caixa()
        self.deletar_self()
        self._atualizar_display_stack()

    def _atualizar_display_stack(self):
        """Atualiza o número de stacks exibido"""
        # Recarregar imagem base
        self.image, _ = sprite_manager.carregar_imagem(
            f"{self.nome}.png", self.width, self.height, -1
        )
        
        # Mostrar stack apenas se estiver em uma caixa
        valor = self.stack if self.estado == ItemStates.SLOTTED else 0
        texto = self.font.render(str(valor), True, Colors.WHITE)
        
        x = self.width - texto.get_width() - 4
        y = self.height - texto.get_height() - 4
        self.image.blit(texto, (x, y))


class Caixa(pygame.sprite.Sprite):
    """Caixa para armazenar itens"""
    
    def __init__(self, width=CAIXA_WIDTH, height=CAIXA_HEIGHT, location=0):
        super().__init__()
        self.image, self.rect = sprite_manager.carregar_imagem(
            "caixaitem.png", width, height, -1
        )
        self.width = width
        self.height = height
        self.rect.y = CAIXA_Y
        self.rect.x = CAIXA_START_X + location * (width + CAIXA_SPACING)
        self.location = location
        
        sprite_manager.sprite_group.add(self)
        game_state.lista_caixa.append(self)