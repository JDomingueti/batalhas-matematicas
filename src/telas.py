import pygame, sys, botoes

class tela:
    def __init__(self, largura, altura, cor):
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
        self.display = pygame.display.set_mode((self.largura, self.altura))
        self.display.fill(cor)
        self.rodando = True
        self.botoes = []
        self.pos_botao = 0
    
    def draw(self):
        for botao in self.botoes:
            botao.display_botao(self.display)

    def atualizar(self):
        for pos, botao in enumerate(self.botoes):
            # 'For' utilizado para não focar dois botões (um 
            # selecionado pelo teclado e outro pelo mouse) 
            if botao.mouse and not botao.focado:
                for botao_ in self.botoes:
                    botao_.focado = False
                self.pos_botao = pos
            botao.atualizar(self.display)
        pygame.display.flip()

    def mover_no_teclado(self, movimento: pygame.event.EventType):
        res = None
        if len(self.botoes) > 0:
            if movimento == pygame.K_UP:
                self.botoes[self.pos_botao].focado = False
                self.pos_botao = (self.pos_botao - 1)
                self.pos_botao %= len(self.botoes)
                self.botoes[self.pos_botao].focado = True
                if isinstance(self.botoes[self.pos_botao], botoes.Selecao_mapas):
                    pos_card = self.botoes[self.pos_botao].num_card_destacado
                    self.botoes[self.pos_botao].card_focado[pos_card] = True
            elif movimento == pygame.K_DOWN:
                self.botoes[self.pos_botao].focado = False
                self.pos_botao = (self.pos_botao + 1)
                self.pos_botao %= len(self.botoes)
                self.botoes[self.pos_botao].focado = True
            elif movimento == pygame.K_LEFT:
                if isinstance(self.botoes[self.pos_botao], botoes.Controle_desl):
                    self.botoes[self.pos_botao].focado = True
                    self.botoes[self.pos_botao].percent -= 0.1
                    res = 'musica'
                elif isinstance(self.botoes[self.pos_botao], botoes.Selecao_mapas):
                    pos_card = self.botoes[self.pos_botao].num_card_destacado
                    self.botoes[self.pos_botao].num_card_destacado -= 1
                    pos_card = 0 if (pos_card < 1) else pos_card - 1 
                    self.botoes[self.pos_botao].card_focado = 3*[False]
                    self.botoes[self.pos_botao].card_focado[pos_card] = True
            elif movimento == pygame.K_RIGHT:
                if isinstance(self.botoes[self.pos_botao], botoes.Controle_desl):
                    self.botoes[self.pos_botao].focado = True
                    self.botoes[self.pos_botao].percent += 0.1
                    res = 'musica'
                elif isinstance(self.botoes[self.pos_botao], botoes.Selecao_mapas):
                    pos_card = self.botoes[self.pos_botao].num_card_destacado
                    self.botoes[self.pos_botao].num_card_destacado += 1
                    pos_card = 2 if (pos_card > 1) else pos_card + 1
                    self.botoes[self.pos_botao].card_focado = 3*[False]
                    self.botoes[self.pos_botao].card_focado[pos_card] = True
            else:
                pass
        if movimento == pygame.K_RETURN:
            res = self.checar_eventos(movimento)
        return res

    def volume_efeitos(self, novo_volume):
        for botao in self.botoes:
            botao.som.set_volume(novo_volume)
    
    def checar_eventos(self, evento = None):
        pass

