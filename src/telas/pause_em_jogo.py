import pygame, botoes
from . import padrao

class tela(padrao.tela):
    '''
    Subclasse de `padrao.tela` que define o menu de pause dentro de um 
    cenário de jogo
    
    Atributos adicionais
    --------------------
    fonte: pygame.font.SysFont

        Fonte a ser utilizada na tela
        
    superficie_fundo: pygame.Surface
    
        Fundo a ser utilizado na tela
        
    nome: pygame.Surface
    
        Texto que indica o status do jogo
        
    nome_rect: pygame.Rect
    
        Retângulo onde será impresso o atributo `nome`
        
    callback_botoes: function
    
        Função para chamada de retorno quando um dos botões da tela for 
        acionado
        
    volume_musica: float
    
        Valor que indica o volume da música que está sendo tocada
        
    volume_efeitos: float
    
        Valor que indica o volume dos efeitos dos botões
        
    resumir: botoes.Botao
    
        Botão utilizado na tela que muda o status pausado para `False`
        Botão do set 0
        
    opcoes: botoes.Botao
    
        Botão utilizado na tela que leva para o menu de opções
        Botão do set 0, alterna para o set 1.
        
    inicio: botoes.Botao
    
        Botão utilizado na tela que encerra a execução do pygame
        Botão do set 0
    
    musica: botoes.Controle_desl

        Controle deslizante utilizado para ajustar o volume da música do
        jogo. Botão do set 1

    
    efeitos: botoes.Controle_desl

        Controle deslizante utilizado para ajustar o volume dos efeitos do
        jogo. Botão do set 1
    
    voltar: botoes.Botao

        Botão utilizado para voltar ao set de botões principal do menu.
        Botão do set 1, alterna para o set 0.
            
    botoes: List[botoes.padrao] 

        Lista com os botões do set atual.
    
    set_botoes: int

        Indica o set atual de botões sendo utilizados.
        Set 0: [resumir, opcoes, inicio] 
        Set 1: [voltar, musica, efeitos]
    '''
    def __init__(self, largura, altura, cor, volume_musica, volume_efeitos, display, callback_botoes):
        '''
        Inicializa um objeto da subclasse pause_em_jogo.tela
        
        Parâmetros
        ----------
        volume_musica: float

            Valor do volume da música sendo tocada

        volume_efeitos: float

            Valor do volume dos efeitos dos botões

        callback_botões: function

            Função de retorno dos botões da tela
        '''
        super().__init__(largura, altura, cor, display)
        
        self.volume_musica = volume_musica
        self.volume_efeitos = volume_efeitos
        self.callback_botoes = callback_botoes
        
        # Fundo transparente para destacar o menu de pause
        self.superficie_fundo = pygame.Surface((self.largura, self.altura))
        self.superficie_fundo.fill((0,0,0))
        self.superficie_fundo.set_alpha(100)

        # Texto indicando que o menu está pausado
        self.fonte = pygame.font.SysFont("Terminal", self.largura//10)
        self.nome = self.fonte.render("Pausado", False, "White")
        self.nome_rect = self.nome.get_rect(center = (self.largura//2, self.altura//10))

        dist_botoes = altura//5

        # Botões do menu de pause, divididos em dois grupos (Principais e opções)
        self.resumir = botoes.Botao((self.largura//2, 2*dist_botoes), "Resumir", "Terminal",
                        altura//15,  "White", (255,242,0), volume_efeitos, True)
        self.opcoes = botoes.Botao((self.largura//2, 3*dist_botoes), "Opções", "Terminal", 
                        altura//15,  "White", (255,242,0), volume_efeitos, False)
        self.inicio = botoes.Botao((self.largura//2, 4*dist_botoes), "Início", "Terminal", 
                        altura//15,  "White", (255,242,0), volume_efeitos, False)
        self.voltar = botoes.Botao((self.largura//2, 4*dist_botoes), "Voltar", "Terminal",
                        altura//15,  "White", (255,242,0), volume_efeitos, False)
        self.musica = botoes.Controle_desl((2*self.largura//5, 2*dist_botoes), "Música", 
                        "Terminal", altura//15, (self.largura//3, 20), volume_musica, "White", 
                        (255,242,0), volume_efeitos, False)
        self.efeitos = botoes.Controle_desl((2*self.largura//5, 3*dist_botoes), "Efeitos", 
                        "Terminal", altura//15, (self.largura//3, 20), volume_efeitos, "White",
                        (255,242,0), volume_efeitos, False)

        self.botoes_principais = [self.resumir, self.opcoes, self.inicio]
        self.botoes_opcoes = [self.voltar, self.musica, self.efeitos]
        self.botoes = self.botoes_principais
        self.set_botoes = 0

    def checar_eventos(self, evento = None):
        if evento == pygame.K_RETURN:
            if self.set_botoes == 0:
                match self.pos_botao:
                    case 0:
                        self.callback_botoes('resumir')
                    case 1:
                        self.opcoes.focado = False
                        self.voltar.focado = True
                        self.pos_botao = 0
                        self.set_botoes = 1
                        self.botoes = self.botoes_opcoes
                    case 2:
                        self.inicio.focado = False
                        self.resumir.focado = True
                        self.pos_botao = 0
                        self.set_botoes = 0
                        self.botoes = self.botoes_principais
                        self.callback_botoes('silenciar_eventos')
                        self.callback_botoes('inicio')
                    case _:
                        pass
            else:
                match self.pos_botao:
                    case 0:
                        self.voltar.focado = False
                        self.resumir.focado = True
                        self.set_botoes = 0
                        self.botoes = self.botoes_principais
                    case 1:
                        self.callback_botoes('musica')
                    case 2:
                        self.callback_botoes('efeitos')
                    case _:
                        pass
        if self.set_botoes == 0:
            if (self.resumir.mouse and pygame.mouse.get_pressed()[0]):
                self.callback_botoes('resumir')
            if (self.opcoes.mouse and pygame.mouse.get_pressed()[0]):
                self.opcoes.focado = False
                self.voltar.focado = True
                self.pos_botao = 0
                self.set_botoes = 1
                self.botoes = self.botoes_opcoes
            if (self.inicio.mouse and pygame.mouse.get_pressed()[0]):
                self.callback_botoes('inicio')
        else:
            if (self.musica.destacado or self.musica.focado):
                self.callback_botoes('musica')
            if (self.efeitos.destacado or self.efeitos.focado):
                self.callback_botoes('efeitos')
            if (self.voltar.mouse and pygame.mouse.get_pressed()[0]):
                self.voltar.focado = False
                self.resumir.focado = True
                self.botoes = self.botoes_principais
                self.pos_botao = 0
                self.set_botoes = 0

    def atualizar(self):
        super().atualizar()
        self.checar_eventos(None)

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

    def atualizar_vol_efeitos(self, novo_volume):
        for set_botao in [self.botoes_principais, self.botoes_opcoes]:
            for botao in set_botao:
                botao.som.set_volume(novo_volume)

    def re_escalar(self, largura_nova, altura_nova):
        self.__init__(largura_nova, altura_nova, self.cor, self.volume_musica, self.volume_efeitos, 
                      self.display, self.callback_botoes)

    def desenhar(self):
        self.display.blit(self.superficie_fundo,(0,0))
        self.display.blit(self.nome, self.nome_rect)
        for botao in self.botoes:
            botao.display_botao(self.display)