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
        
    recomecar: botoes.Botao
    
        Botão utilizado retornar à tela seleção
        
    inicio: botoes.Botao
    
        Botão utilizado para retornar a tela inicial
        
    botoes: List[botoes.padrao] 

        Lista com os botões do set atual.
    '''
    def __init__(self, largura, altura, cor, volume_efeitos, display, callback_botoes, placar):
        '''
        Inicializa um objeto da subclasse fim_jogo.tela
        
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
        # Última imagem desenhada na tela
        self.imagem_fundo = pygame.image.load("../assets/fundos/fim.jpg")
        self.imagem_fundo = pygame.transform.scale(self.imagem_fundo, (self.largura, self.altura))
        self.volume_efeitos = volume_efeitos
        self.callback_botoes = callback_botoes
    
        # Fundo transparente para destacar a mensagem final
        self.superficie_fundo = pygame.Surface((self.largura, self.altura))
        self.superficie_fundo.fill((0,0,0))
        self.superficie_fundo.set_alpha(220)

        dist_botoes = altura//7
        # Texto indicando o menu
        self.fonte = pygame.font.SysFont("Terminal", self.largura//10)
        self.nome = self.fonte.render("Fim de jogo!", False, "White")
        self.nome_rect = self.nome.get_rect(center = (self.largura//2, dist_botoes))
        self.placar = self.fonte.render(f"{placar[0]} - {placar[1]}", False, "White")
        self.placar_rect = self.placar.get_rect(center = (self.largura//2, 2*dist_botoes))
        if placar[0] > placar[1]:
            self.resultado = self.fonte.render("Vitória do player 1!", False, "White")
        elif placar[0] < placar[1]:
            self.resultado = self.fonte.render("Vitória do player 2!", False, "White")
        else:
            self.resultado = self.fonte.render("Melhor de 3?", False, "White")
        self.result_rect = self.resultado.get_rect(center = (self.largura//2, 3*dist_botoes))

        # Botões do menu de pause, divididos em dois grupos (Principais e opções)
        self.recomecar = botoes.Botao((self.largura//2, 5*dist_botoes), "Recomeçar", "Terminal",
                        altura//15,  "White", (255,242,0), volume_efeitos, True)
        self.inicio = botoes.Botao((self.largura//2, 6*dist_botoes), "Inicio", "Terminal", 
                        altura//15,  "White", (255,242,0), volume_efeitos, False)
        self.botoes = [self.recomecar, self.inicio]

    def checar_eventos(self, evento = None):
        if evento == pygame.K_RETURN:
            match self.pos_botao:
                case 0:
                    self.callback_botoes('selecao')
                case 1:
                    self.callback_botoes('inicio')
                case _:
                    pass
        if (self.recomecar.mouse and pygame.mouse.get_pressed()[0]):
            self.callback_botoes('recomecar')
        if (self.inicio.mouse and pygame.mouse.get_pressed()[0]):
            self.callback_botoes('inicio')

    def atualizar(self):
        super().atualizar()
        self.checar_eventos(None)

    def desenhar(self):
        self.display.blit(self.imagem_fundo, (0,0))
        self.display.blit(self.superficie_fundo, (0,0))
        self.display.blit(self.placar, self.placar_rect)
        self.display.blit(self.resultado, self.result_rect)
        self.display.blit(self.nome, self.nome_rect)
        super().desenhar()
        for botao in self.botoes:
            botao.display_botao(self.display)