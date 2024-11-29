import pygame, sys, telas
import jogo
from telas import inicio, opcoes, pause_em_jogo, selecao
from typing import List

class GerenciadorTelas:
    '''
    Código que controla e associa os códigos de:
        - Menus
        - Execução em jogo
        - Opções
    Relaciona e direciona comandos de diferentes arquivos de códigos

    Atributos
    ---------
    Lista dos atributos da classe com descrição breve:

    largura_padrao: int
    
        Comprimento em x inicial da tela
        
    largura: int
    
        Comprimento em x atual da tela
        
    altura_padrao: int
    
        Comprimento em y inicial da tela
        
    altura: int
    
        Comprimento em y atual da tela
        
    cor: ColorValue
    
        Cor padrão do fundo da tela
        
    volume_efeitos: float
    
        Volume dos efeitos compreendido entre 0 e 1
        
    musica: pygame.mixer.Sound
    
        Música que toca durante o jogo
        
    volume_musica: float
    
        Volume da música compreendido entre 0 e 1
        
    display: pygame.display
    
        Janela utilizada pelo jogo
        
    tela: padrao.tela | jogo.jogo
    
        Classe que herda da classe padrao.tela ou da classe jogo.jogo e 
        que controla o que será exibido na tela
        
    tela_pause : pause_em_jogo.tela

        Classe utilizada para desenhar o pause do menu quando em jogo

    rodando: bool
    
        Booleano que indica se o programa deve ser rodado
        
    pausado: bool
    
        Booleano que indica se o jogo está pausado (destinado a quando a
        tela é da classe jogo.jogo)
        
    estado: str
    
        Texto que indica o estado atual da tela (Se o jogo está no menu 
        inicial, de opções, de seleção ou em um dos mapas de jogo)
        
    relogio: pygame.time.Clock

        Relógio do menu

    Métodos
    -------
    Os métodos que podem ser executados são (Mais informações nas 
    definições dos métodos):
        - run()
        - atualizar_display()
        - interagir(estado)
    '''
    def __init__(self, largura, altura, cor):
        '''
        Função que inicializa o jogo
        
        Parâmetros
        ----------
        Largura: int

            É o comprimento em x da tela utilizada no jogo

        altura: int

            É o comprimento em y da tela utilizada no jogo
            
        cor: ColorValue
        
            É a cor padrão a ser usada no fundo da tela. Pode ser passada 
            como valor em RGB (Ex:(0,0,0)) ou nome da cor em inglês caso 
            seja uma cor reconhecida pelo pygame (Ex:'White')
        '''
        self.largura_padrao = largura
        self.largura = self.largura_padrao
        self.altura_padrao = altura
        self.altura = self.altura_padrao
        self.cor = cor
        self.volume_efeitos = 0
        self.musica = pygame.mixer.music.load("../assets/musica_menu.mp3")
        pygame.mixer.music.set_volume(0)
        self.volume_musica = pygame.mixer.music.get_volume()
        self.display = pygame.display.set_mode((self.largura, self.altura), pygame.RESIZABLE)
        self.tela = inicio.tela(self.largura, self.altura, self.cor, self.volume_musica, self.volume_efeitos, "fundo_inicio.png", self.display, self.interagir)
        self.tela_pause = pause_em_jogo.tela(self.largura, self.altura, self.cor, self.volume_musica, self.volume_efeitos, self.display, self.interagir)
        self.rodando = True
        self.pausado = False
        self.estado = 'inicio'
        self.relogio = pygame.time.Clock()

    def run(self):
        '''
        Esse método é responsável por, principalmente, redirecionar
        e controlar as ações realizadas pelo jogador (Como `pause`, 
        `K_ESCAPE`, `QUIT`), atualizar as telas, define os frames
        por segundo e troca o estado da tela
        '''
        pygame.mixer.music.play(-1, 1500)
        tempo_press = pygame.time.get_ticks()
        while (self.rodando):
            if (self.estado != 'jogando'):
                eventos: List[pygame.event.Event] = pygame.event.get()
                for evento in eventos:
                    self.tela.checar_eventos(evento)
                    # self.interagir(res)
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
                            self.tela = inicio.tela(self.largura, self.altura, self.cor, self.volume_musica, self.volume_efeitos, "fundo_inicio.png", self.display, self.interagir)
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
                self.tela.desenhar()
            
            else:

                eventos: List[pygame.event.Event] = pygame.event.get()
                for evento in eventos:
                    if (evento.type == pygame.QUIT):
                        self.rodando = False

                teclas_pressionadas = pygame.key.get_pressed()
                if teclas_pressionadas[pygame.K_ESCAPE]:
                    if (pygame.time.get_ticks() - tempo_press) > 300:
                        tempo_press = pygame.time.get_ticks()
                        self.tela_pause.botoes = self.tela_pause.botoes_principais
                        self.tela_pause.set_botoes = 0
                        self.tela_pause.pos_botao = 0
                        self.pausado = not self.pausado

                self.tela.movimento_players(teclas_pressionadas)

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
            pygame.display.flip()
            self.relogio.tick(60)
        pygame.quit()

    def atualizar_display(self):
        '''
        Método que atualiza o tamanho do display do pygame
        '''
        larg, alt = pygame.display.get_window_size()
        if self.largura != larg or self.altura != alt:
            self.largura = larg
            self.altura = alt
            if isinstance(self.tela, telas.padrao.tela):
                self.tela.re_escalar(self.largura, self.altura)
                self.tela_pause.re_escalar(self.largura, self.altura)

    def interagir(self, acao):
        '''
        Método que realiza a interação entre menus e cenários
        Parâmetros
        ----------
        acao: str

            Ação a ser realizada. As ações válidas são:

            - 'selecao' | 'opcoes' | 'inicio'
                - Vai para o respectivo menu
            
            - 'oceano' | 'deserto | 'espaco'
                - Vai para o respectivo cenário de jogo
            
            - 'silenciar_eventos'
                - Para o som dos eventos caso haja algum (destinado 
                para quando estiver em um dos cenários)

            - 'resumir'
                - Despausa o jogo

            - 'efeitos'
                - Atualiza o volume dos efeitos

            - 'musica'
                - Atualiza o volume das musicas
        '''
        match acao:
            case 'selecao':
                self.tela = selecao.tela(self.largura, self.altura, self.cor, self.volume_musica, self.volume_efeitos, None, self.display, self.interagir)
                pygame.display.set_caption("Seleção de mapas")
                self.estado = 'selecao'
            case 'opcoes':
                self.tela = opcoes.tela(self.largura, self.altura, self.cor, self.volume_musica, self.volume_efeitos, None, self.display, self.interagir)
                pygame.display.set_caption("Opções")
                self.estado = 'opcoes'
            case 'inicio':
                self.tela = inicio.tela(self.largura, self.altura, self.cor, self.volume_musica, self.volume_efeitos, "fundo_inicio.png", self.display, self.interagir)
                pygame.display.set_caption("Início")
                self.estado = 'inicio'
            case 'oceano':
                self.pausado = False
                self.tela = jogo.oceano(self.largura, self.altura, self.cor, self.volume_musica, self.volume_efeitos, self.display)
                pygame.display.set_caption("Mapa oceano")
                self.estado = "jogando"
            case 'deserto':
                self.pausado = False
                self.tela = jogo.deserto(self.largura, self.altura, self.cor, self.volume_musica, self.volume_efeitos, self.display)
                pygame.display.set_caption("Mapa deserto")
                self.estado = "jogando"
            case 'espaco':
                self.pausado = False
                self.tela = jogo.espaco(self.largura, self.altura, self.cor, self.volume_musica, self.volume_efeitos, self.display)
                pygame.display.set_caption("Mapa espaço")
                self.estado = "jogando"
            case 'opcoes':
                self.tela = opcoes.tela(self.largura, self.altura, self.cor, pygame.mixer.music.get_volume(), self.volume_efeitos)
            case 'voltar':
                self.tela = inicio.tela(self.largura, self.altura, self.cor, self.volume_efeitos, "fundo_inicio.png")
            case 'efeitos':
                if not self.pausado:
                    self.volume_efeitos = self.tela.pegar_vol_efeitos()
                    self.tela.atualizar_vol_efeitos(self.volume_efeitos)
                    self.tela_pause.atualizar_vol_efeitos(self.volume_efeitos)
                else:
                    self.volume_efeitos = self.tela_pause.pegar_vol_efeitos()
                    self.tela.volume_efeitos = self.volume_efeitos
                    self.tela_pause.atualizar_vol_efeitos(self.volume_efeitos)
            case 'musica':
                if not self.pausado:
                    self.volume_musica = self.tela.pegar_vol_musica()
                    self.tela.volume_musica = self.volume_musica
                    self.tela_pause.volume_musica = self.volume_musica
                    pygame.mixer.music.set_volume(self.volume_musica)
                else:
                    self.volume_musica = self.tela_pause.pegar_vol_musica()
                    self.tela.volume_musica = self.volume_musica
                    self.tela_pause.volume_musica = self.volume_musica
                    pygame.mixer.music.set_volume(self.volume_musica)
            case _:
                pass

if (__name__ == "__main__"):
    '''
    Inicializa o jogo e executa caso o código seja executado 
    como principal
    '''
    pygame.init()
    Jogo = GerenciadorTelas(800, 600, (0,0,0))
    Jogo.run()
    pygame.quit()
    sys.exit()