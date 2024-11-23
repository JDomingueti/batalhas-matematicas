import pygame, random
from . import evento
from math import sin

class bola_de_feno(evento.evento):
<<<<<<< HEAD
    def __init__(self, tela: pygame.SurfaceType, volume_efeitos : pygame.mixer.Sound):
=======
    '''
    Atributos adicionais
    --------------------
    tamanho: int

        Tamanho do lado do quadrado do evento
    
    y_inicio: int

        Posição y inicial do evento

    x_inicio: int

        Posição x inicial do evento

    velocidade_y: float

        Controla o movimento do retângulo do evento na direção y

    velocidade_x: float

        Controla o movimento do retângulo do evento na direção x

    aux_y: float

        Variável criada para auxílio no controle da rotação da imagem

    bola_de_feno: pygame.SurfaceType

        Sprite utilizado no evento

    bole_de_feno_rect: pygame.Rect

        Retângulo na qual o evento está inserido

    vida: int

        Vida do evento

    sprite_atual: int

        Controla o sprite que está sendo exibido    
    
    frames_por_sprite: int

        Duração em frames de cada sprite 

    frame_atual: int

        Variável para controle de frames do evento

    som: pygame.mixer.Sound

        Som que o evento toca

    rect_aviso: pygame.Rect

        Retângulo na qual será gerado a imagem de aviso do evento

    img_aviso: pygame.Surface

        Imagem do aviso
    '''
    def __init__(self, tela: pygame.SurfaceType, volume_efeitos : float):
        '''
        Inicializa um objeto do tipo eventos_deserto.bola_de_feno
        '''
