<<<<<<< HEAD
import pygame, sys, botoes

class tela:
    def __init__(self, largura, altura, cor, display):
        '''
        Parameters
        ----------
        largura: int
            Largura máxima da tela
        altura: int
            Altura máxima da tela
        cor: ColorValue
            Código da cor, pode ser uma tupla 
            contendo o código rgb ou a str com
            o nome da cor
=======
import pygame, botoes
from abc import ABC, abstractmethod

class tela(ABC):
    '''
    Tipo de tela padrão destinado à criação dos menus

    Atributos
    ---------
    largura: int

        Valor que indica o comprimento em x da tela 
        
    altura: int
    
        Valor que indica o comprimento em y da tela
        
    cor: ColorValue
        
        Valor que indica a cor padrão do fundo a ser utilizada
        na inicialização

    display: pygame.SurfaceType
    
        Janela do pygame que está sendo utilizada
        
    caminho_fundo: str
    
        O caminho utilizado para carregamento das imagens de 
        fundo

    botoes: List
    
        Lista contendo os botões da tela

    pos_botao: int

        Valor que indica a posição do botão na lista que está
        em destaque

    Métodos
    -------
    Métodos da classe:
        - __init__(largura, altura, cor, display)
        - desenhar()
        - atualizar()
        - mover_no_teclado(movimento)
        - atualizar_vol_efeitos(novo_volume)
        - checar_eventos(evento)
        - re-escalar(nova_largura, nova_altura)
    '''
    @abstractmethod
    def __init__(self, largura, altura, cor, display):
        '''
        Inicializa um objeto com a classe `tela` com os parâmetros
        passados

        Parâmetros
        ----------
        largura: int
        
            Comprimento em x da tela

        altura: int

            Comprimento em y da tela

        cor: ColorValue
            
            Código da cor, pode ser uma tupla contendo o código rgb ou 
            a str com o nome da cor (Ex: (0,0,0) ou ('Black'))
