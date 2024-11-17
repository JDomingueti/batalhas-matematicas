import pygame, random
from . import evento

class bando_aguas_vivas(evento.evento):
    '''
    Atributos adicionais
    --------------------
    tamanho: tuple(int, int)

        Tamanho dos retângulos gerados no evento. Primeira posição indica
        o comprimento em x, e a segunda posição o comprimento em y
    
    y_inicio: int

        Posição y inicial do evento

    x_inicio: int

        Posição x inicial do evento
    
    imgs_agua_viva: List[pygame.SurfaceType]

        Lista contendo os sprites que os objetos do evento podem assumir

    velocidade_x: float

        Controla o movimento dos retângulos do evento na direção x

    afastamento: int

        Valor que indica a maior distância em y do atributo y_inicio que 
        os retângulos podem ser gerados

    quantidade_spawn: int

        Indica o número de objetos (retângulos) o evento irá gerar
        
    quantidade_spawnada: int

        Indica a quantidade de objetos que o evento já gerou

    separador_spawn: int

        Tempo utilizado para monitorar o intervalo de spawn

    tempo_spawn: int

        Valor que representa a quantidade de milisegundos entre a 
        geração de cada objeto do evento

    vida: int

        Vida com a qual os objetos do evento são gerados
    
    vidas: List[int]

        Lista que contém a vida de cada objeto do evento

    agua_viva_rects: List[pygame.Rect]

        Lista que contém os retângulos de todos os objetos do evento

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
        - criar_agua_viva()
    '''
    def __init__(self, tela : pygame.SurfaceType, volume_efeitos : pygame.mixer.Sound):
        '''
        Inicializa um objeto da classe eventos_oceanos.bandos_aguas_vivas
        '''
        super().__init__(tela, volume_efeitos)
        self.tamanho = (self.largura_tela//15, self.altura_tela//8)
        self.y_inicio = random.randint(self.altura_tela//7, 6*self.altura_tela//7)
        self.x_inicio = self.largura_tela + self.tamanho[0] if (self.lado_inicio == -1) else -2*self.tamanho[0]
        self.imgs_agua_viva = []
        for i in [1,2,3,4]:
            img = pygame.image.load(self.caminho + f"agua_viva/{i}.png")
            img = pygame.transform.scale(img, (self.tamanho[0], self.tamanho[1]))
            self.imgs_agua_viva.append(img)
        self.velocidade_x = random.randint(4,6) * self.lado_inicio
        self.afastamento = self.altura_tela//7
        self.quantidade_spawn = random.randint(5,8)
        self.quantidade_spawnada = 0
        self.separador_spawn = pygame.time.get_ticks()
        self.tempo_spawn = 400
        self.vida = 40
        self.vidas = []
        self.agua_viva_rects = []
        self.imgs = []
        self.frame_atual = 0
        self.frame_por_sprite = 30
        self.som = pygame.mixer.Sound(self.caminho + "sons/bolhas1.mp3")
        tamanho_aviso = (self.largura_tela/20, self.altura_tela/10)
        posicao_aviso = (self.largura_tela - 2*tamanho_aviso[0] if (self.lado_inicio == -1) else tamanho_aviso[0], self.y_inicio - tamanho_aviso[1]/2)
        self.rect_aviso = pygame.Rect(posicao_aviso, tamanho_aviso)
        self.img_aviso = pygame.transform.scale(pygame.image.load(self.caminho + "agua_viva/aviso.png"), tamanho_aviso)

    def desenhar(self):
        self.aviso_direcao()
        if len(self.agua_viva_rects) > 0:
            for pos, agua_viva in enumerate(self.agua_viva_rects):
                img = self.imgs_agua_viva[self.imgs[pos]]
                self.tela.blit(img, agua_viva)

    def atualizar(self):
        super().atualizar()
        if self.frame_atual >= 30:
            for i in range(len(self.imgs)):
                self.imgs[i] += 1
                self.imgs[i] %= 4
            self.frame_atual = 0
        if (self.comecou and ((pygame.time.get_ticks() - self.contador) > 2000)):
            if len(self.agua_viva_rects) < self.quantidade_spawn:
                if ((pygame.time.get_ticks() - self.separador_spawn) > self.tempo_spawn):
                    if self.quantidade_spawnada < self.quantidade_spawn:
                        self.criar_agua_viva()
                        self.separador_spawn = pygame.time.get_ticks()
            if len(self.agua_viva_rects) > 0:
                for agua_viva in self.agua_viva_rects:
                    agua_viva.centerx += self.velocidade_x
        self.frame_atual += 1

    def criar_agua_viva(self):
        '''
        Método utilizado para criar os objetos do evento (água-viva)
        '''
        y_atual = self.y_inicio + random.randint(-self.afastamento, self.afastamento)
        agua_viva = pygame.rect.Rect(self.x_inicio, y_atual, self.tamanho[0], self.tamanho[1])
        self.agua_viva_rects.append(agua_viva)
        self.vidas.append(self.vida)
        self.imgs.append(random.randint(0,3))
        self.quantidade_spawnada += 1

    def verificar_colisao(self, rect_obj : pygame.Rect, dano: int):
        colidiu = False
        for pos, rect in enumerate(self.agua_viva_rects):
            if rect.colliderect(rect_obj):
                self.vidas[pos] = max(self.vidas[pos] - dano, 0)
                colidiu = True
        return colidiu

    def matar(self, callback):
        if len(self.agua_viva_rects) > 0:
            for pos, agua_viva in enumerate(self.agua_viva_rects):
                if ((agua_viva.right < -2 * self.tamanho[0]) or (agua_viva.left > (self.largura_tela + 2 * self.tamanho[0]))):
                    self.agua_viva_rects.pop(pos)
                    self.vidas.pop(pos)
                    self.imgs.pop(pos)
                elif (self.vidas[pos] == 0):
                    callback(self.agua_viva_rects[pos])
                    self.agua_viva_rects.pop(pos)
                    self.vidas.pop(pos)
                    self.imgs.pop(pos)
        elif ((self.quantidade_spawnada > 0) and (len(self.vidas) == 0)):
            self.som.fadeout(100)
            return True
        return False

    def pegar_rect(self):
        return self.agua_viva_rects

class caranguejo(evento.evento):
    '''
    Atributos adicionais
    --------------------
    tamanho: tuple(int, int)

        Tamanho do retângulo principal gerado no evento. Primeira posição
        indica o comprimento em x, e a segunda posição o comprimento em y
    
    tamanho_garras: tuple(int, int)

        Tamanho dos retângulos secundários gerados no evento. Primeira 
        posição indica o comprimento em x, e a segunda posição o 
        comprimento em y
    
    x_inicio: int

        Posição x inicial do evento
    
    x_fim: int

        Posição x final do evento

    y_inicio: int

        Posição y inicial do evento

    velocidade_x: float

        Controla o movimento dos retângulos do evento na direção x

    caranguejo_rect: pygame.Rect

        Retângulo principal

    garra_esquerda_rect: pygame.Rect

        Retângulo secundário esquerdo padrão

    garra_direita_rect: pygame.Rect
        
        Retângulo secundário direito padrão

    garra_esquerda_rect_atual: pygame.Rect

        Retângulo secundário esquerdo que está sendo observado
    
    garra_direita_rect_atual: pygame.Rect

        Retângulo secundário direito que está sendo observado

    imgs_corpo: pygame.SurfaceType

        Lista de sprites do retângulo principal do evento

    imgs_esquerda: pygame.SurfaceType

        Lista de sprites do retângulo secundário esquerdo no tamanho 
        padrão

    imgs_esquerda_est: pygame.SurfaceType

        Lista de sprites do retângulo secundário esquerdo no tamanho 
        escalado
 
    imgs_direita: pygame.SurfaceType

        Lista de sprites do retângulo secundário direito no tamanho 
        padrão
    
    imgs_direita_est: pygame.SurfaceType
    
        Lista de sprites do retângulo secundário direito no tamanho 
        padrão

    escalar: float

        Valor na qual a próxima garra será escalada

    contador_garras: int

        Valor em milisegundos para alteração nos retângulos secundários

    garra_esticada: bool

        Booleano que indica se há um retângulo secundário escalado

    prox_garra: int

        Valor que indica qual será a próxima garra a ser escalada. Caso
        seja igual a 1, a próxima garra é a esquerda, caso seja -1 a
        próxima garra é a direita

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
    '''
    def __init__(self, tela: pygame.SurfaceType, volume_efeitos : pygame.mixer.Sound):
        '''
        Inicializa um objeto da classe eventos_oceano.caranguejo
        '''
        super().__init__(tela, volume_efeitos)

        self.vida = 300
        self.tamanho = (self.largura_tela//4, self.altura_tela//5)
        self.tamanho_garras = (2*self.tamanho[1]//3, self.tamanho[1])

        self.x_inicio = -2 * self.tamanho[0] if (self.lado_inicio == 1) else self.largura_tela + self.tamanho[0]
        self.x_fim = self.largura_tela if (self.lado_inicio == 1) else -self.tamanho[0]
        self.y_inicio = self.altura_tela - self.tamanho[1]

        self.velocidade_x = random.randint(3,6) * self.lado_inicio

        self.caranguejo_rect = pygame.rect.Rect(self.x_inicio, self.y_inicio, self.tamanho[0], self.tamanho[1])
        self.garra_esquerda_rect = pygame.rect.Rect(0, 0, 2*self.tamanho[1]//3, self.tamanho[1])
        self.garra_esquerda_rect.bottomright = (self.caranguejo_rect.left + self.tamanho[0]//4, self.caranguejo_rect.centery + self.tamanho[1]//8)
        self.garra_direita_rect = pygame.rect.Rect(0, 0, 2*self.tamanho[1]//3, self.tamanho[1])
        self.garra_direita_rect.bottomleft = (self.caranguejo_rect.right - self.tamanho[0]//4, self.caranguejo_rect.centery + self.tamanho[1]//8)

        self.garra_esquerda_rect_atual = self.garra_esquerda_rect 
        self.garra_direita_rect_atual = self.garra_direita_rect

        self.imgs_corpo = []
        self.imgs_esquerda = []
        self.imgs_esquerda_est = []
        self.imgs_direita = []
        self.imgs_direita_est = []
        for i in [1,2]:
            self.imgs_corpo.append(pygame.transform.scale(pygame.image.load(self.caminho + f"caranguejo/corpo/{i}.png"), self.tamanho))
            self.imgs_esquerda.append(pygame.transform.scale(pygame.image.load(self.caminho + f"caranguejo/garra_e/g_{i}.png"), self.tamanho_garras))
            self.imgs_esquerda_est.append(pygame.transform.scale(pygame.image.load(self.caminho + f"caranguejo/garra_e/g_e_{i}.png"), self.tamanho_garras))
            self.imgs_direita.append(pygame.transform.flip(self.imgs_esquerda[i-1], 1, 0))
            self.imgs_direita_est.append(pygame.transform.flip(self.imgs_esquerda_est[i-1], 1, 0))
        
        # Valor que vai aumentar a garra na próxima "esticada"
        self.escalar = 1
        self.contador_garras = pygame.time.get_ticks()
        self.garra_esticada = False
        # Garra 1 -> Esquerda; Garra -1 -> Direita
        self.prox_garra = 1    
        # Sprites: [Garra_esquerda, Corpo, Garra_direita, Garra_estendida]
        self.sprites_atuais = [0, 0, 0, 0]
        self.frame_atual = 0
        self.frames_por_sprites = 30
        self.som = pygame.mixer.Sound(self.caminho + "sons/caranguejo1.mp3")

        tamanho_aviso = (self.largura_tela/20, self.altura_tela/10)
        posicao_aviso = (self.largura_tela - 2*tamanho_aviso[0] if (self.lado_inicio == -1) else tamanho_aviso[0], self.y_inicio - tamanho_aviso[1]/2)
        self.rect_aviso = pygame.Rect(posicao_aviso, tamanho_aviso)
        self.img_aviso = pygame.transform.scale(pygame.image.load(self.caminho + "caranguejo/aviso.png"), tamanho_aviso)

    def desenhar(self):
        self.aviso_direcao()
        if self.garra_esticada:
            if self.prox_garra == -1:
                surf = self.imgs_esquerda_est[self.sprites_atuais[3]]
                surf = pygame.transform.scale(surf, self.garra_esquerda_rect_atual.size)
                self.tela.blit(surf, self.garra_esquerda_rect_atual)
                self.tela.blit(self.imgs_direita[self.sprites_atuais[2]], self.garra_direita_rect)
            else:
                surf = self.imgs_direita_est[self.sprites_atuais[3]]
                surf = pygame.transform.scale(surf, self.garra_direita_rect_atual.size)
                self.tela.blit(self.imgs_esquerda[self.sprites_atuais[0]], self.garra_esquerda_rect)
                self.tela.blit(surf, self.garra_direita_rect_atual)
        else:
            self.tela.blit(self.imgs_esquerda[self.sprites_atuais[0]], self.garra_esquerda_rect)
            self.tela.blit(self.imgs_direita[self.sprites_atuais[2]], self.garra_direita_rect)
        self.tela.blit(self.imgs_corpo[self.sprites_atuais[1]], self.caranguejo_rect)

    def atualizar(self):
        super().atualizar()
        if self.frame_atual >= self.frames_por_sprites:
            for i in range(3):
                self.sprites_atuais[i] = (self.sprites_atuais[i] + 1) % 2
            self.frame_atual = 0

        if (self.comecou and ((pygame.time.get_ticks() - self.contador) >= 2000)):
            if self.garra_esticada and pygame.time.get_ticks() - self.contador_garras > 250:
                self.sprites_atuais[3] = 1
            self.caranguejo_rect.centerx += self.velocidade_x
            self.garra_esquerda_rect_atual.centerx += self.velocidade_x
            self.garra_direita_rect_atual.centerx += self.velocidade_x

            if pygame.time.get_ticks() - self.contador_garras > 500:
                if not self.garra_esticada:
                    self.escalar = random.randint(180,200)/100
                    if self.prox_garra == 1:
                        baixo_direita = self.garra_esquerda_rect_atual.bottomright
                        self.garra_esquerda_rect_atual = self.garra_esquerda_rect.scale_by(1, self.escalar)
                        self.garra_esquerda_rect_atual.bottomright = baixo_direita
                    else:
                        baixo_esquerda = self.garra_direita_rect_atual.bottomright
                        self.garra_direita_rect_atual = self.garra_esquerda_rect.scale_by(1, self.escalar)
                        self.garra_direita_rect_atual.bottomright = baixo_esquerda

                    self.sprites_atuais[3] = 0
                    self.prox_garra = 1 if (self.prox_garra == -1) else -1
                else:
                    if self.prox_garra == -1:
                        baixo_direita = self.garra_esquerda_rect_atual.bottomright
                        self.garra_esquerda_rect_atual = self.garra_esquerda_rect
                        self.garra_esquerda_rect_atual.bottomright = baixo_direita
                    else:
                        baixo_esquerda = self.garra_direita_rect_atual.bottomleft
                        self.garra_direita_rect_atual = self.garra_direita_rect
                        self.garra_direita_rect_atual.bottomleft = baixo_esquerda
                self.contador_garras = pygame.time.get_ticks()
                self.garra_esticada = not(self.garra_esticada)

        self.frame_atual += 1

    def verificar_colisao(self, rect_obj : pygame.Rect, dano: int):
        colidiu = False
        for parte in [self.garra_esquerda_rect_atual, self.caranguejo_rect, self.garra_direita_rect_atual]:
            if parte.colliderect(rect_obj):
                colidiu = True
                self.vida = max(self.vida - dano, 0)
        return colidiu

    def matar(self, callback):
        if (self.vida == 0):
            self.som.fadeout(500)
            callback(self.caranguejo_rect)
            return True
        if (((self.caranguejo_rect.right < -2 * self.tamanho[0])) or (self.caranguejo_rect.left > (self.largura_tela + 2 * self.tamanho[0]))):
            self.som.fadeout(500)
            return True
        return False

    def pegar_rect(self):
        return [self.garra_esquerda_rect_atual, self.caranguejo_rect, self.garra_direita_rect_atual]

class tubarao(evento.evento):
    '''
    Atributos adicionais
    --------------------
    tamanho: tuple(int, int)

        Tamanho dos retângulos gerados no evento. Primeira posição indica
        o comprimento em x, e a segunda posição o comprimento em y
    
    y_inicio: int
    
        Posição y inicial do evento

    x_inicio: int

        Posição x inicial do evento

    x_fim: int

        Posição x final do evento
    
    imgs_tubarao: List[pygame.SurfaceType]

        Lista contendo os sprites que os objetos do evento podem assumir

    vida: int

        Vida com a qual os objetos do evento são gerados

    tubarao_rect: pygame.Rect

        Retângulos do objeto do evento

    afastamento_max: int

        Valor máximo que o centro do retângulo do evento pode se afastar
        do atributo y_inicio
        
    velocidade_x: float

        Controla o movimento dos retângulos do evento na direção x
        
    velocidade_y: float

        Controla o movimento dos retângulos do evento na direção y

    adicao_velocidade_y : float

        Aceleração da retângulo em y

    sprite_atual: int

        Indica o sprite que deve ser exibido

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
    '''
    def __init__(self, tela: pygame.Surface, volume_efeitos : pygame.mixer.Sound):
        '''
        Inicializa um objeto da classe eventos_oceano.tubarao
        '''
        super().__init__(tela, volume_efeitos)
        self.tamanho = (self.largura_tela//3, self.altura_tela//4)
        self.y_inicio = self.altura_tela//2
        self.x_inicio = -2 * self.tamanho[0] if (self.lado_inicio == 1) else self.largura_tela + self.tamanho[0]
        self.x_fim = self.largura_tela if self.lado_inicio == 1 else -self.tamanho[0]
        self.imgs_tubarao = []
        for i in range(1, 9):
            img = pygame.image.load(self.caminho + f"tubarao/{i}.png")
            img = pygame.transform.scale(img, self.tamanho)
            if (self.lado_inicio == -1):
                img = pygame.transform.flip(img, 1, 0)
            self.imgs_tubarao.append(img)
        self.vida = 400
        self.tubarao_rect = pygame.rect.Rect(self.x_inicio, self.y_inicio - self.tamanho[1]//2, self.tamanho[0], self.tamanho[1])
        self.afastamento_max = random.randint(self.altura_tela//10, self.altura_tela//5)
        self.velocidade_x = 5*self.lado_inicio
        self.velocidade_y = 0
        self.adicao_velocidade_y = random.choice([-1,1])*(random.randint(self.afastamento_max//2, self.afastamento_max))/self.altura_tela
        self.sprite_atual = 0
        self.frame_atual = 0
        self.frames_por_sprites = 30
        self.som = pygame.mixer.Sound(self.caminho + "sons/tubarao.mp3")
        tamanho_aviso = (self.largura_tela/20, self.altura_tela/10)
        posicao_aviso = (self.largura_tela - 2*tamanho_aviso[0] if (self.lado_inicio == -1) else tamanho_aviso[0], self.y_inicio - tamanho_aviso[1]/2)
        self.rect_aviso = pygame.Rect(posicao_aviso, tamanho_aviso)
        self.img_aviso = pygame.transform.scale(pygame.image.load(self.caminho + "tubarao/aviso.png"), tamanho_aviso)

    def desenhar(self):
        self.aviso_direcao()
        self.tela.blit(self.imgs_tubarao[self.sprite_atual], self.tubarao_rect)

    def atualizar(self):
        super().atualizar()
        if self.frame_atual >= self.frames_por_sprites:
            self.sprite_atual += 1
            self.sprite_atual %= 8
            self.frame_atual = 0
        if (self.comecou and ((pygame.time.get_ticks() - self.contador) >= 2000)):
            self.tubarao_rect.centerx += self.velocidade_x
            self.tubarao_rect.centery -= self.velocidade_y
            if (self.lado_inicio == -1 and self.tubarao_rect.left <= self.largura_tela) or (self.lado_inicio == 1 and self.tubarao_rect.right >= 0):
                if self.tubarao_rect.centery <= self.y_inicio - self.afastamento_max:
                    if self.adicao_velocidade_y > 0:
                        self.adicao_velocidade_y *= -1
                if self.tubarao_rect.centery >= self.y_inicio + self.afastamento_max:
                    if self.adicao_velocidade_y < 0:
                        self.adicao_velocidade_y *= -1
                self.velocidade_y += self.adicao_velocidade_y

        self.frame_atual += 1
    
    def verificar_colisao(self, rect_obj : pygame.Rect, dano: int):
        if self.tubarao_rect.colliderect(rect_obj):
            self.vida = max(self.vida - dano, 0)   
            return True

    def matar(self, callback):
        if (self.vida == 0):
            self.som.fadeout(500)
            callback(self.tubarao_rect)
            return True
        if ((self.tubarao_rect.right < -2 * self.tamanho[0]) or (self.tubarao_rect.left > (self.largura_tela + 2 * self.tamanho[0]))):
            self.som.fadeout(500)
            return True
        return False

    def pegar_rect(self):
        return [self.tubarao_rect]
