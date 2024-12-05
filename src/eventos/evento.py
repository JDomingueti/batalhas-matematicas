import pygame, random
from abc import ABC, abstractmethod

''' Arquivo para implementação dos eventos dos cenários '''

class evento(ABC):
    '''
    Classe padrão dos eventos, criada para servir de base nos métodos
    e compartilhar métodos e linhas de código repetidas.
    
    Atributos
    ---------
    largura_tela: int

        Comprimento em x da tela

    altura_tela: int
     
        Comprimento em y da tela
        
    tela: pygame.SurfaceType

        Tela na qual o evento está sendo criado

    comecou: bool

        Indica se o evento foi inicializado

    volume_efeitos: float
     
        Volume dos efeitos em jogo

    lado_inicio: int
     
        Indica o lado de início do evento.
        1: indica que o evento começará do lado esquerdo da tela
        -1: indica que o evento começará do lado direito da tela
        
    contador: int

        Utilizado para controlar o tempo do evento em tela

    caminho: str
    
        Caminho dos arquivos do evento

    Métodos
    -------
        - __init__()
    '''
    @abstractmethod
    def __init__(self, tela: pygame.Surface, volume_efeitos):
        '''
        Inicializa um objeto da classe evento.evento

        Parâmetros
        ----------
        tela: pygame.Surface

            Superfície na qual serão gerados os eventos

        volume_efeitos: float

            Valor do volume dos efeitos em jogo
        '''
        pygame.init()
        self.largura_tela = tela.get_width()
        self.altura_tela = tela.get_height()
        self.tela = tela
        self.comecou = False
        self.volume_efeitos = volume_efeitos
        self.lado_inicio = random.choice([-1,1])
        self.contador = pygame.time.get_ticks()
        self.caminho = "../assets/eventos/"
        self.intervalo_dano = 200
        self.separador_dano = 0
        
    def aviso_direcao(self):
        '''
        Gera o aviso na tela que um evento foi inicializado e a posição
        na qual o evento está vindo
        '''
        if self.comecou and (pygame.time.get_ticks() - self.contador <= 2500):
            self.tela.blit(self.img_aviso, self.rect_aviso)

    @abstractmethod
    def atualizar(self):
        '''
        Método que atualiza as informações do evento
        '''
        if not self.comecou:
            self.contador = pygame.time.get_ticks()
            self.som.play(-1, fade_ms=2000)
            self.som.set_volume(self.volume_efeitos)
            self.comecou = True

    @abstractmethod
    def desenhar(self):
        '''
        Método que desenha o evento na superfície da tela
        '''
        pass

    @abstractmethod
    def verificar_colisao(self, rect_obj : pygame.Rect, dano: int):
        '''
        Método para verificar a colisão do(s) retângulo(s) do evento

        Parâmetros
        ----------
        rect_obj: pygame.Rect

            Retângulo a ser verificada a colisão com o evento
        
        dano: int
            
            Dano a ser realizado ao evento caso tenha tido a colisão
        '''
        pass

    @abstractmethod
    def matar(self):
        '''
        Método que verifica se o evento deve ser destruído com base
        na posição e na vida
        '''
        pass

    @abstractmethod
    def pegar_rect(self):
        '''
        Método que retorna o(s) retângulo(s) do evento
        '''
        pass

class explosao(evento):
    '''
    Evento visual para ser gerado na morte dos outros eventos
    Herda da classe evento.evento para melhor monitoramento e interação
    com os outros eventos

    Atributos
    ---------
    tela: pygame.Surface

        Tela na qual será gerado o evento

    imgs: List[pygame.Surface]

        Lista contendo os sprites do evento

    rect: pygame.Rect

        Retângulo na qual deve ser gerado o evento

    volume_efeitos: float

        Volume de efeito do evento

    som: pygame.mixer.Sound

        Som gerado pelo evento. Volume é controlado por volume_efeitos

    comecou: bool

        Booleano que monitora se foi iniciado o evento

    destruir: bool

        Booleano que monitora se o evento terminou

    sprite_atual: int

        Número que indica o sprite do evento para animação

    frame_atual: int

        Número que indica o frame atual do jogo para animação

    frames_por_sprites: int

        Número que indica o número de frames que cada sprite permanece
        na tela
    '''
    def __init__(self, rect: pygame.Rect, tela: pygame.Surface, volume_efeitos: pygame.mixer.Sound):
        self.tela = tela
        caminho = "../assets/eventos/"
        self.imgs = []
        for i in range(1,4):
            img = pygame.image.load(caminho + f"explosao/{i}.png")
            img = pygame.transform.scale(img, rect.size)
            self.imgs.append(img)
        self.rect = pygame.Rect(rect.topleft, rect.size)
        self.volume_efeitos = volume_efeitos
        self.som = pygame.mixer.Sound(caminho + "sons/explosion.wav")
        self.comecou = False
        self.destruir = False
        self.sprite_atual = 0
        self.frame_atual = 0
        self.frames_por_sprites = 15

    def aviso_direcao(self):
        pass

    def atualizar(self):
        if not self.comecou:
            self.som.play(fade_ms=100)
            self.som.set_volume(self.volume_efeitos)
        if (self.frame_atual >= self.frames_por_sprites):
            if self.sprite_atual < 2:
                self.frame_atual = 0
                self.sprite_atual += 1
            else:
                self.destruir = True
        self.frame_atual += 1

    def desenhar(self):
        self.tela.blit(self.imgs[self.sprite_atual], self.rect)

    def verificar_colisao(self, rect_obj: pygame.Rect, dano: int):
        return False, 0

    def matar(self, callback):
        if self.destruir:
            self.som.fadeout(100)
        return self.destruir

    def pegar_rect(self):
        return self.rect