import pygame, sys, os, jogo
import telas.inicio, telas.opcoes, telas.pause_em_jogo, telas.selecao, telas.padrao
from typing import List

# TODO: Estilizar

class GerenciadorTelas:
    def __init__(self, largura, altura, cor):
        self.largura_padrao = largura
        self.largura = self.largura_padrao
        self.altura_padrao = altura
        self.altura = self.altura_padrao
        self.cor = cor
        self.volume_efeitos = 0
        self.display = pygame.display.set_mode((self.largura, self.altura), pygame.RESIZABLE)
        self.musica = pygame.mixer.Sound("../assets/musica_menu.mp3")
        self.musica.set_volume(0)
        self.musica_volume = self.musica.get_volume()
        self.tela = telas.inicio.tela(self.largura, self.altura, self.cor, self.musica_volume, self.volume_efeitos, "fundo_inicio.png", self.display, self.interagir)
        self.tela_pause = telas.pause_em_jogo.tela(self.largura, self.altura, self.cor, self.musica_volume, self.volume_efeitos, self.display, self.interagir)
        self.rodando = True
        self.pausado = False
        self.estado = 'inicio'
        self.relogio = pygame.time.Clock()
    
    def run(self):
        pygame.mixer.Sound.play(self.musica, -1)
        tempo_press = pygame.time.get_ticks()
        while (self.rodando):
            if (self.estado in ['inicio', 'opcoes', 'selecao']):
                eventos: List[pygame.event.Event] = pygame.event.get()
                for evento in eventos:
                    self.tela.checar_eventos(evento)
                    if (evento.type == pygame.QUIT):
                        pygame.quit()
                        sys.exit()
                            
                teclas_pressionadas = pygame.key.get_pressed()

                if teclas_pressionadas[pygame.K_ESCAPE]:
                    if (pygame.time.get_ticks() - tempo_press) > 300:
                        if (self.estado == 'inicio'):
                            pygame.quit()
                            sys.exit()
                        else:
                            tempo_press = pygame.time.get_ticks()
                            self.estado = 'inicio'
                            self.tela = telas.inicio.tela(self.largura, self.altura, self.cor, self.musica_volume, self.volume_efeitos, "fundo_inicio.png", self.display, self.interagir)
                if teclas_pressionadas[pygame.K_F11]:
                    if (pygame.time.get_ticks() - tempo_press) > 300:
                        if pygame.display.is_fullscreen():
                            pygame.display.toggle_fullscreen()
                            self.display = pygame.display.set_mode((self.largura_padrao, self.altura_padrao), pygame.RESIZABLE)
                        else:
                            self.display = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0])
                            pygame.display.toggle_fullscreen()
                        tempo_press = pygame.time.get_ticks()
                teclado = [pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT,pygame.K_RETURN]
                for item in teclado:
                    if (pygame.time.get_ticks() - tempo_press) > 300:
                        if teclas_pressionadas[item]:
                            tempo_press = pygame.time.get_ticks()
                            self.tela.mover_no_teclado(item)
                            
                self.tela.atualizar()
                self.atualizar_display()
                self.tela.desenhar()
            
            elif (self.estado == 'jogando'):
                
                eventos: List[pygame.event.Event] = pygame.event.get()
                for evento in eventos:
                    if (evento.type == pygame.QUIT):
                        self.rodando = False

                teclas_pressionadas = pygame.key.get_pressed()
                if teclas_pressionadas[pygame.K_ESCAPE]:
                    if (pygame.time.get_ticks() - tempo_press) > 300:
                        tempo_press = pygame.time.get_ticks()
                        if self.pausado:
                            self.musica.set_volume(self.musica_volume)
                        else:
                            self.musica.set_volume(self.musica_volume/10)
                        self.tela_pause.botoes = self.tela_pause.botoes_principais
                        self.tela_pause.set_botoes = 0
                        self.tela_pause.pos_botao = 0
                        self.pausado = not self.pausado
                
                if not self.pausado:
                    self.tela.atualizar()
                    self.atualizar_display()
                    self.tela.desenhar()
                else:
                    teclado = [pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT,pygame.K_RETURN]
                    for item in teclado:
                        if (pygame.time.get_ticks() - tempo_press) > 300:
                            if teclas_pressionadas[item]:
                                tempo_press = pygame.time.get_ticks()
                                self.tela_pause.mover_no_teclado(item)
                    self.tela_pause.atualizar()
                    self.atualizar_display()
                    self.tela.desenhar()
                    self.tela_pause.desenhar()
                
            self.relogio.tick(60)
        pygame.quit()

    def atualizar_display(self):
        larg, alt = pygame.display.get_window_size()
        if self.largura != larg or self.altura != alt:
            self.largura = larg
            self.altura = alt
            if isinstance(self.tela, telas.padrao.tela):
                self.tela.re_escalar(self.largura, self.altura)
                self.tela_pause.re_escalar(self.largura, self.altura)

    def interagir(self, res):
        match res:
            case 'selecao':
                self.tela = telas.selecao.tela(self.largura, self.altura, self.cor, self.musica_volume, self.volume_efeitos, None, self.display, self.interagir)
                pygame.display.set_caption("Seleção de mapas")
                self.estado = 'selecao'
            case 'opcoes':
                self.tela = telas.opcoes.tela(self.largura, self.altura, self.cor, self.musica_volume, self.volume_efeitos, None, self.display, self.interagir)
                pygame.display.set_caption("Opções")
                self.estado = 'opcoes'
            case 'inicio':
                self.tela = telas.inicio.tela(self.largura, self.altura, self.cor, self.musica_volume, self.volume_efeitos, "fundo_inicio.png", self.display, self.interagir)
                pygame.display.set_caption("Início")
                self.estado = 'inicio'
            case 'oceano':
                self.pausado = False
                self.tela = jogo.oceano(self.largura, self.altura, self.cor, self.musica_volume, self.volume_efeitos, self.display)
                pygame.display.set_caption("Mapa oceano")
                self.estado = "jogando"
            case 'deserto':
                self.pausado = False
                self.tela = jogo.deserto(self.largura, self.altura, self.cor, self.musica_volume, self.volume_efeitos, self.display)
                pygame.display.set_caption("Mapa deserto")
                self.estado = "jogando"
            case 'espaco':
                self.pausado = False
                self.tela = jogo.espaco(self.largura, self.altura, self.cor, self.musica_volume, self.volume_efeitos, self.display)
                pygame.display.set_caption("Mapa espaço")
                self.estado = "jogando"
            case 'silenciar_eventos':
                if len(self.tela.eventos) > 0:
                    for evento in self.tela.eventos:
                        evento.som.stop()
            case 'resumir':
                self.pausado = False
            case 'efeitos':
                if not self.pausado:
                    self.volume_efeitos = self.tela.pegar_vol_efeitos()
                    self.tela.volume_efeitos = self.volume_efeitos
                    self.tela_pause.volume_efeitos = self.volume_efeitos
                    self.tela.atualizar_vol_efeitos(self.volume_efeitos)
                else:
                    self.volume_efeitos = self.tela_pause.pegar_vol_efeitos()
                    self.tela.volume_efeitos = self.volume_efeitos
                    self.tela_pause.volume_efeitos = self.volume_efeitos
                    self.tela_pause.atualizar_vol_efeitos(self.volume_efeitos)
            case 'musica':
                if not self.pausado:
                    self.musica_volume = self.tela.pegar_vol_musica()
                    self.tela.volume_musica = self.musica_volume
                    self.tela_pause.volume_musica = self.musica_volume
                    self.musica.set_volume(self.musica_volume)
                else:
                    self.musica_volume = self.tela_pause.pegar_vol_musica()
                    self.tela.volume_musica = self.musica_volume
                    self.tela_pause.volume_musica = self.musica_volume
                    self.musica.set_volume(self.musica_volume)
            case _:
                pass
         
if (__name__ == "__main__"):
    pygame.init()
    Jogo = GerenciadorTelas(800, 600, (0,0,0))
    Jogo.run()
    pygame.quit()
    sys.exit()