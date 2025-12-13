import pygame
import sys
from random import choice
from game_state import game_state
from game_objects import Raquete, Bola, Telha, Caixa
from sprite_manager import sprite_manager
from audio_manager import audio_manager
from ui_manager import UIManager
from level_manager import LevelManager
from item_manager import ItemManager
from upgrade_manager import UpgradeManager
from constants import *


class Jogo:
    """Classe principal que controla o loop"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Crashloop")
        self.clock = pygame.time.Clock()
        
        # Gerenciadores
        self.ui = UIManager(self.screen)
        self.level_manager = LevelManager()
        self.item_manager = ItemManager()
        self.upgrade_manager = UpgradeManager()

        audio_manager.iniciar_playlist()
        
        # Estado inicial
        self.running = True
        game_state.game_state = GameStates.PLAYING
        game_state.vidas = 0
        game_state.pontos = 0
        
        # Cor de fundo aleatória
        self.cor_fundo = choice(Colors.BACKGROUND_COLORS)

    def executar(self, raquete, bola, nivel):
        """
        Loop principal
        
        Args:
            raquete: Objeto da raquete
            bola: Objeto da bola
            nivel: Nível inicial
        """
        # Salvar referências no estado global
        game_state.nivel = nivel
        game_state.raquete = raquete
        game_state.bola = bola
        
        print(f"Nível {game_state.nivel}")
        
        while self.running:
            self._processar_eventos()
            
            if game_state.game_state == GameStates.PLAYING:
                self._atualizar_jogo(raquete, bola)
            
            self._renderizar()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

    def _processar_eventos(self):
        """Processa eventos do pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            audio_manager.processar_eventos_musica(event)

    def _atualizar_jogo(self, raquete, bola):
        """Atualiza a lógica do jogo"""
        self._mover_raquete(raquete)
        self._processar_colisoes_bola(bola)
        bola.bounce()
        bola.colidir_com_objeto(raquete, 1, 1)
        self._verificar_colisao_telhas(bola)
        self._processar_clones(raquete)
        self._verificar_conclusao_nivel()

    def _renderizar(self):
        """Renderiza todos os elementos na tela"""
        sprite_manager.sprite_group.update()

        self.screen.fill(self.cor_fundo)

        # Desenhar sprites
        sprite_manager.sprite_group.draw(self.screen)
        
        # Desenhar HUD
        self.ui.desenhar_hud(game_state.nivel, game_state.pontos, game_state.bola.combo, game_state.pontos_acumulados)
        
        # Desenhar stats no canto superior esquerdo
        stats = self.upgrade_manager.get_stats_texto()
        if stats:
            self.ui.desenhar_stats(stats)

        pygame.display.flip()

    def _mover_raquete(self, raquete):
        """Controla o movimento da raquete"""
        tecla = pygame.key.get_pressed()
        vel = RAQUETE_VEL_BASE + getattr(raquete, "vel_extra", 0)

        if any(tecla[k] for k in MOVE_LEFT_KEYS):
            raquete.mover(-vel)
        if any(tecla[k] for k in MOVE_RIGHT_KEYS):
            raquete.mover(vel)
        
        # Debug: pular nível
        if tecla[pygame.K_1]:
            self._reset_parcial(game_state.bola)
            self.level_manager.limpar_telhas()
            self.ui.tela_vitoria()
            self.ui.esperar_tecla()
            game_state.ultimo_nivel = game_state.nivel
            game_state.nivel += 1
            self._escolher_recompensa()

    def _processar_colisoes_bola(self, bola):
        """Processa colisões da bola com as paredes"""
        # Parede direita
        if bola.rect.x >= SCREEN_WIDTH - 15:
            bola.velocidade[0] = abs(bola.velocidade[0]) * -1
            audio_manager.tocar_sfx("sfx_hit")
        
        # Parede esquerda
        if bola.rect.x <= 0:
            bola.velocidade[0] = abs(bola.velocidade[0])
            audio_manager.tocar_sfx("sfx_hit")
        
        # Teto
        if bola.rect.y <= 0:
            bola.velocidade[1] = -bola.velocidade[1]
            audio_manager.tocar_sfx("sfx_hit")
        
        # Chão (perder bola)
        if bola.rect.y >= SCREEN_HEIGHT:
            self._perder_bola(bola)

    def _perder_bola(self, bola):
        """Processa a perda da bola"""
        if game_state.vidas > 0:
            # Tem vidas extras
            game_state.vidas -= 1
            self.item_manager.limpar_item_vida_se_zerar()
            self._reset_parcial(bola)
            self.proximo_nivel(game_state.raquete, game_state.bola, game_state.nivel)
        else:
            # Game over
            pontuacao = game_state.pontos
            nivel = game_state.ultimo_nivel
            self._reset_total(bola)
            self.item_manager.reset_itens()
            self.upgrade_manager.reset_upgrades()
            game_state.nivel = 1
            game_state.ultimo_nivel = 0
            
            self.ui.tela_derrota(pontuacao, nivel)
            self.ui.esperar_tecla()
            self.proximo_nivel(game_state.raquete, game_state.bola, game_state.nivel)

    def _reset_total(self, bola):
        """Reset completo"""
        self._limpar_sprites()
        self._destruir_clones()
        self.level_manager.limpar_telhas()
        bola.estado = 0
        self.running = False
        game_state.pontos = 0
        game_state.bola.combo = 0
        audio_manager.resetar_pitch_sfx("sfx_hit")

    def _reset_parcial(self, bola):
        """Reset parcial (só telhas)"""
        # Limpa as telhas através do level_manager
        self.level_manager.limpar_telhas()
        
        # Destruir todos os clones
        self._destruir_clones()
        
        # Resetar bola
        bola.estado = 0
        bola.velocidade = [0, 0]
        bola.rect.x = game_state.raquete.rect.x + (game_state.raquete.width / 2)
        bola.rect.y = game_state.raquete.rect.y - bola.height
        game_state.bola.combo = 0
        audio_manager.resetar_pitch_sfx("sfx_hit")
        
        print("Reset parcial realizado")

    def _destruir_clones(self):
        """Destrói todos os clones ativos"""
        from game_objects import BolaClone
        
        for sprite in list(sprite_manager.sprite_group):
            if isinstance(sprite, BolaClone):
                sprite.kill()

    def _limpar_sprites(self):
        """Remove telhas e itens da tela"""
        from game_objects import Telha, Item
        
        for sprite in list(sprite_manager.sprite_group):
            if isinstance(sprite, (Telha, Item)):
                sprite.kill()
        
        game_state.num_telhas = 0

    def _verificar_colisao_telhas(self, bola):
        """Verifica colisões da bola com telhas"""
        # Criar grupo temporário com as telhas do level_manager
        telhas_grupo = pygame.sprite.Group()
        for telha in self.level_manager.telhas[:]:  # Cópia da lista
            if telha.alive():  # Verifica se a telha ainda está viva
                telhas_grupo.add(telha)
        
        lista_colisao = pygame.sprite.spritecollide(bola, telhas_grupo, False)
        
        for telha in lista_colisao:
            if telha.alive():
                bola.colidir_com_objeto(telha, 1, 2)
                telha.tomar_dano(bola.dano)

    def _processar_clones(self, raquete):
        """Processa colisões e comportamento dos clones"""
        from game_objects import BolaClone
        
        # Encontrar todos os clones
        clones = [s for s in sprite_manager.sprite_group if isinstance(s, BolaClone)]
        
        for clone in clones:
            # Colisão com raquete
            clone.colidir_com_objeto(raquete, 1, 1)
            
            # Colisão com telhas
            telhas_grupo = pygame.sprite.Group()
            for telha in self.level_manager.telhas[:]:
                if telha.alive():
                    telhas_grupo.add(telha)
            
            lista_colisao = pygame.sprite.spritecollide(clone, telhas_grupo, False)
            
            for telha in lista_colisao:
                if telha.alive():
                    clone.colidir_com_objeto(telha, 1, 2)
                    telha.tomar_dano(clone.dano)

    def _verificar_conclusao_nivel(self):
        """Verifica se o nível foi concluído"""
        # Sincronizar contador com telhas vivas
        telhas_vivas = sum(1 for t in self.level_manager.telhas if t.alive())
        game_state.num_telhas = telhas_vivas
        
        if game_state.num_telhas <= 0:
            self._reset_parcial(game_state.bola)
            self.level_manager.limpar_telhas()
            
            self.ui.tela_vitoria()
            self.ui.esperar_tecla()
            
            game_state.ultimo_nivel = game_state.nivel
            game_state.nivel += 1
            
            # Menu de upgrades e itens
            self._escolher_recompensa()

    def _escolher_recompensa(self):
        """Permite ao jogador escolher uma recompensa (upgrade ou item)"""
        print("Gerando opções de recompensa...")
        opcoes = self.upgrade_manager.gerar_opcoes_recompensa(3)
        
        print("Exibindo menu de recompensa...")
        escolha_idx = self.ui.tela_recompensa(opcoes)
        
        # Processar escolha
        recompensa_escolhida = opcoes[escolha_idx]
        
        if recompensa_escolhida.tipo == "upgrade":
            # Aplicar upgrade diretamente
            self.upgrade_manager.processar_escolha(recompensa_escolhida)
            print(f"Upgrade aplicado: {recompensa_escolhida.nome}")
        else:
            # Spawnar item na tela
            item = self.upgrade_manager.processar_escolha(
                recompensa_escolhida, 
                spawn_x=SCREEN_WIDTH // 2 - ITEM_WIDTH // 2,
                spawn_y=400
            )
            print(f"Item spawnado: {recompensa_escolhida.nome}")
        
        # Aguardar um momento
        pygame.time.delay(300)
        
        # Continuar para o próximo nível
        self.proximo_nivel(game_state.raquete, game_state.bola, game_state.nivel)

    def proximo_nivel(self, raquete, bola, nivel):
        """Avança para o próximo nível"""
        if game_state.nivel != game_state.ultimo_nivel:
            # Novo nível - calcular parâmetros
            parametros = self.level_manager.calcular_parametros_nivel(nivel)
            self.iniciar_fase(raquete, bola, *parametros, nivel)
        else:
            # Repetir nível atual
            self.iniciar_fase(
                raquete, bola,
                game_state.telha_min, game_state.telha_max,
                game_state.quant_min, game_state.quant_max,
                nivel
            )

    def iniciar_fase(self, raquete, bola, telha_min, telha_max, 
                     quant_min, quant_max, nivel):
        """
        Inicia uma nova fase do jogo.
        
        Args:
            raquete: Objeto da raquete
            bola: Objeto da bola
            telha_min: Número mínimo de linhas de telhas
            telha_max: Número máximo de linhas de telhas
            quant_min: Quantidade mínima de telhas por linha
            quant_max: Quantidade máxima de telhas por linha
            nivel: Número do nível
        """
        self.level_manager.iniciar_fase(
            raquete, bola, telha_min, telha_max, 
            quant_min, quant_max, nivel
        )

        # Escolher nova cor de fundo
        self.cor_fundo = choice(Colors.BACKGROUND_COLORS)
        
        self.running = True
        self.executar(raquete, bola, nivel)


def inicializar_objetos():
    """Inicializa os objetos padrão do jogo"""
    bola = Bola()
    raquete = Raquete()
    
    # Criar caixas de itens
    for i in range(3):
        Caixa(location=i)
    
    return raquete, bola


if __name__ == "__main__":
    jogo = Jogo()
    jogo.ui.tela_inicio()
    jogo.ui.esperar_tecla()
    
    raquete, bola = inicializar_objetos()
    jogo.iniciar_fase(raquete, bola, 1, 2, 1, 4, 1)