>>>>>>> dea53f1aa41b5a56d9244fb01550c69627a4841c
        super().__init__(tela, volume_efeitos)
        self.tamanho = self.largura_tela//10
        self.y_inicio = random.randint(self.altura_tela//4, 3*self.altura_tela//4)
        self.x_inicio = -2*self.tamanho if (self.lado_inicio == 1) else self.largura_tela + self.tamanho
        self.velocidade_y = 0
        self.velocidade_x = random.randint(4,7) * self.lado_inicio
        self.aux_y = 0

<<<<<<< HEAD
        self.imgs = []
        for i in range(1,5):
            self.imgs.append(pygame.transform.scale(pygame.image.load(self.caminho + f"bola_de_feno/{i}.png"), (self.tamanho, self.tamanho)))
        self.bola_de_feno = pygame.image.load(self.caminho + "bola_de_feno/1.png")
        self.bola_de_feno = pygame.transform.scale(self.bola_de_feno, (self.tamanho, self.tamanho))
        self.bola_de_feno_rect = self.imgs[0].get_rect()
=======
        self.bola_de_feno = pygame.image.load(self.caminho + "bola_de_feno/1.png")
        self.bola_de_feno = pygame.transform.scale(self.bola_de_feno, (self.tamanho, self.tamanho))
        self.bola_de_feno_rect = self.bola_de_feno.get_rect()
>>>>>>> dea53f1aa41b5a56d9244fb01550c69627a4841c
        self.bola_de_feno_rect.topleft = (self.x_inicio - self.tamanho//2, self.y_inicio - self.tamanho//2)
        self.vida = 80
        self.sprite_atual = 0
        self.frames_por_sprite = 30
        self.frame_atual = 0
        self.som = pygame.mixer.Sound(self.caminho + "sons/vento.mp3")
        tamanho_aviso = (self.largura_tela/20, self.altura_tela/10)
        posicao_aviso = (self.largura_tela - self.tamanho/2 if (self.lado_inicio == -1) else self.tamanho/2, self.y_inicio - tamanho_aviso[1]/2)
        self.rect_aviso = pygame.Rect(posicao_aviso, tamanho_aviso)
        self.img_aviso = pygame.transform.scale(pygame.image.load(self.caminho + "bola_de_feno/aviso.png"), tamanho_aviso)
<<<<<<< HEAD
=======
        
>>>>>>> dea53f1aa41b5a56d9244fb01550c69627a4841c

    def atualizar(self):
        super().atualizar()
        if self.frame_atual >= self.frames_por_sprite:
            self.sprite_atual += self.lado_inicio
            self.sprite_atual %= 4
            self.frame_atual = 0
        if (self.comecou and ((pygame.time.get_ticks() - self.contador) > 2000)):
            if self.bola_de_feno_rect.right > 0 and self.bola_de_feno_rect.left < self.largura_tela: 
                self.bola_de_feno_rect.centery += 2*self.velocidade_x*sin(self.aux_y)
            self.bola_de_feno_rect.centerx += self.velocidade_x
            self.aux_y += 0.1
        self.frame_atual += 1

    def desenhar(self):
        self.aviso_direcao()        
        centro = self.bola_de_feno_rect.center
        img = pygame.transform.rotate(self.bola_de_feno, -10*self.velocidade_x*self.lado_inicio*self.aux_y/2)
        rect = img.get_rect()
        rect.center = centro
        self.tela.blit(img, rect)

    def verificar_colisao(self, rect_obj : pygame.Rect, dano: int):
        if self.bola_de_feno_rect.colliderect(rect_obj):
            self.vida = max(self.vida - dano, 0)
            return True

    def matar(self, callback):
        if ((self.bola_de_feno_rect.right < -2 * self.tamanho) or (self.bola_de_feno_rect.left > (self.largura_tela + 2 * self.tamanho))):
            self.som.fadeout(500)
            return True
        elif self.vida == 0:
            callback(self.bola_de_feno_rect)
            self.som.fadeout(500)
            return True
        return False

    def pegar_rect(self):
        return [self.bola_de_feno_rect]

class nuvem_gafanhotos(evento.evento):
<<<<<<< HEAD
    def __init__(self, tela: pygame.Surface, volume_efeitos : pygame.mixer.Sound):
=======
    '''
    Atributos adicionais
    --------------------
    tamanho: int

        Tamanho do lado de um quadrado do evento
    
    y_inicio: int

        Posição y inicial do evento

    x_inicio: int

        Posição x inicial do evento
        
    velocidade_x: float

        Controla o movimento do retângulo do evento na direção x

    metade_y_tela: int

        Indica em qual metade (em altura) da tela o evento ocorrerá
        1 -> Metade superior
        2 -> Metade inferior

    quantidade_maxima: int

        Indica o número de objetos (retângulos) o evento irá gerar
        
    quantidade_spawnada: int

        Indica a quantidade de objetos que o evento já gerou

    gafanhotos_imgs: List[pygame.SurfaceType]

        Lista com os sprites dos objetos do evento

    separador_gafanhotos: int

        Valor que representa a quantidade de milisegundos entre a 
        geração de cada objeto do evento

    gafanhotos_rects: List[pygame.Rect]

        Lista que contém os retângulos de todos os objetos do evento

    vidas: List[int]

        Lista que contém a vida de cada objeto do evento

    imgs: List[pygame.Surface]

        Lista que contém o sprite de cada retângulo do evento

    frame_atual: int

        Variável para controle de frames do evento
    
    frames_por_sprite: int

        Duração em frames de cada sprite 

    som: pygame.mixer.Sound

        Som que o evento toca

    rect_aviso: pygame.Rect

        Retângulo na qual será gerado a imagem de aviso do evento

    img_aviso: pygame.Surface

        Imagem do aviso

    Método adicional
    ----------------
        - criar_gafanhoto()
    '''
    def __init__(self, tela: pygame.Surface, volume_efeitos : float):
        '''
        Inicializa um objeto do tipo eventos_deserto.nuvem_gafanhotos
        '''
>>>>>>> dea53f1aa41b5a56d9244fb01550c69627a4841c
        super().__init__(tela, volume_efeitos)
        self.tamanho = 20
        self.vida = 10
        self.velocidade_x = random.randint(4,8) * self.lado_inicio
        self.metade_y_tela = random.choice([1,2])
        self.x_inicio = self.largura_tela + self.tamanho if self.lado_inicio == -1 else -2 * self.tamanho
        self.y_inicio = self.altura_tela//2 + self.altura_tela//4 * (-1 if self.metade_y_tela == 1 else 1)
        self.quantidade_maxima = random.randint(20,30)
        self.quantidade_spawnada = 0
        self.gafanhotos_imgs = []
        for i in range(1,5):
            self.gafanhotos_imgs.append(pygame.transform.scale(pygame.image.load(self.caminho + f"gafanhoto/{i}.png"), (self.tamanho, self.tamanho)))
            if (self.lado_inicio == 1):
                self.gafanhotos_imgs[i-1] = pygame.transform.flip(self.gafanhotos_imgs[i-1], 1, 0)
        self.separador_gafanhotos = pygame.time.get_ticks()
        self.gafanhotos_rects = []
        self.vidas = []
        self.imgs = []
        self.frame_atual = 0
        self.frames_por_sprite = 10
        self.som = pygame.mixer.Sound(self.caminho + "sons/gafanhoto2.mp3")
        tamanho_aviso = (self.largura_tela/20, self.altura_tela/10)
        posicao_aviso = (self.largura_tela - 2*tamanho_aviso[0] if (self.lado_inicio == -1) else tamanho_aviso[0], self.y_inicio - tamanho_aviso[1]/2)
        self.rect_aviso = pygame.Rect(posicao_aviso, tamanho_aviso)
        self.img_aviso = pygame.transform.scale(pygame.image.load(self.caminho + "gafanhoto/aviso.png"), tamanho_aviso)

    def atualizar(self):
        super().atualizar()
        if self.frame_atual >= self.frames_por_sprite:
            for pos in range(len(self.imgs)):
                self.imgs[pos] += 1
                self.imgs[pos] %= 4 
            self.frame_atual = 0
        if (self.comecou and (pygame.time.get_ticks() - self.contador >= 2000)):
            if self.quantidade_spawnada < self.quantidade_maxima:
                if (pygame.time.get_ticks() - self.separador_gafanhotos) > 2000/self.quantidade_maxima:
                    self.criar_gafanhoto()
                    self.separador_gafanhotos = pygame.time.get_ticks()
            for gafanhoto in self.gafanhotos_rects:
                gafanhoto.centerx += self.velocidade_x
        self.frame_atual += 1

    def desenhar(self):
<<<<<<< HEAD
        self.aviso_direcao
=======
        self.aviso_direcao()
>>>>>>> dea53f1aa41b5a56d9244fb01550c69627a4841c
        for pos, gafanhoto in enumerate(self.gafanhotos_rects):
            self.tela.blit(self.gafanhotos_imgs[self.imgs[pos]], gafanhoto)

    def criar_gafanhoto(self):
<<<<<<< HEAD
=======
        '''
        Método utilizado para criar os objetos do evento (gafanhotos)
        '''
>>>>>>> dea53f1aa41b5a56d9244fb01550c69627a4841c
        y_gafanhoto = self.y_inicio + random.randint(-self.altura_tela//4, self.altura_tela//4) - self.tamanho
        gafanhoto = pygame.rect.Rect(self.x_inicio, y_gafanhoto, self.tamanho, self.tamanho)
        self.gafanhotos_rects.append(gafanhoto)
        self.imgs.append(random.choice([1,2,3]))
        self.vidas.append(self.vida)
        self.quantidade_spawnada += 1

    def verificar_colisao(self, rect_obj : pygame.Rect, dano: int):
        colidiu = False
        for pos, rect in enumerate(self.gafanhotos_rects):
            if rect.colliderect(rect_obj):
                colidiu = True
                self.vidas[pos] = max(self.vidas[pos] - dano, 0)
        return colidiu

    def matar(self, callback):
        for pos, gafanhoto in enumerate(self.gafanhotos_rects):
            if ((gafanhoto.right < -2 * self.tamanho) or (gafanhoto.left > (self.largura_tela + 2 * self.tamanho))):
                self.gafanhotos_rects.pop(pos)
                self.vidas.pop(pos)
                self.imgs.pop(pos)
            elif (len(self.vidas) > 0):
                for pos, item in enumerate(self.vidas):
                    if item == 0:
                        callback(self.gafanhotos_rects[pos])
                        self.gafanhotos_rects.pop(pos)
                        self.imgs.pop(pos)
                        self.vidas.pop(pos)

        if ((len(self.gafanhotos_rects) == 0) and (self.quantidade_spawnada > 0)):
            self.som.fadeout(500)
            return True
        return False

    def pegar_rect(self):
        return self.gafanhotos_rects

class verme_da_areia(evento.evento):
<<<<<<< HEAD
    def __init__(self, tela: pygame.Surface, volume_efeitos : pygame.mixer.Sound):
=======
    '''
    Atributos adicionais
    --------------------
    tamanho: int

        Tamanho do lado de um quadrado do evento
    
    x_inicio: int

        Posição x inicial do evento

    x_fim: int

        Posição x final do evento

    velocidade_y_inicial: float

        Velocidade de movimento em y inicial do evento

    gravidade: float

        Valor com que a velocidade em y diminui
        
    velocidade_x: float

        Controla o movimento do retângulo do evento na direção x

    img_cabeca: pygame.Surface

        Sprite do retângulo na posição 0 da lista de retângulos

    img_corpo: pygame.Surface

        Sprites dos retângulos que não são o inicial ou final na lista
        de retângulos

    img_rabo: pygame.Surface

        Sprite do retângulo na última posição da lista de retângulos

    vetor_eixo: pygame.Vetor2
        
        Vetor para controle de rotação dos sprites

    tamanho_corpo: int

        Indica o número de objetos (retângulos) o evento irá gerar
        
    partes_criadas: int

        Indica a quantidade de objetos que o evento já gerou

    vida: int

        Indica a vida de cada objeto do evento
        
    verme_da_areia_rects: List[pygame.Rect]

        Lista que contém os retângulos de todos os objetos do evento

    verme_da_areia_vidas: List[int]

        Lista que contém a vida de cada objeto do evento

    velocidades_verme_da_areia: List[pygame.Vetor2]

        Lista com as velocidades de cada retângulo do evento

    separador_corpo: int

        Valor que representa a quantidade de milisegundos entre a 
        geração de cada retângulo do evento

    som: pygame.mixer.Sound

        Som que o evento toca

    rect_aviso: pygame.Rect

        Retângulo na qual será gerado a imagem de aviso do evento

    img_aviso: pygame.Surface

        Imagem do aviso
    '''
    def __init__(self, tela: pygame.Surface, volume_efeitos : float):
        '''
        Inicializa um objeto do tipo eventos_deserto.verme_da_areia
        '''
>>>>>>> dea53f1aa41b5a56d9244fb01550c69627a4841c
        super().__init__(tela, volume_efeitos)
        self.x_inicio = random.randint(0, self.largura_tela//3)
        self.x_fim = self.largura_tela - self.x_inicio
        self.tamanho = random.randint(40, 50)
        if self.lado_inicio == -1:
            temp = self.x_inicio
            self.x_inicio = self.x_fim
            self.x_fim = temp
        self.velocidade_y_inicial = random.randint(10, 15)
        self.gravidade = 0.2
<<<<<<< HEAD
        # Fórmula para achar o tempo em tela e calcular a velocidade em x
=======
        
>>>>>>> dea53f1aa41b5a56d9244fb01550c69627a4841c
        tempo_em_tela = (2*self.velocidade_y_inicial)/self.gravidade
        self.velocidade_x = (self.x_fim - self.x_inicio)/tempo_em_tela

        self.img_cabeca = pygame.image.load(self.caminho + "verme_da_areia/cabeca/1.png")
        self.img_cabeca = pygame.transform.scale(self.img_cabeca , (self.tamanho, self.tamanho))
        self.img_corpo = pygame.image.load(self.caminho + "verme_da_areia/corpo/1.png")
        self.img_corpo = pygame.transform.scale(self.img_corpo , (self.tamanho, self.tamanho))
        self.img_rabo = pygame.image.load(self.caminho + "verme_da_areia/rabo/1.png")
        self.img_rabo = pygame.transform.scale(self.img_rabo , (self.tamanho, self.tamanho))
        self.vetor_eixo = pygame.Vector2((0,1))

        self.tamanho_corpo = random.randint(8,12)
        self.partes_criadas = 0
        self.vida = 30
        self.verme_da_areia_rects = []
        self.verme_da_areia_vidas = []
        self.velocidades_verme_da_areia : list[pygame.Vector2]= []
        self.separador_corpo = pygame.time.get_ticks()
        self.som = pygame.mixer.Sound(self.caminho + "sons/Roar_1.mp3")

        tamanho_aviso = (self.largura_tela/20, self.altura_tela/10)
        posicao_aviso = (self.x_inicio - tamanho_aviso[0]/2, self.altura_tela - 2*tamanho_aviso[1])

        angulo = pygame.Vector2((self.velocidade_x, self.velocidade_y_inicial)).angle_to((0,1))
        img_aviso = pygame.transform.scale(pygame.image.load(self.caminho + "verme_da_areia/aviso.png"), tamanho_aviso)
        self.img_aviso = pygame.transform.rotate(img_aviso, -angulo)
        self.rect_aviso = (posicao_aviso, self.img_aviso.get_size())

    def atualizar(self):
        super().atualizar()
        if (self.comecou and (pygame.time.get_ticks() - self.contador > 2000)):
            if ((pygame.time.get_ticks() - self.separador_corpo > 45) and (self.partes_criadas < (self.tamanho_corpo))):
                    self.criar_corpo()
                    self.separador_corpo = pygame.time.get_ticks()
            for pos, verme_da_areia in enumerate(self.verme_da_areia_rects):
                if (pos == 0):
                    self.verme_da_areia_rects[pos].centerx += self.velocidades_verme_da_areia[pos][0]
                    self.verme_da_areia_rects[pos].centery -= self.velocidades_verme_da_areia[pos][1]
                    if verme_da_areia.centery < self.altura_tela:
                        self.som.set_volume(0)
                        self.velocidades_verme_da_areia[pos][0] = self.velocidade_x
                        self.velocidades_verme_da_areia[pos][1] -= self.gravidade
                    else:
                        self.som.set_volume(self.volume_efeitos)
                else:
                    self.verme_da_areia_rects[pos].centerx += self.velocidades_verme_da_areia[pos][0]
                    self.verme_da_areia_rects[pos].centery -= self.velocidades_verme_da_areia[pos][1]
                    if verme_da_areia.centery < self.altura_tela:
                        self.velocidades_verme_da_areia[pos][0] = self.velocidade_x
                        self.velocidades_verme_da_areia[pos][1] -= self.gravidade

    def desenhar(self):
        self.aviso_direcao()
        if (len(self.verme_da_areia_rects) > 0):
            for pos in range(1, len(self.verme_da_areia_rects)):
                centro = self.verme_da_areia_rects[pos].center
                angulo = self.velocidades_verme_da_areia[pos].angle_to(self.vetor_eixo)
                parte_rot = pygame.transform.rotate(self.img_corpo, -angulo)
                rect_rot = parte_rot.get_rect()
                rect_rot.center = centro
                self.tela.blit(parte_rot, rect_rot)
            for i in [len(self.verme_da_areia_rects)-1, 0]:
                centro = self.verme_da_areia_rects[i].center
                angulo = self.velocidades_verme_da_areia[i].angle_to(self.vetor_eixo)
                if i == 0:
                    parte_rot = pygame.transform.rotate(self.img_cabeca, -angulo)
                else:
                    parte_rot = pygame.transform.rotate(self.img_rabo, -angulo)
                rect_rot = parte_rot.get_rect()
                rect_rot.center = centro
                self.tela.blit(parte_rot, rect_rot)

    def criar_corpo(self):
        parte = pygame.rect.Rect(self.x_inicio-self.tamanho//2, self.altura_tela + self.tamanho, self.tamanho, self.tamanho)
        self.verme_da_areia_rects.append(parte)
        self.velocidades_verme_da_areia.append(pygame.Vector2(0, self.velocidade_y_inicial))
        self.verme_da_areia_vidas.append(self.vida)
        self.partes_criadas += 1

    def verificar_colisao(self, rect_obj : pygame.Rect, dano: int):
        colidiu = False
        for pos, rect in enumerate(self.verme_da_areia_rects):
            if rect.colliderect(rect_obj):
                colidiu = True
                self.verme_da_areia_vidas[pos] = max(self.verme_da_areia_vidas[pos] - dano, 0)
        return colidiu

    def matar(self, callback):
        matar_pos = []
        for pos in range(len(self.verme_da_areia_vidas)):
            if (self.verme_da_areia_vidas[pos] == 0):
                matar_pos.append(pos)
        if len(matar_pos) > 0:
            for pos in matar_pos:
                callback(self.verme_da_areia_rects[pos])
                self.verme_da_areia_rects.pop(pos)
                self.verme_da_areia_vidas.pop(pos)
                self.velocidades_verme_da_areia.pop(pos)
        if len(self.verme_da_areia_rects) > 0:
            for rect in self.verme_da_areia_rects:
                if rect.bottom > self.altura_tela + 2 * self.tamanho:
                    self.verme_da_areia_rects.remove(rect)
                elif ((rect.left > self.largura_tela) or (rect.right < 0)):
                    self.verme_da_areia_rects.remove(rect)
        if len(self.verme_da_areia_rects) == 0 and self.partes_criadas > 0:
            self.som.fadeout(100)
            return True
        else:
            return False

    def pegar_rect(self):
        return self.verme_da_areia_rects