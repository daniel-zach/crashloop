"""
Gerenciamento da interface do usuário.
"""
import pygame
import sys
from constants import Colors, SLOT_KEY_NAMES, ItemTypes
from audio_manager import audio_manager


class UIManager:
    """Gerenciador de interface"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 96)
        self.font_text = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 30)

    def desenhar_texto(self, texto, y, fonte, cor=Colors.WHITE):
        """Desenha texto centralizado na tela"""
        surface = fonte.render(texto, True, cor)
        rect = surface.get_rect(center=(self.screen.get_width() // 2, y))
        self.screen.blit(surface, rect)

    def tela_inicio(self):
        """Exibe a tela inicial do jogo"""
        self.screen.fill(Colors.BLACK)
        self.desenhar_texto("CRASHLOOP", 300, self.font_title)
        self.desenhar_texto("Pressione ESPAÇO para começar", 450, self.font_text)
        
        self.desenhar_texto("Setas/A-D: mover", 580, self.font_small)
        self.desenhar_texto("Shift/Alt: modo de precisão", 610, self.font_small)
        self.desenhar_texto("Espaço: lançar bola", 640, self.font_small)
        self.desenhar_texto("Mouse: arrastar itens", 670, self.font_small)
        self.desenhar_texto("Botão direito: remover item", 700, self.font_small)
        
        pygame.display.flip()

    def tela_vitoria(self):
        """Exibe a tela de vitória de fase"""
        self.screen.fill(Colors.BLACK)
        self.desenhar_texto("Fase concluída!", 350, self.font_title)
        self.desenhar_texto("Pressione ESPAÇO para continuar", 500, self.font_text)
        pygame.display.flip()

    def tela_derrota(self, pontos=0, nivel=1):
        """Exibe a tela de derrota"""
        self.screen.fill(Colors.BLACK)
        self.desenhar_texto("Você perdeu a bola!", 300, self.font_title)
        self.desenhar_texto(f"Seu nível: {nivel}", 450, self.font_text)
        self.desenhar_texto(f"Sua pontuação: {pontos}", 500, self.font_text)
        self.desenhar_texto("Pressione ESPAÇO para tentar novamente", 600, self.font_text)
        pygame.display.flip()

    def esperar_tecla(self):
        """Aguarda o jogador pressionar ESPAÇO"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                audio_manager.processar_eventos_musica(event)

            tecla = pygame.key.get_pressed()
            if tecla[pygame.K_SPACE]:
                return

    def desenhar_hud(self, nivel, pontos, combo=0, pontos_acumulados=10):
        """Desenha o HUD do jogo"""
        fonte = pygame.font.Font(None, 64)
        fonte_combo = pygame.font.Font(None, 32)
        fonte_pontos_combo = pygame.font.Font(None, 36)
        
        nivel_surface = fonte.render(f"Nível: {nivel}", True, Colors.WHITE)
        nivel_y = self.screen.get_height() - 65
        self.screen.blit(nivel_surface, (10, nivel_y))
        
        pontos_surface = fonte.render(f"{pontos}", True, Colors.WHITE)
        pontos_x = self.screen.get_width() - pontos_surface.get_width() - 10
        pontos_y = self.screen.get_height() - 65
        self.screen.blit(pontos_surface, (pontos_x, pontos_y))

        if combo > 1:
            cor_combo = self._cor_combo(combo)
            
            if pontos_acumulados > 0:
                # Texto de pontos extras
                pontos_combo_texto = f"+{pontos_acumulados}"
                pontos_combo_surface = fonte_pontos_combo.render(pontos_combo_texto, True, cor_combo)
                # Rotacionar o texto
                pontos_combo_rotated = pygame.transform.rotate(pontos_combo_surface, 15)
                # Posicionar na esquerda do valor de pontos
                pontos_combo_x = pontos_x - pontos_combo_rotated.get_width() + 12
                pontos_combo_y = pontos_y - 20
                
                self.screen.blit(pontos_combo_rotated, (pontos_combo_x, pontos_combo_y))
            
            combo_surface = fonte_combo.render(f"COMBO x{combo}!", True, cor_combo)
            combo_x = self.screen.get_width() - combo_surface.get_width() - 20
            combo_y = self.screen.get_height() - 115
            self.screen.blit(combo_surface, (combo_x, combo_y))
        
        self.desenhar_teclas_slots()
    
    def _cor_combo(self, combo):
        """Retorna uma cor baseada no valor do combo"""
        if combo >= 12:
            return Colors.RED
        elif combo >= 7:
            return Colors.ORANGE
        elif combo >= 3:
            return Colors.YELLOW
        else:
            return Colors.WHITE
    
    def desenhar_stats(self, stats_lista):
        """Desenha os stats no canto superior esquerdo"""
        fonte = pygame.font.Font(None, 32)
        y_offset = 10
        
        for stat_texto in stats_lista:
            stat_surface = fonte.render(stat_texto, True, Colors.WHITE)
            self.screen.blit(stat_surface, (10, y_offset))
            y_offset += 35
    
    def desenhar_teclas_slots(self):
        """Desenha as teclas correspondentes aos slots na parte inferior"""
        from constants import CAIXA_START_X, CAIXA_WIDTH, CAIXA_SPACING, CAIXA_Y
        
        fonte_tecla = pygame.font.Font(None, 28)
        
        for slot_idx, tecla_nome in SLOT_KEY_NAMES.items():
            # Calcular posição X do slot
            x = CAIXA_START_X + slot_idx * (CAIXA_WIDTH + CAIXA_SPACING)
            # Centralizar a tecla embaixo
            x_centro = x + CAIXA_WIDTH // 2
            y = CAIXA_Y + CAIXA_WIDTH - 18
            
            # Desenhar fundo da tecla
            tecla_rect = pygame.Rect(x_centro -14, y, 28, 28)
            pygame.draw.rect(self.screen, Colors.GRAY, tecla_rect)
            pygame.draw.rect(self.screen, Colors.BOX_PURPLE, tecla_rect, 3)
            
            # Desenhar letra da tecla
            texto_surface = fonte_tecla.render(tecla_nome, True, Colors.WHITE)
            texto_rect = texto_surface.get_rect(center=tecla_rect.center)
            self.screen.blit(texto_surface, texto_rect)
    
    def tela_recompensa(self, opcoes_recompensa):
        """
        Exibe o menu de seleção de recompensas (upgrades + itens).
        
        Args:
            opcoes_recompensa: Lista de objetos Upgrade ou ItemRecompensa
            
        Returns:
            Índice da recompensa escolhida
        """
        from sprite_manager import sprite_manager
        
        escolha = None
        esperando_soltar = False
        
        while escolha is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            self.screen.fill(Colors.BLACK)
            
            # Título
            self.desenhar_texto("Escolha uma Recompensa", 100, self.font_title)
            
            # Desenhar opções
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]
            
            start_x = 100
            card_width = 220
            card_height = 350
            spacing = 50
            
            for i, recompensa in enumerate(opcoes_recompensa):
                x = start_x + i * (card_width + spacing)
                y = 350
                
                card_rect = pygame.Rect(x, y, card_width, card_height)
                
                # Highlight ao passar o mouse
                cor_borda = Colors.YELLOW if card_rect.collidepoint(mouse_pos) else Colors.WHITE
                
                # Cor diferente para itens
                if recompensa.tipo == "item":
                    cor_borda = Colors.ORANGE if card_rect.collidepoint(mouse_pos) else Colors.CYAN
                
                # Desenhar carta
                pygame.draw.rect(self.screen, Colors.BLACK, card_rect)
                pygame.draw.rect(self.screen, cor_borda, card_rect, 3)
                
                # Carregar e desenhar ícone
                try:
                    icone_image, icone_rect = sprite_manager.carregar_imagem(
                        f"{recompensa.icone}.png", 80, 80, -1
                    )
                    icone_x = x + (card_width - 80) // 2
                    icone_y = y + 20
                    self.screen.blit(icone_image, (icone_x, icone_y))
                except: # Placeholder se não encontrar a imagem
                    placeholder_rect = pygame.Rect(x + 60, y + 20, 80, 80)
                    pygame.draw.rect(self.screen, Colors.WHITE, placeholder_rect, 2)
                
                # Tipo de recompensa
                tipo_texto = "ITEM" if recompensa.tipo == "item" else "UPGRADE"
                tipo_surface = self.font_small.render(tipo_texto, True, Colors.ORANGE if recompensa.tipo == "item" else Colors.YELLOW)
                tipo_x = x + (card_width - tipo_surface.get_width()) // 2
                self.screen.blit(tipo_surface, (tipo_x, y + 110))
                
                # Nome
                nome_palavras = recompensa.nome.split()
                if len(nome_palavras) > 2:
                    linha1 = " ".join(nome_palavras[:2])
                    linha2 = " ".join(nome_palavras[2:])
                    
                    nome1_surface = self.font_small.render(linha1, True, Colors.WHITE)
                    nome1_x = x + (card_width - nome1_surface.get_width()) // 2
                    self.screen.blit(nome1_surface, (nome1_x, y + 135))
                    
                    nome2_surface = self.font_small.render(linha2, True, Colors.WHITE)
                    nome2_x = x + (card_width - nome2_surface.get_width()) // 2
                    self.screen.blit(nome2_surface, (nome2_x, y + 160))
                    
                    nivel_y = y + 185
                else:
                    nome_surface = self.font_small.render(recompensa.nome, True, Colors.WHITE)
                    nome_x = x + (card_width - nome_surface.get_width()) // 2
                    self.screen.blit(nome_surface, (nome_x, y + 140))
                    nivel_y = y + 170
                
                # Nível atual (só para upgrades)
                if recompensa.tipo == "upgrade":
                    nivel_texto = f"Nível: {recompensa.nivel}"
                    nivel_surface = self.font_small.render(nivel_texto, True, Colors.YELLOW)
                    nivel_x = x + (card_width - nivel_surface.get_width()) // 2
                    self.screen.blit(nivel_surface, (nivel_x, nivel_y))
                    desc_y = y + 205
                else:
                    desc_y = nivel_y
                
                # Descrição
                self._desenhar_texto_quebrado(
                    recompensa.descricao, 
                    x + 10, 
                    desc_y, 
                    card_width - 20, 
                    self.font_small, 
                    Colors.WHITE
                )
                
                # Detectar clique
                if card_rect.collidepoint(mouse_pos):
                    if mouse_pressed and not esperando_soltar:
                        escolha = i
                        esperando_soltar = True
            
            if not mouse_pressed:
                esperando_soltar = False
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)
        
        return escolha
    
    def _desenhar_texto_quebrado(self, texto, x, y, largura_max, fonte, cor):
        """Desenha texto com quebra de linha automática"""
        palavras = texto.split(' ')
        linhas = []
        linha_atual = []
        
        for palavra in palavras:
            teste_linha = ' '.join(linha_atual + [palavra])
            teste_surface = fonte.render(teste_linha, True, cor)
            
            if teste_surface.get_width() <= largura_max:
                linha_atual.append(palavra)
            else:
                if linha_atual:
                    linhas.append(' '.join(linha_atual))
                linha_atual = [palavra]
        
        if linha_atual:
            linhas.append(' '.join(linha_atual))
        
        for i, linha in enumerate(linhas):
            linha_surface = fonte.render(linha, True, cor)
            linha_x = x + (largura_max - linha_surface.get_width()) // 2
            self.screen.blit(linha_surface, (linha_x, y + i * 25))