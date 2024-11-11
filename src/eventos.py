import pygame, random
from abc import ABC, abstractmethod
from math import sin

''' Arquivo para implementação dos eventos dos cenários '''

class evento(ABC):
    @abstractmethod
    def __init__(self, tela: pygame.Surface):
        self.largura_tela = tela.get_width()
        self.altura_tela = tela.get_height()
        self.tela = tela
        self.comecou = False
        self.lado_inicio = random.choice([-1,1])
        self.contador = pygame.time.get_ticks()
        self.caminho = "../assets/eventos/"

    @abstractmethod
    def aviso_direcao(self):
        pass

    @abstractmethod
    def atualizar(self):
        pass

    @abstractmethod
    def desenhar(self):
        pass
    
    @abstractmethod
    def verificar_colisao(self, rect_obj : pygame.Rect, dano: int):
        pass
    
    @abstractmethod
    def matar(self):
        pass

class tubarao(evento):
    def __init__(self, tela: pygame.Surface):
        super().__init__(tela)
        self.tamanho = (self.largura_tela//3, self.altura_tela//4)
        self.y_inicio = self.altura_tela//2
        self.x_inicio = -2 * self.tamanho[0] if (self.lado_inicio > 0) else self.largura_tela + self.tamanho[0]
        self.caminho += "tubarao/"
        self.imgs_tubarao = []
        for i in range(1, 9):
            self.imgs_tubarao.append(pygame.transform.scale(pygame.image.load(self.caminho + f"{i}.png"), self.tamanho))
            if (self.lado_inicio == -1):
                self.imgs_tubarao[i-1] = pygame.transform.flip(self.imgs_tubarao[i-1], 1, 0)
        self.vida = 500
        self.tubarao_rect = pygame.rect.Rect(self.x_inicio, self.y_inicio - self.tamanho[1]//2, self.tamanho[0], self.tamanho[1])
        self.afastamento_max = random.randint(self.altura_tela//10, self.altura_tela//5)
        self.velocidade_x = 5*self.lado_inicio
        self.velocidade_y = 0
        self.adicao_velocidade_y = random.choice([-1,1])*(random.randint(self.afastamento_max//2, self.afastamento_max))/self.altura_tela
        self.frame_atual = 0
        self.sprite_atual = 0
        self.frames_por_sprites = 20
        
    def aviso_direcao(self):
        if self.comecou and pygame.time.get_ticks() - self.contador <= 2500:
            x_aviso = self.largura_tela - 30 if (self.lado_inicio == -1) else 30
            aviso = pygame.rect.Rect(x_aviso, self.y_inicio - 3, 6, 30)
            pygame.draw.rect(self.tela, (255,0,0), aviso)
    
    def desenhar(self):
        self.aviso_direcao()
        self.tela.blit(self.imgs_tubarao[self.sprite_atual], self.tubarao_rect)

    def atualizar(self):
        if self.frame_atual >= self.frames_por_sprites:
            self.sprite_atual += 1
            self.sprite_atual %= 8
            self.frame_atual = 0
        if not self.comecou:
            self.contador = pygame.time.get_ticks()
            self.comecou = True
        elif pygame.time.get_ticks() - self.contador >= 2000:
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

    def matar(self):
        if (self.vida == 0):
            return True
        if ((self.lado_inicio == 1) and (self.tubarao_rect.left > self.largura_tela)):
            return True
        elif ((self.lado_inicio == -1) and (self.tubarao_rect.right < 0)):
            return True
        return False

class caranguejo(evento):
    def __init__(self, tela: pygame.SurfaceType):
        super().__init__(tela)
        
        self.vida = 1000
        self.tamanho = (self.largura_tela//4, self.altura_tela//5)
        self.tamanho_garras = (2*self.tamanho[1]//3, self.tamanho[1])

        self.x_inicio = -2 * self.tamanho[0] if (self.lado_inicio == 1) else self.largura_tela + self.tamanho[0]
        self.y_inicio = self.altura_tela - self.tamanho[1]
        
        self.velocidade_x = random.randint(3,6) * self.lado_inicio

        self.caranguejo_rect = pygame.rect.Rect(self.x_inicio, self.y_inicio, self.tamanho[0], self.tamanho[1])
        self.garra_esquerda_rect = pygame.rect.Rect(0, 0, 2*self.tamanho[1]//3, self.tamanho[1])
        self.garra_esquerda_rect.bottomright = (self.caranguejo_rect.left + self.tamanho[0]//4, self.caranguejo_rect.centery + self.tamanho[1]//8)
        self.garra_direita_rect = pygame.rect.Rect(0, 0, 2*self.tamanho[1]//3, self.tamanho[1])
        self.garra_direita_rect.bottomleft = (self.caranguejo_rect.right - self.tamanho[0]//4, self.caranguejo_rect.centery + self.tamanho[1]//8)

        self.garra_esquerda_rect_atual = self.garra_esquerda_rect 
        self.garra_direita_rect_atual = self.garra_direita_rect

        self.caminho += "caranguejo/"
        self.imgs_corpo = []
        self.imgs_esquerda = []
        self.imgs_esquerda_est = []
        self.imgs_direita = []
        self.imgs_direita_est = []
        for i in [1,2]:
            self.imgs_corpo.append(pygame.transform.scale(pygame.image.load(self.caminho + f"corpo/{i}.png"), self.tamanho))
            self.imgs_esquerda.append(pygame.transform.scale(pygame.image.load(self.caminho + f"garra_e/g_{i}.png"), self.tamanho_garras))
            self.imgs_esquerda_est.append(pygame.transform.scale(pygame.image.load(self.caminho + f"garra_e/g_e_{i}.png"), self.tamanho_garras))
            self.imgs_direita.append(pygame.transform.flip(self.imgs_esquerda[i-1], 1, 0))
            self.imgs_direita_est.append(pygame.transform.flip(self.imgs_esquerda_est[i-1], 1, 0))
        
        # Valor que vai aumentar a garra na próxima "esticada"
        self.escalar = 1
        self.contador_garras = pygame.time.get_ticks()
        self.garra_esticada = False
        # Garra 1 -> Esquerda; Garra -1 -> Direita
        self.prox_garra = 1    
        # [Garra_esquerda, Corpo, Garra_direita, Garra_estendida]
        self.sprites_atuais = [0, 0, 0, 0]
        self.frames_por_sprites = 30
        self.frame_atual = 0

    def aviso_direcao(self):
        if (self.comecou and (pygame.time.get_ticks() - self.contador <= 2500)):
            x_aviso = self.largura_tela - 30 if (self.lado_inicio == -1) else 30
            aviso = pygame.rect.Rect(x_aviso, self.y_inicio - 3, 6, 30)
            pygame.draw.rect(self.tela, (255,0,0), aviso)

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
        if not self.comecou:
            self.contador = pygame.time.get_ticks()
            self.comecou = True
        if self.frame_atual >= self.frames_por_sprites:
            for i in range(3):
                self.sprites_atuais[i] = (self.sprites_atuais[i] + 1) % 2
            self.frame_atual = 0
            
    
        elif pygame.time.get_ticks() - self.contador >= 2000:
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

    def matar(self):
        if (self.vida == 0):
            return True
        if ((self.lado_inicio == 1) and (self.caranguejo_rect.left > self.largura_tela)):
            return True
        elif ((self.lado_inicio == -1) and (self.caranguejo_rect.right < 0)):
            return True
        return False

class bando_aguas_vivas(evento):
    def __init__(self, tela : pygame.SurfaceType):
        super().__init__(tela)
        self.tamanho = (self.largura_tela//15, self.altura_tela//8)
        self.y_inicio = random.randint(self.altura_tela//7, 6*self.altura_tela//7)
        self.quantidade_spawn = random.randint(5,8)
        self.x_inicio = self.largura_tela + 30 if (self.lado_inicio == -1) else -60
        self.max_velocidade_x = random.randint(4,6)
        self.imgs_agua_viva = []
        self.caminho += "agua_viva/"
        for i in [1,2,3,4]:
            self.imgs_agua_viva.append(pygame.transform.scale(pygame.image.load(self.caminho + f"{i}.png"), (self.tamanho[0], self.tamanho[1])))
        self.velocidade_x = 0
        self.incremento_velocidade_x = 1/2
        self.afastamento = self.altura_tela//7
        self.separador_spawn = pygame.time.get_ticks()
        self.quantidade_spawnada = 0
        self.vida = 30
        self.vidas = []
        self.agua_viva_rects = []
        self.imgs = []
        self.frame_por_sprite = 30
        self.frame_atual = 0

    def aviso_direcao(self):
        if (self.comecou and (pygame.time.get_ticks() - self.contador <= 2500)):
            x_aviso = self.largura_tela - 30 if (self.lado_inicio == -1) else 30
            aviso = pygame.rect.Rect(x_aviso, self.y_inicio - 3, 6, 30)
            pygame.draw.rect(self.tela, (77,77,189), aviso)
    
    def desenhar(self):
        self.aviso_direcao()
        if len(self.agua_viva_rects) > 0:
            for pos, agua_viva in enumerate(self.agua_viva_rects):
                img = self.imgs_agua_viva[self.imgs[pos]]
                self.tela.blit(img, agua_viva)
        
    def atualizar(self):
        if self.frame_atual >= 30:
            for i in range(len(self.imgs)):
                self.imgs[i] += 1
                self.imgs[i] %= 4
            self.frame_atual = 0
        if not self.comecou:
            self.contador = pygame.time.get_ticks()
            self.comecou = True
        else:
            if len(self.agua_viva_rects) < self.quantidade_spawn:
                if ((pygame.time.get_ticks() - self.separador_spawn) > 400):
                    if self.quantidade_spawnada < self.quantidade_spawn:
                        self.criar_agua_viva()
                        self.separador_spawn = pygame.time.get_ticks()
            if len(self.agua_viva_rects) > 0:
                for agua_viva in self.agua_viva_rects:
                    agua_viva.centerx += self.velocidade_x
            if abs(self.velocidade_x) < self.max_velocidade_x:
                self.velocidade_x += self.incremento_velocidade_x * self.lado_inicio
        self.frame_atual += 1
    
    def criar_agua_viva(self):
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

    def matar(self):
        if len(self.agua_viva_rects) > 0:
            for pos, agua_viva in enumerate(self.agua_viva_rects):
                if ((self.lado_inicio == 1) and (agua_viva.left > self.largura_tela)):
                    self.agua_viva_rects.pop(pos)
                    self.imgs.pop(pos)
                elif ((self.lado_inicio == -1) and (agua_viva.right < 0)):
                    self.agua_viva_rects.pop(pos)
                    self.imgs.pop(pos)
        elif self.comecou and self.quantidade_spawnada > 0:
            return True
        return False

class bola_de_feno(evento):
    def __init__(self, tela: pygame.SurfaceType):
        super().__init__(tela)
        self.tamanho = self.largura_tela//10
        self.y_inicio = random.randint(self.altura_tela//4, 3*self.altura_tela//4)
        self.x_inicio = -2*self.tamanho if (self.lado_inicio == 1) else self.largura_tela + self.tamanho
        self.velocidade_y = 0
        self.velocidade_x = 0
        self.max_velocidade_x = random.randint(4,7)
        self.velocidade_incremento_x = self.lado_inicio/2
        self.aux_y = 0
        self.caminho += "bola_de_feno/"
        self.imgs = []
        for i in range(1,5):
            self.imgs.append(pygame.transform.scale(pygame.image.load(self.caminho + f"{i}.png"), (self.tamanho, self.tamanho)))
        self.bola_de_feno = pygame.image.load(self.caminho + "1.png")
        self.bola_de_feno = pygame.transform.scale(self.bola_de_feno, (self.tamanho, self.tamanho))
        self.bola_de_feno_rect = self.imgs[0].get_rect()
        self.bola_de_feno_rect.topleft = (self.x_inicio - self.tamanho//2, self.y_inicio - self.tamanho//2)
        self.vida = 200
        self.sprite_atual = 0
        self.frames_por_sprite = 30
        self.frame_atual = 0
        
    def aviso_direcao(self):
        if self.comecou and pygame.time.get_ticks() - self.contador <= 2500:
            x_aviso = self.largura_tela - 30 if (self.lado_inicio == -1) else 30
            aviso = pygame.rect.Rect(x_aviso, self.y_inicio - 3, 6, 30)
            pygame.draw.rect(self.tela, (231,231,0), aviso)

    def atualizar(self):
        if self.frame_atual >= self.frames_por_sprite:
            self.sprite_atual += self.lado_inicio
            self.sprite_atual %= 4
            self.frame_atual = 0    
        if not self.comecou:
            self.contador = pygame.time.get_ticks()
            self.comecou = True
        elif pygame.time.get_ticks() - self.contador > 2000:
            if abs(self.velocidade_x) < self.max_velocidade_x:
                self.velocidade_x += self.velocidade_incremento_x
            self.bola_de_feno_rect.centery += 2*self.max_velocidade_x*sin(self.aux_y)
            self.bola_de_feno_rect.centerx += self.velocidade_x
            self.aux_y += 0.1
        self.frame_atual += 1

    def desenhar(self):
        self.aviso_direcao()        
        centro = self.bola_de_feno_rect.center
        img = pygame.transform.rotate(self.bola_de_feno, -10*self.max_velocidade_x*self.lado_inicio*self.aux_y/2)
        rect = img.get_rect()
        rect.center = centro
        self.tela.blit(img, rect)
        
    def verificar_colisao(self, rect_obj : pygame.Rect, dano: int):
        if self.bola_de_feno_rect.colliderect(rect_obj):
            self.vida = max(self.vida - dano, 0)
            return True

    def matar(self):
        if ((self.lado_inicio == 1) and (self.bola_de_feno_rect.left > self.largura_tela)):
            return True
        elif ((self.lado_inicio == -1) and (self.bola_de_feno_rect.right < 0)):
            return True
        elif self.vida == 0:
            return True
        return False

class verme_da_areia(evento):
    def __init__(self, tela: pygame.Surface):
        super().__init__(tela)
        self.x_inicio = random.randint(0, self.largura_tela//3)
        self.x_fim = self.largura_tela - self.x_inicio
        self.tamanho = random.randint(40, 50)
        if self.lado_inicio == -1:
            temp = self.x_inicio
            self.x_inicio = self.x_fim
            self.x_fim = temp
        self.velocidade_y_inicial = random.randint(10, 15)
        self.gravidade = 0.2
        # Fórmula para achar o tempo em tela e calcular a velocidade em x
        tempo_em_tela = (2*self.velocidade_y_inicial)/self.gravidade
        self.velocidade_x = (self.x_fim - self.x_inicio)/tempo_em_tela
        self.caminho += "verme_da_areia/"
        self.img_cabeca = pygame.image.load(self.caminho + "cabeca/1.png")
        self.img_cabeca = pygame.transform.scale(self.img_cabeca , (self.tamanho, self.tamanho))
        self.img_corpo = pygame.image.load(self.caminho + "corpo/1.png")
        self.img_corpo = pygame.transform.scale(self.img_corpo , (self.tamanho, self.tamanho))
        self.img_rabo = pygame.image.load(self.caminho + "rabo/1.png")
        self.img_rabo = pygame.transform.scale(self.img_rabo , (self.tamanho, self.tamanho))
        self.vetor_eixo = pygame.Vector2((0,1))
        
        self.tamanho_corpo = random.randint(6,10)
        self.partes_criadas = 0
        self.vida = 50
        self.verme_da_areia_rects = []
        self.verme_da_areia_vidas = []
        self.velocidades_verme_da_areia : list[pygame.Vector2]= []
        self.separador_corpo = pygame.time.get_ticks()

    def aviso_direcao(self):
        if self.comecou and pygame.time.get_ticks() - self.contador <= 2500:
            y_aviso = self.altura_tela - 90
            aviso = pygame.rect.Rect(self.x_inicio - 5, y_aviso, 10, 40)
            pygame.draw.rect(self.tela, (0,0,0), aviso)

    def atualizar(self):
        if not self.comecou:
            self.contador = pygame.time.get_ticks()
            self.comecou = True
        elif (pygame.time.get_ticks() - self.contador > 2000):
            if ((pygame.time.get_ticks() - self.separador_corpo > 45) and (self.partes_criadas < (self.tamanho_corpo))):
                    self.criar_corpo()
                    self.separador_corpo = pygame.time.get_ticks()
            for pos, verme_da_areia in enumerate(self.verme_da_areia_rects):
                if (pos == 0):
                    self.verme_da_areia_rects[pos].centerx += self.velocidades_verme_da_areia[pos][0]
                    self.verme_da_areia_rects[pos].centery -= self.velocidades_verme_da_areia[pos][1]
                    if verme_da_areia.centery < self.altura_tela:
                        self.velocidades_verme_da_areia[pos][0] = self.velocidade_x
                        self.velocidades_verme_da_areia[pos][1] -= self.gravidade
                    pass
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
                if (self.verme_da_areia_vidas[pos] == 0):
                    self.verme_da_areia_rects.pop(pos)
                    self.verme_da_areia_vidas.pop(pos)
                    self.velocidades_verme_da_areia.pop(pos)
                    pos -= 1
        return colidiu

    def matar(self):
        if len(self.verme_da_areia_rects) > 0:
            for rect in self.verme_da_areia_rects:
                if rect.bottom > self.altura_tela + 2 * self.tamanho:
                    self.verme_da_areia_rects.remove(rect)
        if len(self.verme_da_areia_rects) == 0 and self.partes_criadas > 0:
            return True
        else:
            return False

class nuvem_gafanhotos(evento):
    def __init__(self, tela: pygame.Surface):
        super().__init__(tela)
        self.tamanho = 20
        self.vida = 10
        self.velocidade_x = 0
        self.velocidade_x_max = random.randint(4,8)
        self.incremento_velocidade = random.randint(10,20)/10 * self.lado_inicio
        self.metade_y_tela = random.choice([1,2])
        self.x_inicio = self.largura_tela + self.tamanho if self.lado_inicio == -1 else -2 * self.tamanho
        self.y_inicio = self.altura_tela//2 + self.altura_tela//4 * (-1 if self.metade_y_tela == 1 else 1)
        self.quantidade_maxima = random.randint(20,30)
        self.quantidade_spawnada = 0
        self.gafanhotos_imgs = []
        self.caminho += "gafanhoto/"
        for i in range(1,5):
            self.gafanhotos_imgs.append(pygame.transform.scale(pygame.image.load(self.caminho + f"{i}.png"), (self.tamanho, self.tamanho)))
            if (self.lado_inicio == 1):
                self.gafanhotos_imgs[i-1] = pygame.transform.flip(self.gafanhotos_imgs[i-1], 1, 0)
        self.separador_gafanhotos = pygame.time.get_ticks()
        self.gafanhotos_rects = []
        self.vidas = []
        self.imgs = []
        self.frame_atual = 0
        self.frames_por_sprite = 10
        # self.gafanhoto_img = pygame.image.load(self.caminho + "gafanhoto.png")
        # self.gafanhoto_img = pygame.transform.scale(self.gafanhoto_img, (self.tamanho, self.tamanho))
        # if (self.lado_inicio == 1):
        #     self.gafanhoto_img = pygame.transform.flip(self.gafanhoto_img, 1, 0)
        

    def aviso_direcao(self):
        if self.comecou and pygame.time.get_ticks() - self.contador <= 2500:
            x_aviso = self.largura_tela - 40 if (self.lado_inicio == -1) else 40
            aviso = pygame.rect.Rect(x_aviso, self.y_inicio, 10, 40)
            pygame.draw.rect(self.tela, (50,155,50), aviso)

    def atualizar(self):
        if self.frame_atual >= self.frames_por_sprite:
            for pos in range(len(self.imgs)):
                self.imgs[pos] += 1
                self.imgs[pos] %= 4 
            self.frame_atual = 0
            print(self.imgs)
        if not self.comecou:
            self.contador = pygame.time.get_ticks()
            self.comecou = True
        elif pygame.time.get_ticks() - self.contador >= 2000:
            if self.quantidade_spawnada < self.quantidade_maxima:
                if (pygame.time.get_ticks() - self.separador_gafanhotos) > 2000/self.quantidade_maxima:
                    self.criar_gafanhoto()
                    self.separador_gafanhotos = pygame.time.get_ticks()
            for gafanhoto in self.gafanhotos_rects:
                gafanhoto.centerx += self.velocidade_x
                if abs(self.velocidade_x) < self.velocidade_x_max:
                    self.velocidade_x += self.incremento_velocidade
        self.frame_atual += 1

    def desenhar(self):
        self.aviso_direcao
        for pos, gafanhoto in enumerate(self.gafanhotos_rects):
            self.tela.blit(self.gafanhotos_imgs[self.imgs[pos]], gafanhoto)
    
    def criar_gafanhoto(self):
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

    def matar(self):
        for pos, gafanhoto in enumerate(self.gafanhotos_rects):
            if ((self.lado_inicio == 1) and (gafanhoto.left > self.largura_tela)):
                self.gafanhotos_rects.pop(pos)
                self.vidas.pop(pos)
                self.imgs.pop(pos)
            elif ((self.lado_inicio == -1) and (gafanhoto.right < 0)):
                self.gafanhotos_rects.pop(pos)
                self.vidas.pop(pos)
                self.imgs.pop(pos)
            elif (len(self.vidas) > 0):
                for pos, item in enumerate(self.vidas):
                    if item == 0:
                        self.gafanhotos_rects.pop(pos)
                        self.imgs.pop(pos)
                        self.vidas.pop(pos)
                        pos -= 1

        if ((len(self.gafanhotos_rects) == 0) and (self.quantidade_spawnada > 0)):
            return True
        return False

class invasores_do_espaco(evento):
    def __init__(self, tela: pygame.Surface):
        super().__init__(tela)
        self.velocidade_y = 3
        self.num_linhas = 3
        self.num_colunas = 5
        self.x_inicio = self.largura_tela//2
        self.tamanho_x = (self.largura_tela//3 - self.largura_tela//12)//self.num_colunas
        self.espacamento_x = (self.largura_tela//3 -self.num_colunas * self.tamanho_x)//(self.num_colunas + 1)
        self.tamanho_y = 2*self.tamanho_x // 3
        self.tamanho_nave = (self.tamanho_x*2, self.tamanho_y)
        self.espacamento_y = self.tamanho_y // 3
        self.matriz_inimigos = [[],[],[]]
        self.vida_1 = 20
        self.vidas_inimigos = [[],[],[]]
        self.caminho += "space/"
        self.img_linha_1 = []
        self.img_linha_2 = []
        self.img_linha_3 = []
        for i in [1, 2]:
            self.img_linha_1.append(pygame.transform.scale(pygame.image.load(self.caminho + f"/inimigo1/{i}.png"), (self.tamanho_x, self.tamanho_y)))
            self.img_linha_2.append(pygame.transform.scale(pygame.image.load(self.caminho + f"/inimigo2/{i}.png"), (self.tamanho_x, self.tamanho_y)))
            self.img_linha_3.append(pygame.transform.scale(pygame.image.load(self.caminho + f"/inimigo3/{i}.png"), (self.tamanho_x, self.tamanho_y)))
        self.img_nave_antiga = pygame.transform.scale(pygame.image.load(self.caminho + "nave.png"), self.tamanho_nave)            
        self.vida_nave = 30
        self.nave_antiga_rect = pygame.Rect
        self.criar_inimigos()
        self.frames_por_sprite = 30
        self.sprite_atual = 0
        self.frame_atual = 0

    def aviso_direcao(self):
        if self.comecou and (pygame.time.get_ticks() - self.contador <= 2500):
            aviso = pygame.rect.Rect(self.largura_tela//2 - 5, 10, 10, 40)
            pygame.draw.rect(self.tela, (255,0,0), aviso)
    
    def criar_inimigos(self):
        for i in range(self.num_linhas):
            for j in range(self.num_colunas):
                pos_x = self.largura_tela//3 + (j + 1) * self.espacamento_x + j * self.tamanho_x
                pos_y =  - (i + 1) * self.espacamento_y - (i + 2) * self.tamanho_y
                inimigo = pygame.rect.Rect(pos_x, pos_y, self.tamanho_x, self.tamanho_y)
                self.matriz_inimigos[i].append(inimigo)
                self.vidas_inimigos[i].append(self.vida_1)
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
        if self.frame_atual >= self.frames_por_sprite:
            self.sprite_atual += 1
            self.sprite_atual %= 2
            self.frame_atual = 0
        if not self.comecou:
            self.contador = pygame.time.get_ticks()
            self.comecou = True
        elif (pygame.time.get_ticks() - self.contador) >= 2500:
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
                    self.vidas_inimigos[i][j] = max(self.vidas_inimigos[i][j] - dano, 0)
                    if self.vidas_inimigos[i][j] == 0:
                        self.vidas_inimigos[i].pop(j)
                        self.matriz_inimigos[i].pop(j) 
                        if len(self.matriz_inimigos[i]) == 0:
                            self.matriz_inimigos.pop(i)
                            self.vidas_inimigos.pop(i)
        if self.nave_antiga_rect != None:
            if self.nave_antiga_rect.colliderect(rect_obj):
                colidiu = True
                self.vida_nave = max(self.vida_nave - dano, 0)
                if self.vida_nave == 0:
                    self.nave_antiga_rect = None
        return colidiu

    def matar(self):
        if self.comecou:
            if self.nave_antiga_rect == None and len(self.matriz_inimigos) == 0:
                return True
            elif self.nave_antiga_rect != None and self.nave_antiga_rect.top > self.altura_tela:
                return True
            elif len(self.matriz_inimigos) > 0:
                if self.matriz_inimigos[len(self.matriz_inimigos) - 1][0].top > self.altura_tela:
                    self.matriz_inimigos.clear()
        return False
        
class cometa(evento):
    def __init__(self, tela: pygame.Surface):
        super().__init__(tela)
        self.tamanho = (self.largura_tela//6, self.largura_tela//4)
        self.x_inicio = random.randint(0, self.largura_tela//2) if self.lado_inicio == 1 else random.randint(self.largura_tela//2, self.largura_tela) 
        self.x_fim = random.randint(self.largura_tela//2, self.largura_tela) if self.lado_inicio == 1 else random.randint(0, self.largura_tela//2)
        self.tempo_em_tela = random.randint(5,10)*10
        self.velocidade_y = self.altura_tela//self.tempo_em_tela
        self.velocidade_x = (self.x_fim - self.x_inicio)//self.tempo_em_tela
        self.vida = 300
        self.cometa_rect = pygame.rect.Rect(self.x_inicio - self.tamanho[0]//2, -2*self.tamanho[1], self.tamanho[0], self.tamanho[1])
        self.caminho += "cometa/"
        self.imgs = []
        for i in range(1,5):
            self.imgs.append(pygame.transform.scale(pygame.image.load(self.caminho + f"{i}.png"), (self.tamanho[0], self.tamanho[1])))
        self.frame_atual = 0
        self.sprite_atual = 0
        self.frames_por_sprite = 15
        self.angulo = 0


    def aviso_direcao(self):
        if self.comecou and (pygame.time.get_ticks() - self.contador <= 2500):
            aviso_surf = pygame.Surface((10, 40))
            aviso_surf.fill((255,255,255))
            aviso_surf.set_colorkey((0,0,0))
            aviso_rect0 = aviso_surf.get_rect()
            aviso_rect0.center = (self.x_inicio + self.lado_inicio * 40, 40)
            aviso_rect1 = aviso_surf.get_rect()
            aviso_rect1.center = aviso_rect0.center
            aviso_surf = pygame.transform.rotate(aviso_surf, self.angulo)
            self.tela.blit(aviso_surf, aviso_rect1)

    def atualizar(self):
        if self.frame_atual >= self.frames_por_sprite:
            self.sprite_atual += 1
            self.sprite_atual %= 4
            self.frame_atual = 0
        if not self.comecou:
            self.contador = pygame.time.get_ticks()
            self.comecou = True
        elif (pygame.time.get_ticks() - self.contador) >= 2500:
            if (self.cometa_rect.bottom >= 0):
                self.cometa_rect.centerx += self.velocidade_x
                self.cometa_rect.centery += self.velocidade_y
            else:
                self.cometa_rect.centery += self.velocidade_y
        direcao = pygame.Vector2(self.velocidade_x, self.velocidade_y)
        self.angulo = direcao.angle_to(pygame.Vector2(0, 1))
        self.frame_atual += 1

    def desenhar(self):
        self.aviso_direcao()
        centro = self.cometa_rect.center
        img = pygame.transform.rotate(self.imgs[self.sprite_atual], self.angulo)
        rect = img.get_rect()
        rect.center = centro
        self.tela.blit(img, rect)

    def verificar_colisao(self, rect_obj : pygame.Rect, dano: int):
        if self.cometa_rect.colliderect(rect_obj):
            self.vida = max(self.vida - dano, 0)
            return True

    def matar(self):
        if self.cometa_rect.top > self.altura_tela or self.vida == 0:
            return True
        return False