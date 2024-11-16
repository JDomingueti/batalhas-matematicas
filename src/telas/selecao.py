import pygame, botoes
from . import padrao

class tela(padrao.tela):
    '''
    Subclasse de `padrao.tela` que define o menu de selecao
    
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
        
    cenarios = botoes.Selecao_mapas
    
        Botão que possui a definição dos cards dos cenários a serem 
        desenhados na tela
        
    voltar = botoes.Botao
    
        Botão utilizado na tela que volta para o menu de início
        
    self.botoes = List[botoes.Botao, botoes.Selecao_mapas]

        Lista contendo os botões da tela
    '''
    def __init__(self, largura, altura, cor, volume_musica, volume_efeitos, fundo, display, callback_botoes):
        '''
        Inicializa um objeto da subclasse selecao.tela
        
        Parâmetros
        ----------
        volume_musica: float

            Valor do volume da música sendo tocada

        volume_efeitos: float

            Valor do volume dos efeitos dos botões

        fundo: pygame.Surface
        
            Fundo a ser utilizado na tela

        callback_botões: function

            Função de retorno dos botões da tela
        '''
        super().__init__(largura, altura, cor, display)
        
        pygame.display.set_caption("Seleção")
        self.fonte = pygame.font.SysFont("Terminal", self.largura//10)
        self.nome = self.fonte.render("Selecione o mapa", False, "White")
        self.nome_rect = self.nome.get_rect(center = (self.largura//2, self.altura//10))
        self.callback_botoes = callback_botoes
        self.nome_fundo = fundo
        self.fundo = fundo
        if self.fundo != None:
            self.caminho_fundo += fundo
            self.fundo = pygame.image.load(self.caminho_fundo)
            self.fundo = pygame.transform.scale(self.fundo, (self.largura, self.altura))
        x_botao = self.largura//2
        y_botao = self.altura//10
        tam_fonte = self.altura//15
        self.volume_musica = volume_musica
        self.volume_efeitos = volume_efeitos
        self.cenarios = botoes.Selecao_mapas(largura, altura,(255,242,0), self.volume_efeitos)
        self.voltar : botoes.Botao = botoes.Botao((x_botao, 9 * y_botao), "Voltar", "Terminal",
                        tam_fonte, "White", (255,242,0), self.volume_efeitos, True)
        self.botoes = [self.voltar, self.cenarios]

    def re_escalar(self, largura_nova, altura_nova):
        if self.fundo == None:
            self.__init__(largura_nova, altura_nova, self.cor, self.volume_musica, self.volume_efeitos, 
                          None, self.display, self.callback_botoes)
        else:
            self.__init__(largura_nova, altura_nova, self.cor, self.volume_musica, self.volume_efeitos, 
                          self.nome_fundo, self.display, self.callback_botoes)

    def checar_eventos(self, evento = None):
        if evento == pygame.K_RETURN:
            match self.pos_botao:
                case 0:
                    self.callback_botoes('inicio')
                case 1:
                    match self.cenarios.num_card_destacado:
                        case 0:
                            self.callback_botoes('oceano')
                        case 1:
                            self.callback_botoes('deserto')
                        case 2:
                            self.callback_botoes('espaco')
                case _:
                    pass
        if (self.voltar.mouse and pygame.mouse.get_pressed()[0]):
            self.callback_botoes('inicio')
        if (self.cenarios.mouse and pygame.mouse.get_pressed()[0]):
            match self.cenarios.num_card_destacado:
                case 0:
                    self.callback_botoes('oceano')
                case 1:
                    self.callback_botoes('deserto')
                case 2:
                    self.callback_botoes('espaco')
        if (self.pos_botao == 0):
            self.cenarios.card_focado = 3*[False]
            self.cenarios.card_mouse = 3*[False]
    
    def atualizar(self):
        super().atualizar()
        self.cenarios.atualizar()
    
    def desenhar(self):
        self.display.fill(self.cor)
        if self.fundo != None:
            self.display.blit(self.fundo, (0,0))
        super().desenhar()
        self.cenarios.display_botao(self.display)
        self.display.blit(self.nome, self.nome_rect)
