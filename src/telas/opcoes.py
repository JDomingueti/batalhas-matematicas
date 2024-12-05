import pygame, sys, botoes
from . import padrao

class tela(padrao.tela):
    '''
    Subclasse de `padrao.tela` que define o menu de opções fora dos
    cenários
    
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
        
    voltar: botoes.Botao
        
        Botão utilizado para retornar ao menu de início

    musica: botoes.Controle_desl

        Controle deslizante utilizado para ajustar o volume da música
        do jogo

    efeitos: botoes.Controle_desl

        Controle deslizante utilizado para ajustar o volume dos efeitos
        do jogo

    Métodos adicionais
    ------------------
        - pegar_vol_musica()
        - pegar_vol_efeitos()
    '''
    def __init__(self, largura, altura, cor, volume_musica, volume_efeitos, fundo, display, callback_botoes):
        '''
        Inicializa um objeto da subclasse opcoes.tela
        
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
        '''
        super().__init__(largura, altura, cor, display)

        self.nome_fundo = fundo
        self.fundo = fundo
        if self.fundo != None:
            self.caminho_fundo += fundo
            self.fundo = pygame.image.load(fundo)
            self.fundo = pygame.transform.scale(self.fundo, (self.largura, self.altura))
            self.fundo = self.fundo.convert_alpha()
            self.fundo.set_alpha(60)
        
        self.fonte = pygame.font.SysFont("Terminal", self.largura//10)
        self.nome = self.fonte.render("Opcões", False, "White")
        self.nome_rect = self.nome.get_rect(center = (self.largura//2, self.altura//10))
        
        self.callback_botoes = callback_botoes
        
        x_botoes = self.largura//2
        y_botoes = self.altura//10
        tam_fonte = altura//15
        tam_barras = (self.largura//3, 10)
        
        self.volume_musica = volume_musica
        self.volume_efeitos = volume_efeitos

        self.voltar : botoes.Botao = botoes.Botao((x_botoes, 9 * y_botoes), "Voltar", "Terminal",
                        tam_fonte, "White", (255,242,0), self.volume_efeitos, True)
        self.musica : botoes.Controle_desl = botoes.Controle_desl((3 * self.largura // 7, 4 * y_botoes),
                        "Musica", "Terminal", tam_fonte, tam_barras, self.volume_musica, (250, 250, 250))
        self.efeitos : botoes.Controle_desl = botoes.Controle_desl((3 * self.largura // 7, 6 * y_botoes), 
                        "Efeitos", "Terminal", tam_fonte, tam_barras, self.volume_efeitos, (250, 250, 250))

        self.botoes = [self.voltar, self.musica, self.efeitos]

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
                    self.callback_botoes('musica')
                case 2:
                    self.callback_botoes('efeitos')
                case _:
                    pass
        if (self.voltar.mouse and pygame.mouse.get_pressed()[0]):
            self.callback_botoes('inicio')
        if self.efeitos.destacado or self.efeitos.focado:
            self.callback_botoes('efeitos')
        if self.musica.destacado or self.musica.focado:
            self.callback_botoes('musica')

    def desenhar(self):
        self.display.fill(self.cor)
        if self.fundo != None:
            self.display.blit(self.fundo, (0,0))
        super().desenhar()
        self.display.blit(self.nome, self.nome_rect)

    def atualizar(self):
        super().atualizar()
        if self.efeitos.destacado:
            self.atualizar_vol_efeitos(self.pegar_vol_efeitos())

    def pegar_vol_musica(self):
        '''
        Método utilizado para o botão de controle deslizante de ajuste
        do volume da música.
        '''
        return(self.musica.ler_posicao())

    def pegar_vol_efeitos(self):
        '''
        Método utilizado para o botão de controle deslizante de ajuste
        do volume dos efeitos.
        '''
        return (self.efeitos.ler_posicao())