>>>>>>> dea53f1aa41b5a56d9244fb01550c69627a4841c
        '''
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.display : pygame.SurfaceType = display
        self.caminho_fundo = "../assets/fundos/"
        self.display.fill(cor)
<<<<<<< HEAD
        self.rodando = True
        self.botoes = []
        self.pos_botao = 0
    
    def desenhar(self):
=======
        self.botoes = []
        self.pos_botao = 0
    
    @abstractmethod
    def desenhar(self):
        '''
        Método desenha por padrão somente os botões na tela
        '''
        # Foi feito dessa maneira para reutilizar a mesma função
        # em diferentes tipos de tela
>>>>>>> dea53f1aa41b5a56d9244fb01550c69627a4841c
        for botao in self.botoes:
            botao.display_botao(self.display)

    def atualizar(self):
<<<<<<< HEAD
=======
        '''
        Método que atualiza os botões da tela analisando o foco do teclado
        e do mouse
        '''
>>>>>>> dea53f1aa41b5a56d9244fb01550c69627a4841c
        for pos, botao in enumerate(self.botoes):
            # 'For' utilizado para não focar dois botões (um 
            # selecionado pelo teclado e outro pelo mouse)
            if botao.mouse and not botao.focado:
                for botao_ in self.botoes:
                    botao_.mouse = False
                    botao_.focado = False
                self.pos_botao = pos
            botao.atualizar()
<<<<<<< HEAD
        pygame.display.flip()

    def mover_no_teclado(self, movimento: pygame.event.EventType):
        # res = None
=======

    def mover_no_teclado(self, movimento: pygame.key):
        '''
        Método para movimento da tela pelo teclado
        Foi adaptado para reação diferenciada em tipos específicos
        de botões.

        Parâmetro
        ---------
        movimento: pygame.key
        
            Movimento realizado pelo teclado que deve ser analisado
            pela tela.
        
        '''
>>>>>>> dea53f1aa41b5a56d9244fb01550c69627a4841c
        if len(self.botoes) > 0:
            if movimento == pygame.K_UP:
                if isinstance(self.botoes[self.pos_botao], botoes.Selecao_mapas):
                    pos_card = self.botoes[self.pos_botao].num_card_destacado
                    self.botoes[self.pos_botao].card_focado[pos_card] = False
                self.botoes[self.pos_botao].focado = False
                self.pos_botao = (self.pos_botao - 1)
                self.pos_botao %= len(self.botoes)
                self.botoes[self.pos_botao].focado = True
                if isinstance(self.botoes[self.pos_botao], botoes.Selecao_mapas):
                    pos_card = self.botoes[self.pos_botao].num_card_destacado
                    self.botoes[self.pos_botao].card_focado[pos_card] = True
            elif movimento == pygame.K_DOWN:
                if isinstance(self.botoes[self.pos_botao], botoes.Selecao_mapas):
                    pos_card = self.botoes[self.pos_botao].num_card_destacado
                    self.botoes[self.pos_botao].card_focado[pos_card] = False
                self.botoes[self.pos_botao].focado = False
                self.pos_botao = (self.pos_botao + 1)
                self.pos_botao %= len(self.botoes)
                self.botoes[self.pos_botao].focado = True
                if isinstance(self.botoes[self.pos_botao], botoes.Selecao_mapas):
                    pos_card = self.botoes[self.pos_botao].num_card_destacado
                    self.botoes[self.pos_botao].card_focado[pos_card] = True
            elif movimento == pygame.K_LEFT:
                if isinstance(self.botoes[self.pos_botao], botoes.Controle_desl):
                    self.botoes[self.pos_botao].focado = True
                    self.botoes[self.pos_botao].percent -= 0.1
                elif isinstance(self.botoes[self.pos_botao], botoes.Selecao_mapas):
                    pos_card = self.botoes[self.pos_botao].num_card_destacado
                    self.botoes[self.pos_botao].num_card_destacado -= 1
                    pos_card = (pos_card - 1) % len(self.botoes[self.pos_botao].cards) 
                    self.botoes[self.pos_botao].card_focado = 3*[False]
                    self.botoes[self.pos_botao].card_focado[pos_card] = True
            elif movimento == pygame.K_RIGHT:
                if isinstance(self.botoes[self.pos_botao], botoes.Controle_desl):
                    self.botoes[self.pos_botao].focado = True
                    self.botoes[self.pos_botao].percent += 0.1
                elif isinstance(self.botoes[self.pos_botao], botoes.Selecao_mapas):
                    pos_card = self.botoes[self.pos_botao].num_card_destacado
                    self.botoes[self.pos_botao].num_card_destacado += 1
                    pos_card = (pos_card + 1) % len(self.botoes[self.pos_botao].cards) 
                    self.botoes[self.pos_botao].card_focado = 3*[False]
                    self.botoes[self.pos_botao].card_focado[pos_card] = True
            else:
                pass
        if movimento == pygame.K_RETURN:
            self.checar_eventos(movimento)

    def atualizar_vol_efeitos(self, novo_volume):
<<<<<<< HEAD
        for botao in self.botoes:
            botao.som.set_volume(novo_volume)
    
    def checar_eventos(self, evento = None):
        pass

    def re_escalar(self, largura_nova, altura_nova):
=======
        '''
        Método utilizado para atualizar o volume dos efeitos dos botões 
        da tela.

        Parâmetro
        ---------
        novo_volume: float

            Novo volume de efeito a ser definido para os botões
        '''
        for botao in self.botoes:
            botao.som.set_volume(novo_volume)
    
    @abstractmethod
    def checar_eventos(self, evento = None):
        '''
        Método que realiza ações predeterminadas para os botões

        Parâmetro
        ---------
        evento: pygame.key | None

            Caso haja algum evento específico da tela, pode ser 
            passado o evento como parâmetro para este método e 
            determinado o comportamento na definição da classe.
        '''
        pass

    def re_escalar(self, largura_nova, altura_nova):
        '''
        Método que inicializa a classe com os mesmos atributos com novos
        atributos de largura e altura.

        Parâmetros
        ----------
        largura_nova: int

            Novo comprimento em x da tela

        altura_nova: int
        
            Novo comprimento em y da tela
        '''
>>>>>>> dea53f1aa41b5a56d9244fb01550c69627a4841c
        self.__init__(largura_nova, altura_nova, self.cor, self.display)
