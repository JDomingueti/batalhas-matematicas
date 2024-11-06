import pygame

# TODO: Estilizar

pygame.font.init()

class Botao:
    def __init__(self, pos, texto, fonte, tamanho, cor, cor_destaque, efeitos = 0.3, focado = False):
        self.x_pos = pos[0]
        self.x_inicial = self.x_pos
        self.y_pos = pos[1]
        
        self.focado = focado
        self.mouse = False
        self.destacado = False
        self.direcao = 0.1
        
        self.cor_original = cor
        self.cor = cor
        self.cor_destaque = cor_destaque
        
        self.texto = texto
        self.fonte = pygame.font.SysFont(fonte, tamanho)
        texto_render = self.fonte.render(self.texto, False, self.cor)
        self.texto_rect = texto_render.get_rect(center = (self.x_pos, self.y_pos))
        self.estrelas = []
        for i in range(4):
            self.estrelas.append(pygame.image.load(f"../assets/sprites/estrela_{i+1}.png"))
            self.estrelas[i] = pygame.transform.scale(self.estrelas[i], (30, 30))
        self.frames_por_estrela = 15
        self.contador_frames = 0
        self.frame_atual = 0
        self.som = pygame.mixer.Sound("../assets/movimento_menu.wav")
        self.som.set_volume(efeitos)
        
    def display_botao(self, tela: pygame.SurfaceType):
        
        if self.destacado:
            texto_render = self.fonte.render(self.texto, False, self.cor_destaque)
            tela.blit(self.estrelas[self.frame_atual], (self.texto_rect.left - 40, self.texto_rect.centery - 15))
            tela.blit(self.estrelas[self.frame_atual], (self.texto_rect.right + 10, self.texto_rect.centery - 15))
        else:
            texto_render = self.fonte.render(self.texto, False, self.cor)
        self.texto_rect = texto_render.get_rect(center = (self.x_pos, self.y_pos))
        tela.blit(texto_render, self.texto_rect)

    def atualizar(self, tela):
        if self.contador_frames >= self.frames_por_estrela:
            self.contador_frames %= self.frames_por_estrela
            self.frame_atual = (self.frame_atual + 1) % 4
        self.mouse = self.texto_rect.collidepoint(pygame.mouse.get_pos())
        if self.focado:
            if not self.destacado:
                self.destacado = True
                self.display_botao(tela)
                pygame.mixer.Sound.play(self.som, fade_ms= 2)
            self.x_pos += self.direcao
            if self.x_pos >= self.x_inicial + 2:
                self.direcao = -0.1
            elif self.x_pos <= self.x_inicial - 2:
                self.direcao = 0.1
        elif self.mouse:
            if not self.destacado:
                self.mouse = True
                self.destacado = True
                self.display_botao(tela)
                pygame.mixer.Sound.play(self.som, fade_ms= 2)
            self.x_pos += self.direcao
            if self.x_pos >= self.x_inicial + 2:
                self.direcao = -0.1
            elif self.x_pos <= self.x_inicial - 2:
                self.direcao = 0.1
        else:
            self.mouse = False
            if self.destacado:
                self.destacado = False
                self.display_botao(tela)
            if (self.x_pos != self.x_inicial):
                if self.x_pos > self.x_inicial:
                    self.direcao = -0.1
                if self.x_pos < self.x_inicial:
                    self.direcao = 0.1
                self.x_pos += self.direcao
        self.contador_frames += 1

