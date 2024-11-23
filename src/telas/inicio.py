import pygame, sys, botoes
from . import padrao

class tela(padrao.tela):
<<<<<<< HEAD
    def __init__(self, largura, altura, cor, musica, efeitos, fundo, display, callback_botoes):
        '''
        Parameters
        ----------
        efeitos: float
            Valor entre 0 e 1 que representa o volume
            dos efeitos.
=======
    '''
    Subclasse de `padrao.tela` que define o menu de início
    
    Atributos adicionais
    --------------------
    fonte: pygame.font.SysFont

        Fonte a ser utilizada na tela
        
    nome_fundo: str
    
        Nome do fundo a ser utlizado na tela
        
    fundo: pygame.Surface
    
        Fundo a ser utilizado na tela
        
    nome: pygame.Surface
    
        Texto que indica o nome do jogo
        
    nome_rect: pygame.Rect
    
        Retângulo onde será impresso o atributo `nome`
        
    callback_botoes: function
    
        Função para chamada de retorno quando um dos botões da tela for 
        acionado
        
    volume_musica: float
    
        Valor que indica o volume da música que está sendo tocada
        
    volume_efeitos: float
    
        Valor que indica o volume dos efeitos dos botões
        
    jogar = botoes.Botao
    
        Botão utilizado na tela que leva para o menu de seleção de 
        cenários
        
    opcoes = botoes.Botao
    
        Botão utilizado na tela que leva para o menu de opções
        
    sair = botoes.Botao
    
        Botão utilizado na tela que encerra a execução do pygame
    '''
    def __init__(self, largura, altura, cor, volume_musica, volume_efeitos, fundo, display, callback_botoes):
        '''
        Inicializa um objeto da subclasse inicio.tela
        
        Parâmetros
        ----------
        volume_musica: float

            Valor do volume da música sendo tocada

        volume_efeitos: float

            Valor do volume dos efeitos dos botões

        fundo: pygame.Surface

            Imagem ou superfície a ser utilizada de fundo na tela

        callback_botões: function

            Função de retorno dos botões da tela
>>>>>>> dea53f1aa41b5a56d9244fb01550c69627a4841c
        '''
        super().__init__(largura, altura, cor, display)
        pygame.display.set_caption("Inicio")
        
        self.fonte = pygame.font.SysFont("Terminal", self.largura // 10)
        self.nome_fundo = fundo
        self.fundo = fundo
        if self.fundo != None:
<<<<<<< HEAD
            self.caminho_fundo += fundo
            self.fundo = pygame.image.load(self.caminho_fundo)
            self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
        self.rect = self.fundo.get_rect()
        self.rect.x = 0
        self.rect.y = 0
=======
            self.caminho_fundo += self.fundo
            self.fundo = pygame.image.load(self.caminho_fundo)
            self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
>>>>>>> dea53f1aa41b5a56d9244fb01550c69627a4841c
        self.nome = self.fonte.render("Batalhas Matemáticas", False, "White")
        self.nome_rect = self.nome.get_rect(center = (self.largura//2, self.altura//10))
        x_botoes = self.largura//2
        y_botoes = self.altura//10
        tam_fonte = altura//10
        self.callback_botoes = callback_botoes
<<<<<<< HEAD
        self.musica = musica
        self.volume_efeitos = efeitos
=======
        self.volume_musica = volume_musica
        self.volume_efeitos = volume_efeitos
>>>>>>> dea53f1aa41b5a56d9244fb01550c69627a4841c
        self.jogar = botoes.Botao((x_botoes, 4*y_botoes), "Jogar", "Terminal", tam_fonte, 
                        "White", (255,242,0), self.volume_efeitos, True)
        self.opcoes = botoes.Botao((x_botoes, 6*y_botoes), "Opções", "Terminal", tam_fonte, 
                        "White", (255,242,0), self.volume_efeitos)
        self.sair = botoes.Botao((x_botoes, 8*y_botoes), "Sair", "Terminal", tam_fonte,
                        "White", (255,242,0), self.volume_efeitos)
        self.botoes = [self.jogar, self.opcoes, self.sair]

    def re_escalar(self, largura_nova, altura_nova):
<<<<<<< HEAD
        if self.fundo == None:
            self.__init__(largura_nova, altura_nova, self.cor, self.musica, self.volume_efeitos, 
                          None, self.display, self.callback_botoes)
        else:
            self.__init__(largura_nova, altura_nova, self.cor, self.musica, self.volume_efeitos, 
                          self.nome_fundo, self.display, self.callback_botoes)

    def checar_eventos(self, evento = None):
=======
        '''
        Método que inicializa um novo objeto da subclasse tela atual com
        os mesmos parâmetros, com alterações apenas na largura e altura.

        Parâmetros
        ----------
        largura_nova: int

            Novo comprimento em x do objeto

        altura_nova: int
        
            Novo comprimento em y do objeto
        '''
        if self.fundo == None:
            self.__init__(largura_nova, altura_nova, self.cor, self.volume_musica, self.volume_efeitos, 
                          None, self.display, self.callback_botoes)
        else:
            self.__init__(largura_nova, altura_nova, self.cor, self.volume_musica, self.volume_efeitos, 
                          self.nome_fundo, self.display, self.callback_botoes)

    def checar_eventos(self, evento = None):
        '''
        Método que utiliza a chamada de retorno em cada botão de 
        determinada maneira

        Parâmetro
        ---------
        evento: pygame.key | None
            Evento a ser analisado na tela, caso haja algum
        '''
>>>>>>> dea53f1aa41b5a56d9244fb01550c69627a4841c
        if evento == pygame.K_RETURN:
            match self.pos_botao:
                case 0:
                    self.callback_botoes('selecao')
                case 1:
                    self.callback_botoes('opcoes')
                case 2:
                    pygame.quit()
                    sys.exit()
                case _:
                    pass
        if self.jogar.mouse and pygame.mouse.get_pressed()[0]:
            self.callback_botoes('selecao')
        if self.opcoes.mouse and pygame.mouse.get_pressed()[0]:
            self.callback_botoes('opcoes')
        if self.sair.mouse and pygame.mouse.get_pressed()[0]:        
            pygame.quit()
            sys.exit()

    def desenhar(self):
<<<<<<< HEAD
=======
        '''
        Desenha os objetos da subclasse no display do pygame
        '''
>>>>>>> dea53f1aa41b5a56d9244fb01550c69627a4841c
        self.display.fill(self.cor)
        if self.fundo != None:
            self.display.blit(self.fundo, (0,0))
        super().desenhar()
<<<<<<< HEAD
        self.display.blit(self.nome, self.nome_rect)
=======
        self.display.blit(self.nome, self.nome_rect)
>>>>>>> dea53f1aa41b5a56d9244fb01550c69627a4841c
