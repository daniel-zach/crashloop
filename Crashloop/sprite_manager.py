"""
Módulo para gerenciar sprites e renderização.
"""
import pygame
import os

# Configuração de paths
path = os.path.split(os.path.abspath(__file__))[0]
assets = os.path.join(path, "assets")


class SpriteManager:
    """Gerenciador de sprites do jogo"""
    
    def __init__(self):
        pygame.init()
        self.sprite_group = pygame.sprite.Group()

    def carregar_imagem(self, nome, width, height, colorkey=None):
        """Carrega e redimensiona uma imagem"""
        local_imagem = os.path.join(assets, nome)
        imagem = pygame.image.load(local_imagem)

        # Redimensionar mantendo proporções
        tamanho_original = imagem.get_size()
        novo_tamanho = (
            tamanho_original[0] * (width / tamanho_original[0]),
            tamanho_original[1] * (height / tamanho_original[1])
        )
        imagem = pygame.transform.scale(imagem, novo_tamanho)

        imagem = imagem.convert()
        
        # Aplicar transparência se necessário
        if colorkey is not None:
            if colorkey == -1:
                colorkey = imagem.get_at((0, 0))
            imagem.set_colorkey(colorkey, pygame.RLEACCEL)
            
        return imagem, imagem.get_rect()

    def limpar_sprites(self, exceto_tipos=None):
        """
        Remove sprites do grupo.
        
        Args:
            exceto_tipos: Lista de tipos de sprites a serem mantidos
        """
        if exceto_tipos is None:
            exceto_tipos = []
            
        for sprite in list(self.sprite_group):
            if not any(isinstance(sprite, tipo) for tipo in exceto_tipos):
                sprite.kill()

    def limpar_tipo(self, tipo):
        """Remove todos os sprites de um tipo"""
        for sprite in list(self.sprite_group):
            if isinstance(sprite, tipo):
                sprite.kill()


# Instância global do gerenciador
sprite_manager = SpriteManager()