class Controle_desl:
    def __init__(self, pos, texto, fonte, tamanho_texto, tamanho_barra, percent, cor, cor_destaque = (255,242,0), efeitos = 0.3, focado = False):
        self.x_pos = pos[0]
        self.y_pos = pos[1]

        self.barra_largura = tamanho_barra[0]
        self.barra_altura = tamanho_barra[1]
        self.barra = pygame.rect.Rect(self.x_pos + 10, self.y_pos - self.barra_altura//2, self.barra_largura, self.barra_altura)
        self.tamanho_controle = 2 * self.barra_altura
        self.percent = percent
        self.controle_x = self.barra.left + self.percent * self.barra_largura
        self.controle = pygame.rect.Rect(self.controle_x, self.y_pos - self.tamanho_controle//2, self.tamanho_controle, self.tamanho_controle)

        self.cor = cor
        self.cor_destaque = cor_destaque
        self.destacado = False
        self.mouse = False
        self.focado = focado
        
        self.texto = texto
        self.fonte = pygame.font.SysFont(fonte, tamanho_texto)
        self.texto_render = self.fonte.render(self.texto, False, self.cor)
        tamanho_texto = self.texto_render.get_size()[0]//2
        self.texto_rect = self.texto_render.get_rect(center = (self.x_pos - tamanho_texto - 10, self.y_pos))
        
        self.estrelas = []
        for i in range(4):
            self.estrelas.append(pygame.image.load(f"../assets/sprites/estrela_{i+1}.png"))
            self.estrelas[i] = pygame.transform.scale(self.estrelas[i], (30, 30))
        self.frames_por_estrela = 15
        self.contador_frames = 0
        self.frame_atual = 0
        
        self.som = pygame.mixer.Sound("../assets/movimento_menu.wav")
        self.som.set_volume(efeitos)
        
    def display_botao(self, tela: pygame.SurfaceType):
        if self.percent >= 1:
            self.percent = 1
        elif self.percent <= 0:
            self.percent = 0
        tela.blit(self.texto_render, self.texto_rect)
        pygame.draw.rect(tela, self.cor, self.barra)
        if self.destacado or self.focado:
            tela.blit(self.estrelas[self.frame_atual], (self.texto_rect.left - 40, self.barra.centery - 15))
            tela.blit(self.estrelas[self.frame_atual], (self.barra.right + 10, self.barra.centery - 15))
            self.texto_render = self.fonte.render(self.texto, False, self.cor_destaque)
            self.controle_x = self.barra.left + self.percent * (self.barra_largura - self.tamanho_controle)
            self.controle = pygame.rect.Rect(self.controle_x, self.y_pos - self.tamanho_controle//2, self.tamanho_controle, self.tamanho_controle)
            pygame.draw.rect(tela, self.cor_destaque, self.controle)
        else:
            self.texto_render = self.fonte.render(self.texto, False, self.cor)
            self.controle_x = self.barra.left + self.percent * (self.barra_largura - self.tamanho_controle)
            self.controle = pygame.rect.Rect(self.controle_x, self.y_pos - self.tamanho_controle//2, self.tamanho_controle, self.tamanho_controle)
            pygame.draw.rect(tela, self.cor, self.controle)

    def atualizar(self, tela: pygame.SurfaceType):
        if self.contador_frames >= self.frames_por_estrela:
            self.contador_frames %= self.frames_por_estrela
            self.frame_atual = (self.frame_atual + 1) % 4
        if self.controle.collidepoint(pygame.mouse.get_pos()) or self.focado:
            if not self.destacado:
                self.destacado = True
                pygame.mixer.Sound.play(self.som, fade_ms= 2)
            if not self.focado:
                self.mouse = True
            if any(pygame.mouse.get_pressed()):
                novo_x = pygame.mouse.get_pos()[0] - self.tamanho_controle//2
                if novo_x <= self.barra.left:
                    novo_x = self.barra.left
                elif novo_x >= self.barra.right - self.tamanho_controle:
                    novo_x = self.barra.right - self.tamanho_controle
                self.percent = (novo_x - self.barra.left) / (self.barra_largura - self.tamanho_controle)
                self.display_botao(tela)
        else:
            self.destacado = False
            self.mouse = False
        self.contador_frames += 1

    def ler_posicao(self):
        pos_inicio = self.barra.left
        pos_controle = self.controle.left
        posicao = (pos_controle - pos_inicio) / (self.barra_largura - self.tamanho_controle) 
        return posicao

class Selecao_mapas:
    '''
    Botão predefinido com o seletor de mapas
    Gera por definição 3 cards onde cada um 
    leva a um cenário de jogo
    '''
    def __init__(self, largura, altura, cor_destaque, efeitos):
        self.largura_tela = largura
        self.altura_tela = altura
        self.som = pygame.mixer.Sound("../assets/movimento_menu.wav")
        self.som.set_volume(efeitos)
        caminho = "../assets/fundos/cards/card_{0}.png"
        self.espacamento = self.largura_tela//25
        self.altura_cards = self.altura_tela//2
        self.largura_cards = (self.largura_tela - 4 * self.espacamento)//3
        
        self.card_oceano = pygame.image.load(caminho.format('oceano'))
        self.card_oceano = pygame.transform.scale(self.card_oceano, (self.largura_cards, self.altura_cards))
        self.card_deserto = pygame.image.load(caminho.format('deserto'))
        self.card_deserto = pygame.transform.scale(self.card_deserto, (self.largura_cards, self.altura_cards))
        self.card_espaco = pygame.image.load(caminho.format('espaco'))
        self.card_espaco = pygame.transform.scale(self.card_espaco, (self.largura_cards, self.altura_cards))
        self.cards = [self.card_oceano, self.card_deserto, self.card_espaco]
        self.card_rects = []
        for i in range(3):
            posx = (i+1)*self.espacamento + i * self.largura_cards
            posy = self.altura_tela//4
            self.card_rects.append(pygame.rect.Rect(posx, posy, self.largura_cards, self.altura_cards))

        self.num_card_destacado = 0
        self.cor_destaque = cor_destaque
        self.destacado = False
        self.mouse = False
        self.focado = False
        self.card_destacado = 3 * [False]
        self.card_focado = 3 * [False]
        self.card_mouse = 3 * [False]
    
    def display_botao(self, tela:pygame.Surface):
        if any(self.card_destacado):
            esquerda = self.card_rects[self.num_card_destacado].left - 5
            topo = self.card_rects[self.num_card_destacado].top - 5
            largura =  self.largura_cards + 10
            altura = self.altura_cards + 10
            ret_fundo = pygame.rect.Rect(esquerda, topo, largura, altura)
            pygame.draw.rect(tela, self.cor_destaque, ret_fundo)

        for i in range(3):
            tela.blit(self.cards[i], self.card_rects[i])

    def atualizar(self, tela: pygame.SurfaceType):
        if (self.num_card_destacado <= 0):
            self.num_card_destacado = 0
        elif (self.num_card_destacado >= 2):
            self.num_card_destacado = 2
        for num, card in enumerate(self.card_rects):
            self.card_mouse[num] = card.collidepoint(pygame.mouse.get_pos())
            if self.card_mouse[num] or self.card_focado[num]:
                self.mouse = any(self.card_mouse)
                if not(self.card_destacado[num]):
                    if not(self.card_focado[num]):
                        self.card_focado = 3 * [False]
                    # self.card_destacado = 3 * [False]
                    self.card_destacado[num] = True
                    self.destacado = True
                    self.num_card_destacado = num
                    pygame.mixer.Sound.play(self.som, fade_ms= 2)
                elif not self.mouse:
                    self.focado = True
            else:
                self.card_destacado[num] = False
                self.card_mouse[num] = False
        if not(any(self.card_mouse) or any(self.card_focado)):
            self.destacado = False
            self.focado = False
            self.mouse = False
