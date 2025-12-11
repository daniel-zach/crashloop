"""
Objetos principais do jogo (Raquete, Bola, Telha, Item, Caixa).
"""
import pygame
import numpy as np
from random import randint, uniform
from sprite_manager import sprite_manager
from game_state import game_state
from constants import *
from audio_manager import audio_manager


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
        self.estado = 0
        self.max_velocidade = max_velocidade
        self.dano = dano
        self.combo = 0
        sprite_manager.sprite_group.add(self)

    def bounce(self):
        """Controla o movimento e lançamento da bola"""
        tecla = pygame.key.get_pressed()
        
        if self.estado == 1:
            self.rect.x += self.velocidade[0]
            self.rect.y += self.velocidade[1]
            self._limitar_velocidade()
        else:
            if tecla[pygame.K_SPACE]:
                self._lancar_direcao_aleatoria()
                self.estado = 1

    def _lancar_direcao_aleatoria(self):
        """Lança a bola em uma direção aleatória para cima"""
        angulo = uniform(60, 120)
        angulo_rad = np.radians(angulo)
        
        vel_x = self.max_velocidade * np.cos(angulo_rad)
        vel_y = -self.max_velocidade * np.sin(angulo_rad)
        
        self.velocidade = [vel_x, vel_y]

    def _limitar_velocidade(self):
        """Limita a velocidade da bola ao máximo permitido"""
        for i in range(2):
            if abs(self.velocidade[i]) >= self.max_velocidade:
                self.velocidade[i] = int(self.max_velocidade * np.sign(self.velocidade[i]))

    def colidir_com_objeto(self, obj, intensidade=1, tipo=1):
        """Verifica e trata colisão com objetos"""
        if not pygame.sprite.collide_mask(self, obj):
            return False
            
        if tipo == 1:
            # Colisão com raquete
            centro = obj.rect.x + (obj.width / 2)
            self.velocidade[0] = (self.rect.x - centro) / (10 / intensidade)
            self.velocidade[1] = -abs(self.velocidade[1]) # Colisão com raquete sempre fará o eixo Y ser negativo
            self.combo = 0
            game_state.pontos_acumulados = 0
            # Tocar som e resetar o pitch de hit
            audio_manager.tocar_sfx("sfx_hit_raquete")
            audio_manager.resetar_pitch_sfx("sfx_hit")
        elif tipo == 2:
            # Colisão com telha
            centro_bola = self.rect.centerx
            if centro_bola < obj.rect.left or centro_bola > obj.rect.right:
                self.velocidade[0] = -self.velocidade[0]
            else:
                self.velocidade[1] = -self.velocidade[1]

        return True


class BolaClone(pygame.sprite.Sprite):
    """Bola clone que não causa fim de nível ao cair"""
    
    def __init__(self, width=BOLA_WIDTH, height=BOLA_HEIGHT, 
                 max_velocidade=BOLA_VEL_MAX, dano=BOLA_DANO_INICIAL):
        super().__init__()
        self.image, self.rect = sprite_manager.carregar_imagem(
            "bola.png", width, height, -1
        )
        
        # Aplicar transparência (opacidade reduzida)
        self.image.set_alpha(150)  # 0-255, onde 255 é opaco
        
        self.width = width
        self.height = height
        self.velocidade = [0, 0]
        self.estado = 1  # Sempre em movimento
        self.max_velocidade = max_velocidade
        self.dano = dano
        sprite_manager.sprite_group.add(self)

    def update(self):
        """Atualiza a posição do clone"""
        if self.estado == 1:
            self.rect.x += self.velocidade[0]
            self.rect.y += self.velocidade[1]
            self._limitar_velocidade()
            self._verificar_colisoes_parede()
            self._verificar_morte()

    def _limitar_velocidade(self):
        """Limita a velocidade da bola ao máximo permitido"""
        for i in range(2):
            if abs(self.velocidade[i]) >= self.max_velocidade:
                self.velocidade[i] = int(self.max_velocidade * np.sign(self.velocidade[i]))

    def _verificar_colisoes_parede(self):
        """Verifica colisões com as paredes"""
        # Parede direita
        if self.rect.x >= SCREEN_WIDTH - 15:
            self.velocidade[0] = abs(self.velocidade[0]) * -1
            audio_manager.tocar_sfx("sfx_hit")
        
        # Parede esquerda
        if self.rect.x <= 0:
            self.velocidade[0] = abs(self.velocidade[0])
            audio_manager.tocar_sfx("sfx_hit")
        
        # Teto
        if self.rect.y <= 0:
            self.velocidade[1] = -self.velocidade[1]
            audio_manager.tocar_sfx("sfx_hit")

    def _verificar_morte(self):
        """Remove o clone se cair no chão"""
        if self.rect.y >= SCREEN_HEIGHT:
            print("Clone caiu e foi destruído")
            self.kill()

    def colidir_com_objeto(self, obj, intensidade=1, tipo=1):
        """Verifica e trata colisão com objetos"""
        if not pygame.sprite.collide_mask(self, obj):
            return False
            
        if tipo == 1:
            # Colisão com raquete
            centro = obj.rect.x + (obj.width / 2)
            self.velocidade[0] = (self.rect.x - centro) / (10 / intensidade)
            self.velocidade[1] = -abs(self.velocidade[1])
            audio_manager.tocar_sfx("sfx_hit_raquete")
        elif tipo == 2:
            # Colisão com telha
            centro_bola = self.rect.centerx
            if centro_bola < obj.rect.left or centro_bola > obj.rect.right:
                self.velocidade[0] = -self.velocidade[0]
            else:
                self.velocidade[1] = -self.velocidade[1]

        return True


