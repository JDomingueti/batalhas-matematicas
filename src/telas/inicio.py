import pygame, sys, botoes
from . import padrao

class tela(padrao.tela):
    def __init__(self, largura, altura, cor, musica, efeitos, fundo, display, callback_botoes):
        '''
        Parameters
        ----------
        efeitos: float
            Valor entre 0 e 1 que representa o volume
            dos efeitos.
        '''
        super().__init__(largura, altura, cor, display)
        pygame.display.set_caption("Inicio")
        
        self.fonte = pygame.font.SysFont("Terminal", self.largura // 10)
        self.nome_fundo = fundo
        self.fundo = fundo
        if self.fundo != None:
            self.caminho_fundo += fundo
            self.fundo = pygame.image.load(self.caminho_fundo)
            self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
        self.rect = self.fundo.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.nome = self.fonte.render("Batalhas Matemáticas", False, "White")
        self.nome_rect = self.nome.get_rect(center = (self.largura//2, self.altura//10))
        x_botoes = self.largura//2
        y_botoes = self.altura//10
        tam_fonte = altura//10
        self.callback_botoes = callback_botoes
        self.musica = musica
        self.volume_efeitos = efeitos
        self.jogar = botoes.Botao((x_botoes, 4*y_botoes), "Jogar", "Terminal", tam_fonte, 
                        "White", (255,242,0), self.volume_efeitos, True)
        self.opcoes = botoes.Botao((x_botoes, 6*y_botoes), "Opções", "Terminal", tam_fonte, 
                        "White", (255,242,0), self.volume_efeitos)
        self.sair = botoes.Botao((x_botoes, 8*y_botoes), "Sair", "Terminal", tam_fonte,
                        "White", (255,242,0), self.volume_efeitos)
        self.botoes = [self.jogar, self.opcoes, self.sair]

    def re_escalar(self, largura_nova, altura_nova):
        if self.fundo == None:
            self.__init__(largura_nova, altura_nova, self.cor, self.musica, self.volume_efeitos, 
                          None, self.display, self.callback_botoes)
        else:
            self.__init__(largura_nova, altura_nova, self.cor, self.musica, self.volume_efeitos, 
                          self.nome_fundo, self.display, self.callback_botoes)

    def checar_eventos(self, evento = None):
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
        self.display.fill(self.cor)
        if self.fundo != None:
            self.display.blit(self.fundo, (0,0))
        super().desenhar()
        self.display.blit(self.nome, self.nome_rect)
