import pygame, sys, botoes
from . import padrao

class tela(padrao.tela):
    def __init__(self, largura, altura, cor, musica, efeitos, fundo, display, callback_botoes):
        super().__init__(largura, altura, cor, display)

        self.nome_fundo = fundo
        self.fundo = fundo
        if self.fundo != None:
            self.caminho_fundo += fundo
            self.fundo = pygame.image.load(fundo)
            self.fundo = pygame.transform.scale(self.fundo, (self.largura, self.altura))
        
        self.fonte = pygame.font.SysFont("Terminal", self.largura//10)
        self.nome = self.fonte.render("Opcões", False, "White")
        self.nome_rect = self.nome.get_rect(center = (self.largura//2, self.altura//10))
        
        self.callback_botoes = callback_botoes
        
        x_botoes = self.largura//2
        y_botoes = self.altura//10
        tam_fonte = altura//15
        tam_barras = (self.largura//3, 10)
        
        self.volume_musica = musica
        self.volume_efeitos = efeitos

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
        return(self.musica.ler_posicao())

    def pegar_vol_efeitos(self):
        return (self.efeitos.ler_posicao())