class Telha(pygame.sprite.Sprite):
    """Telha que pode ser destruída pela bola"""
    
    def __init__(self, width=TELHA_WIDTH, height=TELHA_HEIGHT, level_manager=None, cor=None):
        super().__init__()
        self.image, self.rect = sprite_manager.carregar_imagem(
            "telha.png", width, height, -1
        )
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 28)
        self.level_manager = level_manager
        self.cor = cor if cor else Colors.WHITE
        
        if game_state.nivel == 1:
            self.vida = 1
        else:
            self.vida = randint(game_state.nivel, int(game_state.nivel * 1.25))
            
        sprite_manager.sprite_group.add(self)

    def update(self):
        """Atualiza a aparência da telha com o texto de vida"""
        self.image, _ = sprite_manager.carregar_imagem(
            "telha.png", self.width, self.height, -1
        )
        
        # Mudar cor da telha
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill(self.cor)
        self.image.blit(overlay, (0, 0), special_flags=pygame.BLEND_MULT)

        texto = self.font.render(str(self.vida), True, Colors.BLACK)
        x = (self.width - texto.get_width()) // 2
        y = (self.height - texto.get_height()) // 2
        self.image.blit(texto, (x, y))

    def tomar_dano(self, dano):
        """Causa dano à telha e adiciona pontos com combo"""
        game_state.bola.combo += 1
        dano_real = min(dano, self.vida)
        pontos_combo = int(dano_real * (game_state.bola.combo*0.25 + 1))
        
        game_state.pontos += pontos_combo
        if dano_real < pontos_combo:
            game_state.pontos_acumulados += pontos_combo - dano_real
        self.vida -= dano
        
        # Notificar itens explosivos sobre a colisão
        if hasattr(game_state.bola, 'itens_explosivos'):
            for item in game_state.bola.itens_explosivos:
                if hasattr(item, 'notificar_colisao_telha'):
                    item.notificar_colisao_telha(self)

        print(f"Dano: {dano}, Combo: {game_state.bola.combo}x, Pontos: +{pontos_combo}, Vida restante: {self.vida}")
        
        if self.vida <= 0:
            game_state.num_telhas -= 1
            audio_manager.tocar_sfx("sfx_quebra")
            if self.level_manager and self in self.level_manager.telhas:
                self.level_manager.telhas.remove(self)
            self.kill()
            print(f"Telha destruída! Telhas restantes: {game_state.num_telhas}") 
        else:
            audio_manager.tocar_sfx("sfx_hit")
        audio_manager.aumentar_pitch_sfx("sfx_hit", 0.1)


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
        self.limite = 1
        self.tipo_item = ItemTypes.PASSIVE
        self.font = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
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

            # Empilhar item do mesmo tipo (verificar limite)
            if isinstance(slot_item, self.__class__):
                if slot_item.stack < slot_item.limite:
                    slot_item.stack += 1
                    if hasattr(slot_item, "aplicar_efeito"):
                        slot_item.aplicar_efeito()
                    self.kill()
                else:
                    print(f"Limite de {slot_item.limite} stacks atingido!")
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
                self.stack -= 1
                self.desfazer_efeito()
            else:
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
        self.item()
        self._atualizar_display()

    def _atualizar_display(self):
        """Atualiza a aparência do item com informações"""
        self.image, _ = sprite_manager.carregar_imagem(
            f"{self.nome}.png", self.width, self.height, -1
        )
        
        if self.estado == ItemStates.SLOTTED:
            # Mostrar stack para passivos
            if self.tipo_item == ItemTypes.PASSIVE:
                texto = self.font.render(str(self.stack), True, Colors.WHITE)
                x = self.width - texto.get_width() - 4
                y = self.height - texto.get_height() - 4
                self.image.blit(texto, (x, y))
            
            # Mostrar cargas para ativos (se aplicável)
            elif self.tipo_item == ItemTypes.ACTIVE:
                if hasattr(self, "get_cargas_disponiveis"):
                    cargas = self.get_cargas_disponiveis()
                    total = self.stack
                    
                    # Texto de cargas
                    texto = self.font.render(f"{cargas}/{total}", True, Colors.GREEN if cargas > 0 else Colors.RED)
                    x = self.width - texto.get_width() - 4
                    y = self.height - texto.get_height() - 4
                    self.image.blit(texto, (x, y))
                    
                    # Mostrar menor cooldown se houver
                    if cargas < total and hasattr(self, "get_menor_cooldown"):
                        cd = self.get_menor_cooldown()
                        cd_segundos = cd / 60.0
                        texto_cd = self.font_small.render(f"{cd_segundos:.1f}s", True, Colors.YELLOW)
                        self.image.blit(texto_cd, (4, 4))


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