import pygame
pygame.font.init()

# TODO: Estilizar

'''
Arquivo de códigos criado com o intuito de armazenar
as linhas de código dos botões utilizados na interface
gráfica do jogo.
'''

class padrao:
    '''
    Classe criada para ser tomada por herança, com métodos
    e atributos comuns a mais de um tipo de botão.
    '''
    def __init__(self, pos, texto, fonte, tamanho_texto, cor_principal, cor_destaque, efeitos = 0.3, focado = False):
        '''
        Método que carrega e ajusta as configurações iniciais 
        e comuns a mais de um tipo de botão, 

        Parâmetros
        ----------
        pos: List[int]
            Lista que indica a posição inicial do texto. O
            primeiro valor é atribuído ao eixo x e o 
            segundo ao eixo y

        texto: str
            Indica o texto que será escrito no botão

        fonte: str
            Indica qual fonte do sistema será utilizada
        
        tamanho_texto: int
            Indica o tamanho da fonte utilizada
        
        cor_principal: ColorValue
            Indica a cor padrão do texto do botão. Pode
            ser passada como valor em texto (Ex: 'White')
            ou em valor RGB (Ex: (255,255,255))

        cor_destaque: ColorValue
            Indica a cor utilizada quando o botão está
            em destaque. Pode ser passada da mesma
            maneira que o parâmetro cor_principal

        efeitos: float
            Valor entre 0 e 1 que indica o volume inicial
            do efeito do botão.
        
        focado: bool
            Caso passado como True o botão é carregado 
            inicialmente já com destaque
        '''
        # Conversão das posições passadas como parâmetros para atributos
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        # Bolleanos para controle de movimento e destaque
        self.focado = focado
        self.mouse = False
        self.destacado = False
        # Cores das letras do texto
        self.cor = cor_principal
        self.cor_destaque = cor_destaque
        # Carregamento inicial do texto predefinido
        self.texto = texto
        self.fonte = pygame.font.SysFont(fonte, tamanho_texto)
        self.texto_render = self.fonte.render(self.texto, False, self.cor)
        # Estrelas desenhadas ao lado dos botões
        self.estrelas = []
        for i in range(4):
            self.estrelas.append(pygame.image.load(f"../assets/sprites/estrela_{i+1}.png"))
            self.estrelas[i] = pygame.transform.scale(self.estrelas[i], (30, 30))
        # Contador de frames para animação das estrelas
        self.frames_por_estrela = 15
        self.contador_frames = 0
        self.frame_atual = 0
        # Carregamento do som de efeito do botão
        self.som = pygame.mixer.Sound("../assets/movimento_menu.wav")
        self.som.set_volume(efeitos)
        
    def atualizar(self):
        '''
        Método comum aos botões que tem como função
        parte da animação dos botões em destaque
        '''
        if self.contador_frames >= self.frames_por_estrela:
            self.contador_frames %= self.frames_por_estrela
            self.frame_atual = (self.frame_atual + 1) % 4
        self.contador_frames += 1