class inicio(tela):
    def __init__(self, largura, altura, cor, efeitos, imagem):
        '''
        Parameters
        ----------
        efeitos: float
            Valor entre 0 e 1 que representa o volume
            dos efeitos.
        '''
        super().__init__(largura, altura, cor)
        pygame.display.set_caption("Inicio")
        
        self.fonte = pygame.font.SysFont("Terminal", self.largura // 10)
        
        caminho_imagem = "../assets/fundos/" + imagem
        self.imagem = pygame.image.load(caminho_imagem)
        self.imagem = pygame.transform.scale(self.imagem, (800,600))
        self.rect = self.imagem.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.nome = self.fonte.render("Batalhas Matemáticas", False, "White")
        self.nome_rect = self.nome.get_rect(center = (self.largura//2, self.altura//10))
        x_botoes = self.largura//2
        y_botoes = self.altura//10
        tam_fonte = altura//10
        self.jogar = botoes.Botao((x_botoes, 4*y_botoes), "Jogar", "Terminal", tam_fonte, "White", (255,242,0), efeitos = efeitos, focado = True)
        self.opcoes = botoes.Botao((x_botoes, 6*y_botoes), "Opções", "Terminal", tam_fonte, "White", (255,242,0), efeitos = efeitos)
        self.sair = botoes.Botao((x_botoes, 8*y_botoes), "Sair", "Terminal", tam_fonte, "White", (255,242,0), efeitos = efeitos)
        self.botoes = [self.jogar, self.opcoes, self.sair]

    def checar_eventos(self, evento = None):
        if evento == pygame.K_RETURN:
            match self.pos_botao:
                case 0:
                    return("selecao")
                case 1:
                    return("opcoes")
                case 2:
                    pygame.quit()
                    sys.exit()
                case _:
                    pass
        if self.jogar.mouse and pygame.mouse.get_pressed()[0]:
            return("selecao")
        if self.opcoes.mouse and pygame.mouse.get_pressed()[0]:
            return("opcoes")
        if self.sair.mouse and pygame.mouse.get_pressed()[0]:        
            pygame.quit()
            sys.exit()

    def draw(self):
        self.display.fill(self.cor)
        self.display.blit(self.imagem, self.rect)
        super().draw()
        self.display.blit(self.nome, self.nome_rect)

class opcoes(tela):
    def __init__(self, largura, altura, cor, musica, efeitos):
        super().__init__(largura, altura, cor)
        pygame.display.set_caption("Opções")
        
        self.fonte = pygame.font.SysFont("Terminal", self.largura//10)
        self.nome = self.fonte.render("Opcões", False, "White")
        self.nome_rect = self.nome.get_rect(center = (self.largura//2, self.altura//10))
        
        x_botoes = self.largura//2
        y_botoes = self.altura//10
        tam_fonte = altura//15
        tam_barras = (self.largura//3, 10)
        self.voltar : botoes.Botao = botoes.Botao((x_botoes, 9 * y_botoes), "Voltar", "Terminal", tam_fonte, "White", (255,242,0), efeitos = efeitos, focado = True)
        self.musica : botoes.Controle_desl = botoes.Controle_desl((3*self.largura//7, 4 * y_botoes), "Musica", "Terminal", tam_fonte, tam_barras, musica, (250, 250, 250))
        self.efeitos : botoes.Controle_desl = botoes.Controle_desl((3*self.largura//7, 6 * y_botoes), "Efeitos", "Terminal", tam_fonte, tam_barras, efeitos, (250, 250, 250))
        self.botoes = [self.voltar, self.musica, self.efeitos]

    def checar_eventos(self, evento = None):
        if evento == pygame.K_RETURN:
            match self.pos_botao:
                case 0:
                    return("voltar")
                case 1:
                    return("musica")
                case 2:
                    return("efeitos")
                case _:
                    pass
        if (self.voltar.mouse and pygame.mouse.get_pressed()[0]):
            return("voltar")
        if self.efeitos.destacado or self.efeitos.focado:
            return("efeitos")
        if self.musica.destacado or self.musica.focado:
            return("musica")

    def draw(self):
        self.display.fill(self.cor)
        super().draw()
        self.display.blit(self.nome, self.nome_rect)

    def atualizar(self):
        super().atualizar()
        self.volume_efeitos(self.atualizar_efeitos())

    def atualizar_musica(self):
        return(self.musica.ler_posicao())

    def atualizar_efeitos(self):
        return(self.efeitos.ler_posicao())
   
class seletor_jogo(tela):
    def __init__(self, largura, altura, cor, efeitos):
        super().__init__(largura, altura, cor)
        
        pygame.display.set_caption("Seleção")
        self.fonte = pygame.font.SysFont("Terminal", self.largura//10)
        self.nome = self.fonte.render("Selecione o mapa", False, "White")
        self.nome_rect = self.nome.get_rect(center = (self.largura//2, self.altura//10))
        x_botao = self.largura//2
        y_botao = self.altura//10
        tam_fonte = self.altura//15
        self.cenarios = botoes.Selecao_mapas(largura, altura,(255,242,0),efeitos)
        self.voltar : botoes.Botao = botoes.Botao((x_botao, 9 * y_botao), "Voltar", "Terminal", tam_fonte, "White", (255,242,0), efeitos = efeitos, focado = True)
        self.botoes = [self.voltar, self.cenarios]

    def checar_eventos(self, evento = None):
        if evento == pygame.K_RETURN:
            match self.pos_botao:
                case 0:
                    return("voltar")
                case _:
                    pass
        if (self.voltar.mouse and pygame.mouse.get_pressed()[0]):
            return("voltar")
        if (self.cenarios.mouse and pygame.mouse.get_pressed()[0]):
            print("cenarios")
        if (self.pos_botao == 0):
            self.cenarios.card_focado = 3*[False]
            self.cenarios.card_mouse = 3*[False]
    
    def atualizar(self):
        super().atualizar()
        self.cenarios.atualizar(self.display)
    
    def draw(self):
        self.display.fill(self.cor)
        super().draw()
        self.cenarios.display_botao(self.display)
        self.display.blit(self.nome, self.nome_rect)
