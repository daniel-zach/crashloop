"""
Gerenciamento de áudio do jogo (música e efeitos sonoros).
"""
import pygame
import os
import numpy as np
import random

# Configuração de paths
path = os.path.split(os.path.abspath(__file__))[0]
audio_path = os.path.join(path, "assets/audio")
music_path = os.path.join(audio_path, "music")


class AudioManager:
    """Gerenciador de áudio do jogo"""
    
    def __init__(self):
        pygame.mixer.init()
        
        # Configurações de volume (0.0 a 1.0)
        self.volume_musica = 0.03
        self.volume_sfx = 0.5
        
        # Cache de efeitos sonoros carregados
        self.sfx_cache = {}

        self.sfx_pitch = 1

        # Cache de sons originais (sem o pitch shift)
        self.sfx_originais = {}
        
        # Sistema de playlist
        self.playlist = []
        self.playlist_index = 0
        self.playlist_ativa = False
        
        
        # Música atual tocando
        # Música atual tocando
        self.musica_atual = None
        self.musica_atual = None
        
        
        # Configurar evento de fim de música
        self.MUSIC_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.MUSIC_END)
        
        print("Audio Manager inicializado")
        print("Audio Manager inicializado")
        
        # Criar playlist automaticamente
        self._criar_playlist()
        # Música atual tocando
        self.musica_atual = None
        
        print("Audio Manager inicializado")
    
    def carregar_sfx(self, nome):
        """Carrega um efeito sonoro em cache"""
        if nome in self.sfx_cache:
            return self.sfx_cache[nome]
        
        # Tentar carregar com diferentes extensões
        extensoes = ['.wav', '.ogg', '.mp3']
        
        for ext in extensoes:
            caminho = os.path.join(audio_path, f"{nome}{ext}")
            if os.path.exists(caminho):
                try:
                    som = pygame.mixer.Sound(caminho)
                    som.set_volume(self.volume_sfx)
                    self.sfx_cache[nome] = som
                    self.sfx_originais[nome] = pygame.mixer.Sound(caminho)
                    self.sfx_originais[nome].set_volume(self.volume_sfx)
                    print(f"SFX carregado: {nome}{ext}")
                    return som
                except pygame.error as e:
                    print(f"Erro ao carregar {nome}{ext}: {e}")
        
        print(f"Aviso: SFX não encontrado: {nome}")
        return None
    
    def tocar_sfx(self, nome):
        """Toca um efeito sonoro"""
        som = self.carregar_sfx(nome)
        if som:
            som.play()
    
    def _criar_playlist(self):
        """
        Cria uma playlist com todas as músicas da pasta music.
        A ordem é randomizada.
        """
        if not os.path.exists(music_path):
            print(f"Aviso: Pasta de música não encontrada: {music_path}")
            return
        
        # Extensões de música suportadas
        extensoes = ['.mp3', '.ogg', '.wav']
        
        # Listar todos os arquivos de música
        musicas = []
        for arquivo in os.listdir(music_path):
            nome, ext = os.path.splitext(arquivo)
            if ext.lower() in extensoes:
                musicas.append(nome)
        
        if not musicas:
            print("Nenhuma música encontrada na pasta music/")
            return
        
        # Randomizar ordem
        random.shuffle(musicas)
        self.playlist = musicas
        
        print(f"Playlist criada com {len(self.playlist)} músicas: {', '.join(self.playlist)}")
    
    def iniciar_playlist(self):
        """
        Inicia a reprodução da playlist.
        As músicas tocam em sequência e depois se repetem.
        """
        if not self.playlist:
            print("Playlist vazia, não há músicas para tocar")
            return False
        
        self.playlist_ativa = True
        self.playlist_index = 0
        return self._tocar_musica_playlist()
    
    def _tocar_musica_playlist(self):
        """Toca a música atual da playlist"""
        if not self.playlist:
            return False
        
        nome_musica = self.playlist[self.playlist_index]
        sucesso = self.tocar_musica(nome_musica, loop=0)  # Tocar uma vez
        
        if sucesso:
            print(f"Tocando música {self.playlist_index + 1}/{len(self.playlist)}: {nome_musica}")
        
        return sucesso
    
    def proxima_musica_playlist(self):
        """Avança para a próxima música da playlist"""
        if not self.playlist_ativa or not self.playlist:
            return False
        
        self.playlist_index = (self.playlist_index + 1) % len(self.playlist)
        
        if self.playlist_index == 0:
            print("Playlist reiniciando do começo")
        
        return self._tocar_musica_playlist()
    
    def processar_eventos_musica(self, event):
        """Processa fim de música"""
        if event.type == self.MUSIC_END and self.playlist_ativa:
            self.proxima_musica_playlist()
            return True
        return False
    
    def parar_playlist(self):
        """Para a playlist"""
        self.playlist_ativa = False
        self.parar_musica()

    def tocar_musica(self, nome, loop=-1, fade_ms=0):
        """Toca uma música de fundo"""
        # Tentar carregar com diferentes extensões
        extensoes = ['.mp3', '.ogg', '.wav']
        
        for ext in extensoes:
            caminho = os.path.join(music_path, f"{nome}{ext}")
            if os.path.exists(caminho):
                try:
                    pygame.mixer.music.load(caminho)
                    pygame.mixer.music.set_volume(self.volume_musica)
                    
                    if fade_ms > 0:
                        pygame.mixer.music.play(loop, fade_ms=fade_ms)
                    else:
                        pygame.mixer.music.play(loop)
                    
                    self.musica_atual = nome
                    print(f"Música tocando: {nome}{ext}")
                    return True
                except pygame.error as e:
                    print(f"Erro ao carregar música {nome}{ext}: {e}")
        
        print(f"Aviso: Música não encontrada: {nome}")
        return False
    
    def parar_musica(self, fade_ms=500):
        """
        Para a música atual.
        
        Args:
            fade_ms: Tempo de fade out em milissegundos
        """
        if fade_ms > 0:
            pygame.mixer.music.fadeout(fade_ms)
        else:
            pygame.mixer.music.stop()
        
        self.musica_atual = None
    
    def pausar_musica(self):
        """Pausa a música atual"""
        pygame.mixer.music.pause()
    
    def despausar_musica(self):
        """Despausa a música"""
        pygame.mixer.music.unpause()
    
    def set_volume_musica(self, volume):
        """
        Define o volume da música.
        
        Args:
            volume: Valor entre 0.0 e 1.0
        """
        self.volume_musica = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume_musica)
    
    def set_volume_sfx(self, volume):
        """
        Define o volume dos efeitos sonoros.
        
        Args:
            volume: Valor entre 0.0 e 1.0
        """
        self.volume_sfx = max(0.0, min(1.0, volume))
        
        # Atualizar volume de todos os sons em cache
        for som in self.sfx_cache.values():
            som.set_volume(self.volume_sfx)

    def aumentar_pitch_sfx(self, nome, incremento=0.1):
        self.sfx_pitch += incremento
        novo_fator = self.sfx_pitch
        self.alterar_pitch_sfx(nome, novo_fator)

    def alterar_pitch_sfx(self, nome, fator=1.0, limite_max=4.0):
        """
        Aumenta o pitch de um efeito sonoro em cache.
        Modificado através da velocidade de reprodução.
        
        Args:
            nome: Nome do arquivo sem extensão
            fator: Multiplicador do pitch (1.0 = normal, 2.0 = uma oitava acima)
            limite_max: Limite máximo do pitch
        
        Returns:
            bool: True se o pitch foi alterado com sucesso
        """
        if nome not in self.sfx_originais:
            print(f"Aviso: SFX {nome} não encontrado nos originais")
            return False
        
        # Limitar o fator ao máximo permitido
        fator = min(fator, limite_max)
        fator = max(fator, 0.5)  # Mínimo de 0.5x (metade da velocidade)
        
        try:
            # Pegar o som original
            som_original = self.sfx_originais[nome]

            # Converter para array
            sound_array = pygame.sndarray.array(som_original)
            
            # Calcular novo tamanho baseado no fator de pitch
            novo_tamanho = int(len(sound_array) / fator)
            
            # Resample o áudio (interpolação linear simples)
            if sound_array.ndim == 1:  # Mono
                indices = np.linspace(0, len(sound_array) - 1, novo_tamanho)
                novo_array = np.interp(indices, np.arange(len(sound_array)), sound_array)
            else:  # Stereo
                indices = np.linspace(0, len(sound_array) - 1, novo_tamanho)
                novo_array = np.zeros((novo_tamanho, sound_array.shape[1]))
                for canal in range(sound_array.shape[1]):
                    novo_array[:, canal] = np.interp(
                        indices,
                        np.arange(len(sound_array)),
                        sound_array[:, canal]
                    )
            
            # Converter de volta para Sound
            novo_array = novo_array.astype(sound_array.dtype)
            novo_som = pygame.sndarray.make_sound(novo_array)
            novo_som.set_volume(self.volume_sfx)
            
            # Atualizar cache
            self.sfx_cache[nome] = novo_som
            
            return True
            
        except Exception as e:
            print(f"Erro ao modificar pitch de {nome}: {e}")
            return False
    
    def resetar_pitch_sfx(self, nome):
        """Reseta o pitch de um efeito sonoro para o original"""
        if nome not in self.sfx_originais:
            print(f"Aviso: SFX {nome} não encontrado nos originais")
            return False
        
        try:
            # Restaurar som original
            som_original = self.sfx_originais[nome]
            # Restaurar o pitch
            self.sfx_pitch = 1
            
            # Criar nova cópia para o cache
            import pygame.sndarray as sndarray
            sound_array = sndarray.array(som_original)
            novo_som = sndarray.make_sound(sound_array.copy())
            novo_som.set_volume(self.volume_sfx)
            
            self.sfx_cache[nome] = novo_som
            
            return True
            
        except Exception as e:
            print(f"Erro ao resetar pitch de {nome}: {e}")
            return False
    

    def limpar_cache(self):
        """Limpa o cache de efeitos sonoros"""
        self.sfx_cache.clear()
        self.sfx_originais.clear()
        print("Cache de áudio limpo")


# Instância global do gerenciador
audio_manager = AudioManager()