class Botao(padrao):
    '''
    Botão de clique
    '''
    def __init__(self, pos, texto, fonte, tamanho_texto, cor_principal, cor_destaque, efeitos = 0.3, focado = False):
        super().__init__(pos, texto, fonte, tamanho_texto, cor_principal, cor_destaque, efeitos, focado)
        # Valores utilizados na animação do botão em destaque
        self.x_inicial = self.x_pos
        self.direcao = 0.1
        # Ajuste da posição do texto
        self.texto_rect = self.texto_render.get_rect(center = (self.x_pos, self.y_pos))

    def display_botao(self, tela: pygame.SurfaceType):
        '''
        Método que desenha o botão na superfície passada
        como parâmetro.
        Caso o botão possua o atributo `destacado` com o
        valor `True`, o botão é impresso com a cor de 
        destaque e com estrelas animadas ao seu lado.

        Parâmetros
        ----------
        tela: pygame.SurfaceType
            Superfície na qual o botão será impresso
        '''
        if self.destacado:
            texto_render = self.fonte.render(self.texto, False, self.cor_destaque)
            tela.blit(self.estrelas[self.frame_atual], (self.texto_rect.left - 40, self.texto_rect.centery - 15))
            tela.blit(self.estrelas[self.frame_atual], (self.texto_rect.right + 10, self.texto_rect.centery - 15))
        else:
            texto_render = self.fonte.render(self.texto, False, self.cor)
        self.texto_rect = texto_render.get_rect(center = (self.x_pos, self.y_pos))
        tela.blit(texto_render, self.texto_rect)

    def atualizar(self):
        '''
        Método que verifica se o botão deve ser destacado
        com base na posição do mouse e no atributo `focado`,
        que é atualizado pelo código que criou o botão.
        '''
        super().atualizar()
        
        self.mouse = self.texto_rect.collidepoint(pygame.mouse.get_pos())
        if self.focado or self.mouse:
            if not self.destacado:
                self.destacado = True
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
            if (self.x_pos != self.x_inicial):
                if self.x_pos > self.x_inicial:
                    self.direcao = -0.1
                if self.x_pos < self.x_inicial:
                    self.direcao = 0.1
                self.x_pos += self.direcao

