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
        '''
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.display : pygame.SurfaceType = display
        self.caminho_fundo = "../assets/fundos/"
        self.display.fill(cor)
        self.rodando = True
        self.botoes = []
        self.pos_botao = 0
    
    def desenhar(self):
        for botao in self.botoes:
            botao.display_botao(self.display)

    def atualizar(self):
        for pos, botao in enumerate(self.botoes):
            # 'For' utilizado para não focar dois botões (um 
            # selecionado pelo teclado e outro pelo mouse)
            if botao.mouse and not botao.focado:
                for botao_ in self.botoes:
                    botao_.mouse = False
                    botao_.focado = False
                self.pos_botao = pos
            botao.atualizar()
        pygame.display.flip()

    def mover_no_teclado(self, movimento: pygame.event.EventType):
        # res = None
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
        for botao in self.botoes:
            botao.som.set_volume(novo_volume)
    
    def checar_eventos(self, evento = None):
        pass

    def re_escalar(self, largura_nova, altura_nova):
        self.__init__(largura_nova, altura_nova, self.cor, self.display)
