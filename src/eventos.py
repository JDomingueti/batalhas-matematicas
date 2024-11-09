import pygame, random
from abc import ABC, abstractmethod
from math import sin

# Arquivo para implementação dos eventos dos cenários

class evento(ABC):
    def __init__(self, tela: pygame.Surface):
        self.largura_tela = tela.get_width()
        self.altura_tela = tela.get_height()
        self.tela = tela
        self.comecou = False
        self.lado_inicio = random.choice([-1,1])
        self.contador = pygame.time.get_ticks()
    
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
    def matar(self):
        pass


# OCEANO:
#   TUBARÃO - Ok
#   CARANGUEIJO GIGANTE - Ok
#   ÁGUA VIVA - Ok - Pensando em tirar
#   BOLHAS - Ideia ruim

class tubarao(evento):
    def __init__(self, tela: pygame.Surface):
        super().__init__(tela)
        # self.contador = pygame.time.Clock()
        # self.lado_inicio = random.choice([-1, 1])
        self.tamanho = (self.largura_tela//4, self.altura_tela//6)
        self.y_inicio = self.altura_tela//2
        self.x_inicio = -2 * self.tamanho[0] if (self.lado_inicio > 0) else self.largura_tela + self.tamanho[0]
        self.tubarao = pygame.rect.Rect(self.x_inicio, self.y_inicio, self.tamanho[0], self.tamanho[1])
        self.tubarao.center = (self.x_inicio, self.y_inicio)
        # self.tubarao = pygame.image.load("../assets/tubarao.png")
        # self.tubarao = pygame.transform.scale(self.tubarao, (self.tamanho[0],self.tamanho[1]))
        # if (self.lado_inicio == -1):
        #     self.tubarao = pygame.transform.flip(self.tubarao, True, False)
        # self.tubarao_rect = self.tubarao.get_rect()
        # self.tubarao_rect.topleft = (self.x_inicio, self.y_inicio)
        self.afastamento_max = random.randint(self.altura_tela//10, self.altura_tela//5)
        self.velocidade_x = 5*self.lado_inicio
        self.velocidade_y = 0
        self.adicao_velocidade_y = random.choice([-1,1])*(random.randint(self.afastamento_max//2, self.afastamento_max))/self.altura_tela
        # self.comecou = False
        
    def aviso_direcao(self):
        if self.comecou and pygame.time.get_ticks() - self.contador <= 2500:
            x_aviso = self.largura_tela - 30 if (self.lado_inicio == -1) else 30
            aviso = pygame.rect.Rect(x_aviso, self.y_inicio - 3, 6, 30)
            pygame.draw.rect(self.tela, (255,0,0), aviso)
    
    def desenhar(self):
        self.aviso_direcao()
        # self.tela.blit(self.tubarao, self.tubarao_rect)
        pygame.draw.rect(self.tela, (150,150,150), self.tubarao)

    def atualizar(self):
        if not self.comecou:
            self.contador = pygame.time.get_ticks()
            self.comecou = True
        elif pygame.time.get_ticks() - self.contador >= 2000:
            # self.tubarao_rect.centerx += self.velocidade_x
            # self.tubarao_rect.centery -= self.velocidade_y
            # if (self.lado_inicio == -1 and self.tubarao_rect.centerx <= self.largura_tela) or (self.lado_inicio == 1 and self.tubarao_rect.centerx >= 0):
            #     if self.tubarao_rect.centery <= self.y_inicio - self.afastamento_max:
            #         if self.adicao_velocidade_y > 0:
            #             self.adicao_velocidade_y *= -1
            #     if self.tubarao_rect.centery >= self.y_inicio + self.afastamento_max:
            #         if self.adicao_velocidade_y < 0:
            #             self.adicao_velocidade_y *= -1
            self.tubarao.centerx += self.velocidade_x
            self.tubarao.centery -= self.velocidade_y
            if (self.lado_inicio == -1 and self.tubarao.centerx <= self.largura_tela) or (self.lado_inicio == 1 and self.tubarao.centerx >= 0):
                if self.tubarao.centery <= self.y_inicio - self.afastamento_max:
                    if self.adicao_velocidade_y > 0:
                        self.adicao_velocidade_y *= -1
                if self.tubarao.centery >= self.y_inicio + self.afastamento_max:
                    if self.adicao_velocidade_y < 0:
                        self.adicao_velocidade_y *= -1
                self.velocidade_y += self.adicao_velocidade_y
 
    def matar(self):
        # if self.tubarao_rect.left > self.largura_tela + self.tamanho[0] or self.tubarao_rect.right < -2 * self.tamanho[0]:
        if self.tubarao.left > self.largura_tela + self.tamanho[0] or self.tubarao.right < -2 * self.tamanho[0]:
            return True
        return False

class caranguejo(evento):
    def __init__(self, tela: pygame.SurfaceType):
        super().__init__(tela)
        # self.lado_inicio = random.choice([-1,1])
        # self.contador = pygame.time.get_ticks()
        self.tamanho = (self.largura_tela//3, self.altura_tela//6)
        self.x_inicio = -2 * self.tamanho[0] if (self.lado_inicio == 1) else self.largura_tela + self.tamanho[0]
        self.y_inicio = self.altura_tela - self.tamanho[1]
        self.caranguejo = pygame.rect.Rect(self.x_inicio, self.y_inicio, self.tamanho[0], self.tamanho[1])
        self.caranguejo_rect = self.caranguejo
        self.garra_esquerda = pygame.rect.Rect(self.caranguejo.left,self.caranguejo.top - self.tamanho[1] + self.caranguejo_rect.height//2, self.tamanho[0]//4, self.tamanho[1])
        self.garra_direita = pygame.rect.Rect(self.caranguejo.right - self.tamanho[0]//4, self.caranguejo.top - self.tamanho[1] + self.caranguejo_rect.height//2, self.tamanho[0]//4, self.tamanho[1])
        self.max_velocidade_x = random.randint(3,6)
        self.velocidade_x = 0
        self.adicao_velocidade_x = self.lado_inicio/10
        self.contador_garras = pygame.time.get_ticks()
        self.garra_esticada = False
        self.prox_garra = 1

    def aviso_direcao(self):
        if (self.comecou and (pygame.time.get_ticks() - self.contador <= 2500)):
            x_aviso = self.largura_tela - 30 if (self.lado_inicio == -1) else 30
            aviso = pygame.rect.Rect(x_aviso, self.y_inicio - 3, 6, 30)
            pygame.draw.rect(self.tela, (255,0,0), aviso)

    def desenhar(self):
        self.aviso_direcao()
        pygame.draw.rect(self.tela, (248, 37, 67), self.garra_esquerda)
        pygame.draw.rect(self.tela, (200, 37, 67), self.garra_direita)
        pygame.draw.rect(self.tela, (200, 37, 67), self.caranguejo_rect)

    def atualizar(self):
        if not self.comecou:
            self.contador = pygame.time.get_ticks()
            self.comecou = True
        elif pygame.time.get_ticks() - self.contador >= 2000:
            self.caranguejo_rect.centerx += self.velocidade_x
            # self.garra_esquerda.topleft = (self.caranguejo_rect.left,self.caranguejo_rect.top - self.tamanho[1])
            # self.garra_direita.topleft = (self.caranguejo_rect.right - self.tamanho[0]//3, self.caranguejo_rect.top - self.tamanho[1])
            self.garra_esquerda.centerx += self.velocidade_x
            self.garra_direita.centerx += self.velocidade_x
            if pygame.time.get_ticks() - self.contador_garras > 500:
                if not self.garra_esticada:
                    if self.prox_garra == 1:
                        escalar = random.randint(180,200)/100
                        self.garra_esquerda = self.garra_esquerda.scale_by(1, escalar)
                        self.garra_esquerda.top = self.caranguejo_rect.top - self.garra_esquerda.height + self.caranguejo_rect.height//2
                        self.prox_garra = -1
                        self.contador_garras = pygame.time.get_ticks()
                        self.garra_esticada = True
                        pass
                    else:
                        escalar = random.randint(180,200)/100
                        self.garra_direita = self.garra_direita.scale_by(1, escalar)
                        self.garra_direita.top = self.caranguejo_rect.top - self.garra_direita.height + self.caranguejo_rect.height//2
                        self.prox_garra = 1
                        self.contador_garras = pygame.time.get_ticks()
                        self.garra_esticada = True
                        pass
                else:
                    if self.prox_garra == -1:
                        self.garra_esquerda = pygame.rect.Rect(self.caranguejo_rect.left,self.caranguejo_rect.top - self.tamanho[1] + self.caranguejo_rect.height//2, self.tamanho[0]//4, self.tamanho[1])
                        self.contador_garras = pygame.time.get_ticks()
                        self.garra_esticada = False
                        pass
                    else:
                        self.garra_direita = pygame.rect.Rect(self.caranguejo_rect.right - self.tamanho[0]//4, self.caranguejo_rect.top - self.tamanho[1] + self.caranguejo_rect.height//2, self.tamanho[0]//4, self.tamanho[1])
                        self.contador_garras = pygame.time.get_ticks()
                        self.garra_esticada = False
                        pass

            if abs(self.velocidade_x) < self.max_velocidade_x:
                self.velocidade_x += self.adicao_velocidade_x

    def matar(self):
        if self.caranguejo_rect.left > self.largura_tela + self.tamanho[0] or self.caranguejo_rect.right < -2 * self.tamanho[0]:
            return True
        return False

class bando_aguas_vivas(evento):
    def __init__(self, tela : pygame.SurfaceType):
        super().__init__(tela)
        # self.lado_inicio = random.choice([-1, 1])
        # self.contador = pygame.time.get_ticks()
        self.tamanho = (self.largura_tela//25, self.altura_tela//10)
        self.y_inicio = random.randint(self.altura_tela//7, 6*self.altura_tela//7)
        self.quantidade_spawn = random.randint(5,8)
        self.x_inicio = self.largura_tela + 30 if (self.lado_inicio == -1) else -60
        self.max_velocidade_x = random.randint(4,6)
        self.velocidade_x = 0
        self.incremento_velocidade_x = 1/2
        self.afastamento = self.altura_tela//7
        self.separador_spawn = pygame.time.get_ticks()
        self.quantidade_spawnada = 0
        self.grupo = []

    def aviso_direcao(self):
        if (self.comecou and (pygame.time.get_ticks() - self.contador <= 2500)):
            x_aviso = self.largura_tela - 30 if (self.lado_inicio == -1) else 30
            aviso = pygame.rect.Rect(x_aviso, self.y_inicio - 3, 6, 30)
            pygame.draw.rect(self.tela, (77,77,189), aviso)
    
    def desenhar(self):
        self.aviso_direcao()
        if len(self.grupo) > 0:
            for agua_viva in self.grupo:
                pygame.draw.rect(self.tela, (77,77,255), agua_viva)
        
    def atualizar(self):
        if not self.comecou:
            self.contador = pygame.time.get_ticks()
            self.comecou = True
        else:
            if len(self.grupo) < self.quantidade_spawn:
                if ((pygame.time.get_ticks() - self.separador_spawn) > 400):
                    if self.quantidade_spawnada < self.quantidade_spawn:
                        self.criar_agua_viva()
                        self.separador_spawn = pygame.time.get_ticks()
            if len(self.grupo) > 0:
                for agua_viva in self.grupo:
                    agua_viva.centerx += self.velocidade_x
            if abs(self.velocidade_x) < self.max_velocidade_x:
                self.velocidade_x += self.incremento_velocidade_x * self.lado_inicio
    
    def criar_agua_viva(self):
        y_atual = self.y_inicio + random.randint(-self.afastamento, self.afastamento)
        agua_viva = pygame.rect.Rect(self.x_inicio, y_atual, self.tamanho[0], self.tamanho[1])
        self.grupo.append(agua_viva)
        self.quantidade_spawnada += 1

    def matar(self):
        if len(self.grupo) > 0:
            for agua_viva in self.grupo:
                if ((agua_viva.left <= -65) or (agua_viva.right >= self.largura_tela + 65)):
                    self.grupo.remove(agua_viva)
        elif self.comecou and self.quantidade_spawnada > 0:
            return True
        else:
            return False

# DESERTO:
#   BOLA DE FENO - Ok
#   MINHOCOSUL - Ruim - Pensando em tirar
#   NUVEM DE GAFANHOTOS - Ok
#   TEMPESTADE DE AREIA - Ideia ruim

class bola_de_feno(evento):
    def __init__(self, tela: pygame.SurfaceType):
        super().__init__(tela)
        # self.lado_inicio = random.choice([-1, 1])
        # self.contador = pygame.time.get_ticks()
        self.tamanho = self.largura_tela//10
        self.y_inicio = random.randint(self.altura_tela//4, 3*self.altura_tela//4)
        self.x_inicio = -2*self.tamanho if (self.lado_inicio == 1) else self.largura_tela + self.tamanho
        self.velocidade_y = 0
        self.velocidade_x = 0
        self.max_velocidade_x = random.randint(3,5)
        self.velocidade_incremento_x = self.lado_inicio/2
        self.aux_y = 0
        self.bola_de_feno_rect = pygame.rect.Rect(self.x_inicio - self.tamanho//2, self.y_inicio - self.tamanho,self.tamanho, self.tamanho)

    def aviso_direcao(self):
        if self.comecou and pygame.time.get_ticks() - self.contador <= 2500:
            x_aviso = self.largura_tela - 30 if (self.lado_inicio == -1) else 30
            aviso = pygame.rect.Rect(x_aviso, self.y_inicio - 3, 6, 30)
            pygame.draw.rect(self.tela, (231,231,0), aviso)
            
    def atualizar(self):
        if not self.comecou:
            self.contador = pygame.time.get_ticks()
            self.comecou = True
        else:
            if abs(self.velocidade_x) < self.max_velocidade_x:
                self.velocidade_x += self.velocidade_incremento_x
            self.bola_de_feno_rect.centery += 2*self.max_velocidade_x*sin(self.aux_y)
            self.bola_de_feno_rect.centerx += self.velocidade_x
            self.aux_y += 0.1
            
    def desenhar(self):
        self.aviso_direcao()
        pygame.draw.rect(self.tela,(231,231,0), self.bola_de_feno_rect)

    def matar(self):
        if ((self.bola_de_feno_rect.left < -2*self.tamanho) or (self.bola_de_feno_rect.right > self.largura_tela + 2*self.tamanho)):
            return True
        else:
            return False

# Mudar nome
class minhocosul(evento):
    def __init__(self, tela: pygame.Surface):
        super().__init__(tela)
        # self.lado_inicio = random.choice([-1,1])
        # self.contador = pygame.time.get_ticks()
        self.x_inicio = random.randint(0, self.largura_tela//3)
        self.x_fim = self.largura_tela - self.x_inicio
        self.tamanho = random.randint(5, 20)
        if self.lado_inicio == -1:
            temp = self.x_inicio
            self.x_inicio = self.x_fim
            self.x_fim = temp
        self.velocidade_y_inicial = random.randint(10, 15)
        self.gravidade = 0.3
        # Fórmula para achar o tempo em tela e calcular a velocidade em x
        tempo_em_tela = (2*self.velocidade_y_inicial)/self.gravidade
        self.velocidade_x = (self.x_fim - self.x_inicio)/tempo_em_tela
        self.vetor_velocidade = pygame.Vector2(self.velocidade_x, self.velocidade_y_inicial)
        
        self.tamanho_meio_corpo = random.randint(10,15)
        self.minhocosul = []
        self.minhocosul_surf = []
        self.velocidades_minhocosul = [self.velocidade_y_inicial] * (self.tamanho_meio_corpo + 2)
        self.partes_criadas = 0

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
            if (pygame.time.get_ticks() - self.contador > 50):
                if (self.partes_criadas < (self.tamanho_meio_corpo + 2)):
                    self.criar_corpo()
            for pos, parte in enumerate(self.minhocosul):
                parte.centery -= self.velocidades_minhocosul[pos]
                if parte.top <= self.altura_tela:
                    self.vetor_velocidade[1] = self.velocidades_minhocosul[pos]
                    parte.centerx += self.velocidade_x
                    self.velocidades_minhocosul[pos] -= self.gravidade
            # for pos in range(1, self.tamanho_meio_corpo + 2):
            #     self.velocidades_minhocosul[-pos] = self.velocidades_minhocosul[-pos-1]
            #     self.velocidades_minhocosul[0] += self.gravidade

    def desenhar(self):
        self.aviso_direcao()
        for pos in range(1, len(self.minhocosul)):
            if pos <= len(self.minhocosul)-1:
                centro_c = ((self.minhocosul[-pos].centerx +self.minhocosul[-pos-1].centerx)/2,(self.minhocosul[-pos].centery + self.minhocosul[-pos-1].centery)/2)
                pygame.draw.circle(self.tela, (0,0,0), centro_c, self.tamanho)
            self.tela.blit(self.minhocosul_surf[-pos], self.minhocosul[-pos])
            # pygame.draw.rect(self.tela,(31,31,31), self.minhocosul[-pos])

    def matar(self):
        if len(self.minhocosul) > 0:
            if self.minhocosul[-1].top >= self.altura_tela + (self.tamanho_meio_corpo+3) * self.tamanho:
                for parte in self.minhocosul:
                    self.minhocosul.remove(parte)
            if len(self.minhocosul) == 0 and self.comecou:
                return True
        else:
            return False

    def criar_corpo(self):
        if self.partes_criadas == 0:
            cabeca = pygame.rect.Rect(self.x_inicio-self.tamanho//2, self.altura_tela + self.tamanho, self.tamanho, self.tamanho)
            self.minhocosul.append(cabeca)
            cabeca_surf = pygame.Surface((self.tamanho, self.tamanho)).convert_alpha()
            cabeca_surf.fill((0,0,0))
            self.minhocosul_surf.append(cabeca_surf)
        elif (self.partes_criadas <= (self.tamanho_meio_corpo + 1)):
            parte = pygame.rect.Rect(self.x_inicio-self.tamanho//2, self.altura_tela + self.tamanho, self.tamanho, self.tamanho)
            self.minhocosul.append(parte)
            part_surf = pygame.Surface((self.tamanho, self.tamanho)).convert_alpha()
            part_surf.fill((0,0,0))
            self.minhocosul_surf.append(part_surf)
            # for i in range(2,self.tamanho_meio_corpo+2):
            #     parte = pygame.rect.Rect(self.x_inicio-self.tamanho//2, self.altura_tela + i * self.tamanho, self.tamanho, self.tamanho)
            #     self.minhocosul.append(parte)
            #     part_surf = pygame.Surface((self.tamanho, self.tamanho))
            #     part_surf.fill((0,0,0))
            #     self.minhocosul_surf.append(part_surf)
        else:
            # rabo = pygame.rect.Rect(self.x_inicio-self.tamanho//4, self.altura_tela + self.tamanho*(self.tamanho_meio_corpo + 2), self.tamanho, self.tamanho)
            rabo = pygame.rect.Rect(self.x_inicio-self.tamanho//4, self.altura_tela + self.tamanho_meio_corpo, self.tamanho, self.tamanho)
            self.minhocosul.append(rabo)
            rabo_surf = pygame.Surface((self.tamanho, self.tamanho)).convert_alpha()
            rabo_surf.fill((0,0,0))
            self.minhocosul_surf.append(rabo_surf)
        self.partes_criadas += 1

class nuvem_gafanhotos(evento):
    def __init__(self, tela: pygame.Surface):
        super().__init__(tela)
        # self.lado_inicio = random.choice([-1,1])
        # self.contador = pygame.time.get_ticks()
        self.tamanho = 15
        self.metade_y_tela = random.choice([1,2])
        self.x_inicio = self.largura_tela + self.tamanho if self.lado_inicio == -1 else -2 * self.tamanho
        self.y_inicio = self.altura_tela//2 + self.altura_tela//4 * (-1 if self.metade_y_tela == 1 else 1)
        self.quantidade_maxima = random.randint(20,40)
        self.velocidade_x = 0
        self.velocidade_x_max = random.randint(4,8)
        self.incremento_velocidade = random.randint(0,20)/10 * self.lado_inicio
        self.quantidade_spawnada = 0
        self.gafanhotos = []
        self.separador_gafanhotos = pygame.time.get_ticks()

    def aviso_direcao(self):
        if self.comecou and pygame.time.get_ticks() - self.contador <= 2500:
            x_aviso = self.largura_tela - 40 if (self.lado_inicio == -1) else 40
            aviso = pygame.rect.Rect(x_aviso, self.y_inicio, 10, 40)
            pygame.draw.rect(self.tela, (50,155,50), aviso)

    def atualizar(self):
        if not self.comecou:
            self.contador = pygame.time.get_ticks()
            self.comecou = True
        elif pygame.time.get_ticks() - self.contador >= 2000:
            if self.quantidade_spawnada < self.quantidade_maxima:
                if (pygame.time.get_ticks() - self.separador_gafanhotos) > 50:
                    self.criar_gafanhoto()
                    self.separador_gafanhotos = pygame.time.get_ticks()
            for gafanhoto in self.gafanhotos:
                gafanhoto.centerx += self.velocidade_x
                if abs(self.velocidade_x) < self.velocidade_x_max:
                    self.velocidade_x += self.incremento_velocidade

    def desenhar(self):
        self.aviso_direcao
        for gafanhoto in self.gafanhotos:
            pygame.draw.rect(self.tela, (146,240,146), gafanhoto)
    
    def criar_gafanhoto(self):
        y_gafanhoto = self.y_inicio + random.randint(-self.altura_tela//4, self.altura_tela//4) - self.tamanho
        gafanhoto = pygame.rect.Rect(self.x_inicio, y_gafanhoto, self.tamanho, self.tamanho)
        self.gafanhotos.append(gafanhoto)
        self.quantidade_spawnada += 1

    def matar(self):
        for gafanhoto in self.gafanhotos:
            if (gafanhoto.left <= -3*self.tamanho) or (gafanhoto.right >= self.largura_tela + 3 * self.tamanho):
                self.gafanhotos.remove(gafanhoto)
        if ((len(self.gafanhotos) == 0) and (self.quantidade_spawnada > 0)):
            return True
        else:
            return False

# ESPAÇO:
#   COMETA - Ok
#   SATÉLITE - Padrão repetido
#   CHUVA DE ESTRELAS - Difícil de fazer colisão
#   BURACO NEGRO - Interessante mas tem que pensar mais
#   INIMIGOS SPACE INVADERS ORIGINAL Ok

class invasores_do_espaco(evento):
    def __init__(self, tela: pygame.Surface):
        super().__init__(tela)
        # self.contador = pygame.time.get_ticks()
        self.velocidade_y = 4
        self.num_linhas = 3
        self.num_colunas = 3
        self.x_inicio = self.largura_tela//2
        self.tamanho_x = (self.largura_tela//3 - self.largura_tela//12)//self.num_colunas
        self.espacamento_x = (self.largura_tela//3 -self.num_colunas * self.tamanho_x)//(self.num_colunas + 1)
        self.tamanho_y = 2*self.tamanho_x // 3
        self.espacamento_y = self.tamanho_y // 3
        self.matriz_inimigos = [[],[],[]]
        self.nave_antiga = pygame.Rect
        self.criar_inimigos()

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
        pos_x = self.largura_tela//3 + (self.num_colunas + 1) * self.espacamento_x + (self.num_colunas + 1) * self.tamanho_x
        pos_y =  - (2 * self.num_linhas + 4) * self.espacamento_y - (self.num_linhas + 2) * self.tamanho_y
        tamanho_nave = (self.largura_tela//4, self.altura_tela//6)
        self.nave_antiga = pygame.rect.Rect(self.largura_tela//2 - tamanho_nave[0]//2, pos_y, tamanho_nave[0], tamanho_nave[1])

    def desenhar(self):
        self.aviso_direcao()
        for i, linha in enumerate(self.matriz_inimigos):
            for inimigo in linha:
                if i == 0:
                    pygame.draw.rect(self.tela, (0,0,0), inimigo)
                elif i == 1:
                    pygame.draw.rect(self.tela, (0,124,0), inimigo)
                else:
                    pygame.draw.rect(self.tela, (255,255,255), inimigo)
        pygame.draw.rect(self.tela, (100,255,100), self.nave_antiga)

    def atualizar(self):
        if not self.comecou:
            self.contador = pygame.time.get_ticks()
            self.comecou = True
        elif (pygame.time.get_ticks() - self.contador) >= 2500:
            for linha in self.matriz_inimigos:
                for inimigo in linha:
                    inimigo.centery += self.velocidade_y
            self.nave_antiga.centery += self.velocidade_y
    
    def matar(self):
        if self.comecou:
            if self.nave_antiga.top > self.altura_tela:
                return True
            pass
        else:
            return False
        
class cometa(evento):
    def __init__(self, tela: pygame.Surface):
        super().__init__(tela)
        # self.lado_inicio = random.choice([-1,1])
        # self.contador = pygame.time.get_ticks()
        self.tamanho = self.largura_tela//10
        self.x_inicio = random.randint(0, self.largura_tela//2) if self.lado_inicio == 1 else random.randint(self.largura_tela//2, self.largura_tela) 
        self.x_fim = random.randint(self.largura_tela//2, self.largura_tela) if self.lado_inicio == 1 else random.randint(0, self.largura_tela//2)
        self.tempo_em_tela = random.randint(5,10)*10
        self.velocidade_y = self.altura_tela//self.tempo_em_tela
        self.velocidade_x = (self.x_fim - self.x_inicio)//self.tempo_em_tela
        self.cometa_rect = pygame.rect.Rect(self.x_inicio - self.tamanho//2, -2*self.tamanho, self.tamanho, self.tamanho)

    def aviso_direcao(self):
        if self.comecou and (pygame.time.get_ticks() - self.contador <= 2500):
            aviso_surf = pygame.Surface((10, 40))
            aviso_surf.fill((255,255,255))
            aviso_surf.set_colorkey((0,0,0))
            aviso_rect0 = aviso_surf.get_rect()
            aviso_rect0.center = (self.x_inicio + self.lado_inicio * 40, 40)
            direcao = pygame.Vector2(self.velocidade_x, self.velocidade_y)
            aviso_rect1 = aviso_surf.get_rect()
            aviso_rect1.center = aviso_rect0.center
            aviso_surf = pygame.transform.rotate(aviso_surf, direcao.angle_to(pygame.Vector2(0, self.velocidade_y)))
            self.tela.blit(aviso_surf, aviso_rect1)
    
    def atualizar(self):
        if not self.comecou:
            self.contador = pygame.time.get_ticks()
            self.comecou = True
        elif (pygame.time.get_ticks() - self.contador) >= 2500:
            if (self.cometa_rect.bottom >= 0):
                self.cometa_rect.centerx += self.velocidade_x
                self.cometa_rect.centery += self.velocidade_y
            else:
                self.cometa_rect.centery += self.velocidade_y
    
    def desenhar(self):
        self.aviso_direcao()
        pygame.draw.rect(self.tela, (150,150,150), self.cometa_rect)
    
    def matar(self):
        if self.cometa_rect.top > self.altura_tela:
            return True
        else:
            return False