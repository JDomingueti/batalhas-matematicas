import pygame, random
from . import evento

class cometa(evento.evento):
    '''
    Atributos adicionais
    --------------------
    tamanho: tuple(int, int)

        Tupla que indica o tamanho do retângulo do evento

    x_inicio: int

        Posição x inicial do evento

    x_fim: int

        Posição x final do evento

    velocidade_y: float

        Controla o movimento do retângulo do evento na direção y

    velocidade_x: float

        Controla o movimento do retângulo do evento na direção x

    vida: int

        Vida do evento

    cometa_rect: pygame.Rect

        Retângulo na qual o evento está inserido

    cometa_imgs: List[pygame.SurfaceType]

        Lista com os sprites do evento

    sprite_atual: int

        Controla o sprite que está sendo exibido    
    
    frames_por_sprite: int

        Duração em frames de cada sprite 

    frame_atual: int

        Variável para controle de frames do evento

    som: pygame.mixer.Sound

        Som que o evento toca

    angulo: float

        Ângulo em que o evento será desenhado (em relação ao vetor (0,1))

    img_aviso: pygame.Surface

        Imagem do aviso gerado quando o evento é criado

    rect_aviso: pygame.Rect

        Retângulo na qual será gerado a imagem de aviso do evento
    '''
    def __init__(self, tela: pygame.Surface, volume_efeitos):
        '''
        Inicializa um objeto da classe eventos_espaco.cometa
        '''
        super().__init__(tela, volume_efeitos)
        self.tamanho = (self.largura_tela//7, self.largura_tela//5)
        self.x_inicio = random.randint(0, self.largura_tela//2) if self.lado_inicio == 1 else random.randint(self.largura_tela//2, self.largura_tela) 
        self.x_fim = random.randint(self.largura_tela//2, self.largura_tela) if self.lado_inicio == 1 else random.randint(0, self.largura_tela//2)
        tempo_em_tela = random.randint(5,10)*10
        self.velocidade_y = self.altura_tela//tempo_em_tela
        self.velocidade_x = (self.x_fim - self.x_inicio)//tempo_em_tela
        self.vida = 200
        self.dano = 15
        self.cometa_rect = pygame.rect.Rect(self.x_inicio, -2*self.tamanho[1], self.tamanho[0], self.tamanho[1])
        self.cometa_imgs = []
        for i in range(1,5):
            img = pygame.image.load(self.caminho + f"cometa/{i}.png")
            img = pygame.transform.scale(img, (self.tamanho[0], self.tamanho[1]))
            self.cometa_imgs.append(img)
        self.sprite_atual = 0
        self.frames_por_sprite = 15
        self.frame_atual = 0
        self.angulo = 0
        self.som = pygame.mixer.Sound(self.caminho + "sons/fireball.mp3")
        self.angulo = pygame.Vector2(self.velocidade_x, self.velocidade_y).angle_to(pygame.Vector2(0, 1))
        tamanho_aviso = (self.largura_tela/20, self.altura_tela/10)
        posicao_aviso = (self.x_inicio, tamanho_aviso[1]/2)
        img_aviso = pygame.transform.scale(pygame.image.load(self.caminho + "cometa/aviso.png"), tamanho_aviso)
        self.img_aviso = pygame.transform.rotate(img_aviso, self.angulo)
        self.rect_aviso = pygame.Rect(posicao_aviso, self.img_aviso.get_size())

    def atualizar(self):
        super().atualizar()
        if self.frame_atual >= self.frames_por_sprite:
            self.sprite_atual += 1
            self.sprite_atual %= 4
            self.frame_atual = 0
        if (self.comecou and ((pygame.time.get_ticks() - self.contador) >= 2500)):
            if (self.cometa_rect.bottom >= 0):
                self.cometa_rect.centerx += self.velocidade_x
            self.cometa_rect.centery += self.velocidade_y
        self.frame_atual += 1

    def desenhar(self):
        self.aviso_direcao()
        centro = self.cometa_rect.center
        img = pygame.transform.rotate(self.cometa_imgs[self.sprite_atual], self.angulo)
        rect = img.get_rect()
        rect.center = centro
        self.tela.blit(img, rect)

    def verificar_colisao(self, rect_obj : pygame.Rect, dano: int):
        if self.cometa_rect.colliderect(rect_obj):
            if (pygame.time.get_ticks() - self.separador_dano) > self.intervalo_dano:
                self.vida = max(self.vida - dano, 0)
                self.separador_dano = pygame.time.get_ticks()
            return True
        return False

    def matar(self, callback):
        if self.cometa_rect.top > self.altura_tela or self.vida == 0:
            self.som.fadeout(1000)
            if self.vida == 0:
                callback(self.cometa_rect)
            return True
        return False

    def pegar_rect(self):
        return [self.cometa_rect]

class invasores_do_espaco(evento.evento):
    '''
    Atributos adicionais
    --------------------
    tamanho: tuple(int, int)

        Tupla que indica o tamanho do retângulo do evento

    velocidade_y: float

        Controla o movimento do retângulo do evento na direção y
    
    num_linhas: int

        Indica o número de linhas de espaçonaves menores serão geradas
    
    num_colunas: int

        Indica o número de colunas de espaçonaves menores serão geradas

    x_inicio: int

        Posição x inicial do evento
        
    tamanho_x: int

        Comprimento em x dos inimigos menores

    espacamento_x: int

        Distância em x entre cada um dos inimigos menores

    tamanho_y: int

        Comprimento em y dos inimigos menores

    espacamento_y: int

        Distância em y entre cada um dos inimigos menores
    
    tamanho_nave: tuple(int, int)

        Tupla com o tamanho da nave maior. Primeiro valor indica o 
        comprimento em x e o segundo valor o comprimento em y
    
    matriz_inimigos: List[List[pygame.Rect]]

        Matriz que contém o retângulo referente a cada inimigo menor

    vida: int

        Vida dos inimigos pequenos do evento

    vidas_inimigos: List[List[int]]

        Matriz que contém a vida de cada inimigo pequeno

    img_linha_1: List[pygame.SurfaceType]

        Lista com os sprites da linha 1 da matriz de inimigos pequenos

    img_linha_2: List[pygame.SurfaceType]

        Lista com os sprites da linha 2 da matriz de inimigos pequenos
    
    img_linha_3: List[pygame.SurfaceType]

        Lista com os sprites das linhas maiores ou iguais a 3 da matriz
        de inimigos pequenos
    
    img_nave_antiga: pygame.SurfaceType

        Sprite da nave maior

    vida_nave: int

        Vida da nave maior

    nave_antiga_rect: pygame.Rect

        Retângulo da nave maior

    sprite_atual: int

        Controla o sprite que está sendo exibido    
    
    frames_por_sprite: int

        Duração em frames de cada sprite 

    frame_atual: int

        Variável para controle de frames do evento

    som: pygame.mixer.Sound

        Som que o evento toca

    img_aviso: pygame.Surface

        Imagem do aviso gerado quando o evento é criado

    rect_aviso: pygame.Rect

        Retângulo na qual será gerado a imagem de aviso do evento

    Método adicional
    ----------------
        - criar_inimigos()
    '''
    def __init__(self, tela: pygame.Surface, volume_efeitos : float):
        '''
        Inicializa um objeto da classe eventos_espaco.invasores_do_espaco
        '''
        super().__init__(tela, volume_efeitos)
        self.velocidade_y = 3
        self.num_linhas = 3
        self.num_colunas = 5
        self.x_inicio = self.largura_tela//2
        self.tamanho_x = (self.largura_tela//3 - self.largura_tela//12)//self.num_colunas
        self.espacamento_x = (self.largura_tela//3 -self.num_colunas * self.tamanho_x)//(self.num_colunas + 1)
        self.tamanho_y = 2*self.tamanho_x // 3
        self.espacamento_y = self.tamanho_y // 3
        self.tamanho_nave = (self.tamanho_x*2, self.tamanho_y)
        self.matriz_inimigos = [[],[],[]]
        self.vida = 3
        self.dano = 8
        self.vidas_inimigos = [[],[],[]]
        self.img_linha_1 = []
        self.img_linha_2 = []
        self.img_linha_3 = []
        for i in [1, 2]:
            self.img_linha_1.append(pygame.transform.scale(pygame.image.load(self.caminho + f"space/inimigo1/{i}.png"), (self.tamanho_x, self.tamanho_y)))
            self.img_linha_2.append(pygame.transform.scale(pygame.image.load(self.caminho + f"space/inimigo2/{i}.png"), (self.tamanho_x, self.tamanho_y)))
            self.img_linha_3.append(pygame.transform.scale(pygame.image.load(self.caminho + f"space/inimigo3/{i}.png"), (self.tamanho_x, self.tamanho_y)))
        self.img_nave_antiga = pygame.transform.scale(pygame.image.load(self.caminho + "space/nave.png"), self.tamanho_nave)            
        self.vida_nave = 6
        self.nave_antiga_rect = pygame.Rect
        self.separador_dano = 50
        self.criar_inimigos()

        self.sprite_atual = 0
        self.frames_por_sprite = 30
        self.frame_atual = 0
        self.som = pygame.mixer.Sound(self.caminho + "sons/space3.mp3")
        tamanho_aviso = (self.largura_tela/20, self.altura_tela/10)
        posicao_aviso = (self.largura_tela/2 - tamanho_aviso[0]/2, tamanho_aviso[1])
        self.img_aviso = pygame.transform.scale(pygame.image.load(self.caminho + "space/aviso.png"), tamanho_aviso)
        self.rect_aviso = pygame.Rect(posicao_aviso, tamanho_aviso)

    def criar_inimigos(self):
        for i in range(self.num_linhas):
            for j in range(self.num_colunas):
                pos_x = self.largura_tela//3 + (j + 1) * self.espacamento_x + j * self.tamanho_x
                pos_y =  - (i + 1) * self.espacamento_y - (i + 2) * self.tamanho_y
                inimigo = pygame.rect.Rect(pos_x, pos_y, self.tamanho_x, self.tamanho_y)
                self.matriz_inimigos[i].append(inimigo)
                self.vidas_inimigos[i].append(self.vida)
        pos_x = self.largura_tela//3 + (self.num_colunas + 1) * self.espacamento_x + (self.num_colunas + 1) * self.tamanho_x
        pos_y =  - (2 * self.num_linhas + 4) * self.espacamento_y - (self.num_linhas + 2) * self.tamanho_y
        if self.nave_antiga_rect != None:
            self.nave_antiga_rect = pygame.rect.Rect(self.largura_tela//2 - self.tamanho_nave[0]//2, pos_y, self.tamanho_nave[0], self.tamanho_nave[1])

    def desenhar(self):
        self.aviso_direcao()
        for i, linha in enumerate(self.matriz_inimigos):
            for inimigo in linha:
                if i == 0:
                    self.tela.blit(self.img_linha_1[self.sprite_atual], inimigo)
                elif i == 1:
                    self.tela.blit(self.img_linha_2[self.sprite_atual], inimigo)
                else:
                    self.tela.blit(self.img_linha_3[self.sprite_atual], inimigo)
        if self.nave_antiga_rect != None:
            self.tela.blit(self.img_nave_antiga, self.nave_antiga_rect)

    def atualizar(self):
        super().atualizar()
        if self.frame_atual >= self.frames_por_sprite:
            self.sprite_atual += 1
            self.sprite_atual %= 2
            self.frame_atual = 0
        if (self.comecou and ((pygame.time.get_ticks() - self.contador) >= 2500)):
            for linha in self.matriz_inimigos:
                for inimigo in linha:
                    inimigo.centery += self.velocidade_y
            if self.nave_antiga_rect != None:
                self.nave_antiga_rect.centery += self.velocidade_y
        self.frame_atual += 1

    def verificar_colisao(self, rect_obj : pygame.Rect, dano: int):
        colidiu = False
        for i, linha in enumerate(self.matriz_inimigos):
            for j, rect in enumerate(linha):
                if rect.colliderect(rect_obj):
                    colidiu = True
                    if (pygame.time.get_ticks() - self.separador_dano) >= self.intervalo_dano:
                        self.vidas_inimigos[i][j] = max(self.vidas_inimigos[i][j] - dano, 0)
                        self.separador_dano = pygame.time.get_ticks()
        if self.nave_antiga_rect != None:
            if self.nave_antiga_rect.colliderect(rect_obj):
                colidiu = True
                if (pygame.time.get_ticks() - self.separador_dano) >= self.intervalo_dano:
                    self.vida_nave = max(self.vida_nave - dano, 0)
                    self.separador_dano = pygame.time.get_ticks()
        return colidiu

    def matar(self, callback):
        if self.vida_nave == 0:
            callback(self.nave_antiga_rect)
            self.nave_antiga_rect = None
        for i, linha in enumerate(self.matriz_inimigos):
            for j, rect in enumerate(linha):
                if self.vidas_inimigos[i][j] == 0:
                    self.vidas_inimigos[i].pop(j)
                    self.matriz_inimigos[i].pop(j)
                    callback(rect)
                if len(self.matriz_inimigos[i]) == 0:
                    self.matriz_inimigos.pop(i)
                    self.vidas_inimigos.pop(i)
        if self.comecou:
            if self.nave_antiga_rect == None and len(self.matriz_inimigos) == 0:
                callback(self.nave_antiga_rect)
                self.som.fadeout(500)
                return True
            elif self.nave_antiga_rect != None and self.nave_antiga_rect.top > self.altura_tela:
                self.som.fadeout(500)
                return True
            elif len(self.matriz_inimigos) > 0:
                if self.matriz_inimigos[len(self.matriz_inimigos) - 1][0].top > self.altura_tela:
                    self.matriz_inimigos.clear()
        return False

    def pegar_rect(self):
        rects = [self.nave_antiga_rect]
        (rects.append(inimigo) for inimigo in (linha for linha in self.matriz_inimigos))
        return rects