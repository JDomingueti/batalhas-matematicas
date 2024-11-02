import pygame

# TODO: Estilizar

pygame.font.init()

class Botao:
    def __init__(self, pos, texto, fonte, tamanho, cor, cor_destaque, cor_BG = "Black", efeitos = 0.3, focado = False):
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
        self.cor_BG = cor_BG
        
        self.texto = texto
        self.fonte = pygame.font.SysFont(fonte, tamanho)
        texto_render = self.fonte.render(self.texto, False, self.cor, self.cor_BG)
        self.texto_rect = texto_render.get_rect(center = (self.x_pos, self.y_pos))
        
        self.som = pygame.mixer.Sound("../assets/movimento_menu.wav")
        self.som.set_volume(efeitos)
        
    def display_botao(self, tela: pygame.SurfaceType):
        if self.destacado:
            texto_render = self.fonte.render(self.texto, False, self.cor_destaque, self.cor_BG)
            pygame.draw.circle(tela, self.cor_destaque, (self.texto_rect.left - 15, self.texto_rect.center[1]), 10)
            pygame.draw.circle(tela, self.cor_destaque, (self.texto_rect.right + 15, self.texto_rect.center[1]), 10)
        else:
            texto_render = self.fonte.render(self.texto, False, self.cor, self.cor_BG)
        self.texto_rect = texto_render.get_rect(center = (self.x_pos, self.y_pos))
        tela.blit(texto_render, self.texto_rect)

    def atualizar(self, tela):
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
        elif self.texto_rect.collidepoint(pygame.mouse.get_pos()):
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

class Controle_desl:
    def __init__(self, pos, texto, fonte, tamanho_texto, tamanho_barra, percent, cor, cor_destaque = "Red", cor_BG = "Black", focado = False):
        self.x_pos = pos[0]
        self.y_pos = pos[1]

        self.barra_largura = tamanho_barra[0]
        self.barra_altura = tamanho_barra[1]
        self.barra = pygame.rect.Rect(self.x_pos + 10, self.y_pos - self.barra_altura//2, self.barra_largura, self.barra_altura)
        self.tamanho_controle = 2 * self.barra_altura
        self.percent = percent
        inicio = self.x_pos + percent * self.barra_largura - self.barra_altura
        self.controle = pygame.rect.Rect(inicio + 10, self.y_pos - self.tamanho_controle//2, self.tamanho_controle, self.tamanho_controle)

        self.cor = cor
        self.cor_destaque = cor_destaque
        self.destacado = False
        self.mouse = False
        self.focado = focado
        
        fonte = pygame.font.SysFont(fonte, tamanho_texto)
        self.texto_render = fonte.render(texto, False, self.cor, cor_BG)
        tamanho_texto = self.texto_render.get_size()[0]//2
        self.texto_rect = self.texto_render.get_rect(center = (self.x_pos - tamanho_texto - 10, self.y_pos))
        
    def display_botao(self, tela: pygame.SurfaceType):
        if self.percent > 1:
            self.percent = 1
        elif self.percent < 0:
            self.percent = 0
        tela.blit(self.texto_render, self.texto_rect)
        pygame.draw.rect(tela, self.cor, self.barra)
        if self.destacado:
            inicio = self.x_pos + self.percent * self.barra_largura - self.barra_altura
            self.controle = pygame.rect.Rect(inicio + 10, self.y_pos - self.tamanho_controle//2, self.tamanho_controle, self.tamanho_controle)
            pygame.draw.rect(tela, self.cor_destaque, self.controle)
        else:
            inicio = self.x_pos + self.percent * self.barra_largura - self.barra_altura
            self.controle = pygame.rect.Rect(inicio + 10, self.y_pos - self.tamanho_controle//2, self.tamanho_controle, self.tamanho_controle)
            pygame.draw.rect(tela, self.cor, self.controle)

    def atualizar(self, tela: pygame.SurfaceType):
        if self.controle.collidepoint(pygame.mouse.get_pos()) or self.focado:
            self.destacado = True
            if not self.focado:
                self.mouse = True
            if any(pygame.mouse.get_pressed()):
                novo_x = pygame.mouse.get_pos()[0] - self.tamanho_controle//2
                if novo_x <= self.barra.left - self.tamanho_controle//2:
                    novo_x = self.barra.left - self.tamanho_controle//2
                elif novo_x >= self.barra.right - self.tamanho_controle//2:
                    novo_x = self.barra.right - self.tamanho_controle//2
                self.controle = pygame.rect.Rect(novo_x, self.y_pos - self.tamanho_controle//2, self.tamanho_controle, self.tamanho_controle)
        else:
            self.destacado = False
            self.mouse = False

    def ler_posicao(self):
        pos_inicio = self.barra.left 
        pos_controle = self.controle.centerx
        posicao = (pos_controle - pos_inicio) / self.barra.width
        return posicao