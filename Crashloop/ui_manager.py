"""
Gerenciamento da interface do usuário.
"""
import pygame
from constants import Colors


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
        self.desenhar_texto("CRASHLOOP", 200, self.font_title)
        self.desenhar_texto("Pressione ENTER para começar", 350, self.font_text)
        
        # Controles
        self.desenhar_texto("Setas: mover", 480, self.font_small)
        self.desenhar_texto("Mouse: arrastar itens", 520, self.font_small)
        self.desenhar_texto("Botão direito: deletar item", 560, self.font_small)
        
        pygame.display.flip()

    def tela_vitoria(self):
        """Exibe a tela de vitória de fase"""
        self.screen.fill(Colors.BLACK)
        self.desenhar_texto("Fase concluída!", 250, self.font_title)
        self.desenhar_texto("Pressione ENTER para continuar", 400, self.font_text)
        pygame.display.flip()

    def tela_derrota(self):
        """Exibe a tela de derrota"""
        self.screen.fill(Colors.BLACK)
        self.desenhar_texto("Você perdeu!", 250, self.font_title)
        self.desenhar_texto("Pressione ENTER para tentar novamente", 400, self.font_text)
        pygame.display.flip()

    def esperar_tecla(self):
        """Aguarda o jogador pressionar ENTER"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            tecla = pygame.key.get_pressed()
            if tecla[pygame.K_RETURN]:
                return

    def desenhar_hud(self, nivel, pontos):
        """Desenha o HUD do jogo"""
        fonte = pygame.font.Font(None, 64)
        
        # Texto do nível (canto inferior esquerdo)
        nivel_surface = fonte.render(f"Nível: {nivel}", True, Colors.WHITE)
        self.screen.blit(nivel_surface, (10, 650))
        
        # Texto dos pontos (canto inferior direito)
        pontos_surface = fonte.render(f"{pontos}", True, Colors.WHITE)
        pontos_x = self.screen.get_width() - pontos_surface.get_width() - 10
        self.screen.blit(pontos_surface, (pontos_x, 650))