class Controle_desl(padrao):
    '''
    Controle deslizante
    '''
    def __init__(self, pos, texto, fonte, tamanho_texto, tamanho_barra, percent, cor_principal, cor_destaque = (255,242,0), efeitos = 0.3, focado = False):
        '''
        Controle que permite ajustar um parâmetro em uma
        escala de porcentagem de 1 a 100. Utiliza a classe
        de configurações como herança.
        
        Parâmetros
        ----------
        tamanho_barra: List[int]
            Lista com dois itens que indicam o tamanho da
            barra a ser criada. Primeiro valor indica a 
            largura e o segundo a altura

        percent: float
            Número que informa qual o percentual em que o
            controle deslizante deve ser inicializado
        '''
        super().__init__(pos, texto, fonte, tamanho_texto, cor_principal, cor_destaque, efeitos, focado)
        # Configurações básicas da barra e do controle deslizante
        self.barra_largura = tamanho_barra[0]
        self.barra_altura = tamanho_barra[1]
        self.barra = pygame.rect.Rect(self.x_pos + 10, self.y_pos - self.barra_altura//2, self.barra_largura, self.barra_altura)
        self.tamanho_controle = 2 * self.barra_altura
        self.old_percent = percent
        self.percent = percent
        self.controle_x = self.barra.left + self.percent * self.barra_largura
        self.controle = pygame.rect.Rect(self.controle_x, self.y_pos - self.tamanho_controle//2, self.tamanho_controle, self.tamanho_controle)
        # Ajuste de posição do texto
        tamanho_texto = self.texto_render.get_size()[0]//2
        self.texto_rect = self.texto_render.get_rect(center = (self.x_pos - tamanho_texto - 10, self.y_pos))
        
    def display_botao(self, tela: pygame.SurfaceType):
        '''
        Método que desenha o botão na superfície passada
        como parâmetro.
        Caso o botão possua o atributo `destacado` com o
        valor `True`, o controle deslizante e o texto que
        se refere a ele são destacados no valor passado 
        como `cor_destaque` e são adicionados os efeitos
        de menu.

        Parâmetros
        ----------
        tela: pygame.SurfaceType
            Superfície na qual o botão será impresso
        '''
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

    def atualizar(self):
        '''
        Método que verifica se o botão deve ser destacado
        com base na posição do mouse e no atributo `focado`,
        que é atualizado pelo código que criou o botão.
        '''
        super().atualizar()
        if self.old_percent != self.percent:
            pygame.mixer.Sound.play(self.som)
            self.old_percent = self.percent
        if self.percent >= 1:
            self.percent = 1
        elif self.percent <= 0:
            self.percent = 0
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
        else:
            self.destacado = False
            self.mouse = False

    def ler_posicao(self):
        '''
        Função destinada a retornar a porcentagem da barra
        em que o controle deslizante se encontra.

        Return
        ------
        float
            Número entre 0 e 1 que indica a porcentagem em
            representação decimal do parâmetro controlado.
        '''
        pos_inicio = self.barra.left
        pos_controle = self.controle.left
        posicao = (pos_controle - pos_inicio) / (self.barra_largura - self.tamanho_controle) 
        return posicao

class Selecao_mapas:
    '''
    Botão predefinido com o seletor de mapas. Gera por 
    definição 3 cards onde cada um leva a um cenário de jogo
    '''
    def __init__(self, largura, altura, cor_destaque, efeitos):
        '''
        Configurações para criação dos cards

        Parameters
        ----------
        largura: int
            Largura da tela na qual o card será desenhado
        
        altura: int
            Altura da tela na qual o card será desenhado

        cor_destaque: ColorValue
            Atributo de cor que indica a cor de realce do
            card quando estiver sendo destacado. Pode ser
            passado como str indicando a cor (Ex:'Black')
            ou como tupla de valores RGB (Ex:(0,0,0)).

        efeitos: float
            Valor entre 0 e 1 que determina o volume dos
            sons de efeitos dos cards
        '''
        # Atributos de tamanhos para posicionamento e criação dos cards
        self.largura_tela = largura
        self.altura_tela = altura
        self.espacamento = self.largura_tela//25
        self.altura_cards = self.altura_tela//2
        self.largura_cards = (self.largura_tela - 4 * self.espacamento)//3
        # Cards a serem desenhados na tela
        caminho = "../assets/fundos/cards/card_{0}.png"
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
        # Atributos utilizados para destaque e controle de foco dos cards
        self.cor_destaque = cor_destaque
        self.num_card_destacado = 0
        self.destacado = False
        self.mouse = False
        self.focado = False
        self.card_destacado = 3 * [False]
        self.card_focado = 3 * [False]
        self.card_mouse = 3 * [False]
        # Sons de efeitos dos cards
        self.som = pygame.mixer.Sound("../assets/movimento_menu.wav")
        self.som.set_volume(efeitos)
    
    def display_botao(self, tela:pygame.SurfaceType):
        '''
        Método que desenha os cards na tela passada como
        parâmetro. Caso algum card esteja destacado é
        desenhado também um retângulo na cor do atributo
        `self.cor_destaque` no fundo.

        Parâmetros
        ----------
        tela: pygame.SurfaceType
            Tela a ser utilizada
        '''
        if any(self.card_destacado):
            esquerda = self.card_rects[self.num_card_destacado].left - 5
            topo = self.card_rects[self.num_card_destacado].top - 5
            largura =  self.largura_cards + 10
            altura = self.altura_cards + 10
            ret_fundo = pygame.rect.Rect(esquerda, topo, largura, altura)
            pygame.draw.rect(tela, self.cor_destaque, ret_fundo)
        # Desenha os 3 cards
        for i in range(3):
            tela.blit(self.cards[i], self.card_rects[i])

    def atualizar(self):
        '''
        Método que verifica se algum dos três cards deve
        ser destacado
        '''
        if (self.num_card_destacado <= 0):
            self.num_card_destacado = 0
        elif (self.num_card_destacado >= 2):
            self.num_card_destacado = 2
        for num, card in enumerate(self.card_rects):
            self.card_mouse[num] = card.collidepoint(pygame.mouse.get_pos())
            if self.card_mouse[num] or self.card_focado[num]:
                self.mouse = any(self.card_mouse)
                if not(self.card_destacado[num]):
                    # Caso haja um card focado diferente do atual (mas com mouse)
                    # ele é desfocado para dar ênfase ao mouse 
                    if self.focado and not(self.card_focado[num]):
                        self.card_focado = 3 * [False]
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
