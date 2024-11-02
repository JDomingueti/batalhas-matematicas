import pygame

# TODO: Implementar novos botões (Caixa de selecção
# e slider)

# TODO: Estilizar

pygame.font.init()

class Botao:
    def __init__(self, pos, texto, fonte, tamanho, cor, cor_destaque, cor_BG = "Black", focado = False):
        self.x_pos = pos[0]
        self.x_inicial = self.x_pos
        self.y_pos = pos[1]
        
        self.focado = focado
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
        self.som.set_volume(0.3)
        
    def display_botao(self, tela: pygame.SurfaceType):
        texto_render = self.fonte.render(self.texto, False, self.cor, self.cor_BG)
        self.texto_rect = texto_render.get_rect(center = (self.x_pos, self.y_pos))
        tela.blit(texto_render, self.texto_rect)
        
        if self.destacado:
            pygame.draw.circle(tela, self.cor_destaque, (self.texto_rect.left - 15, self.texto_rect.center[1]), 10)
            pygame.draw.circle(tela, self.cor_destaque, (self.texto_rect.right + 15, self.texto_rect.center[1]), 10)
    
    def atualizar(self, tela):
        if self.texto_rect.collidepoint(pygame.mouse.get_pos()) or self.focado:
            if not self.destacado:
                self.destacado = True
                self.cor = self.cor_destaque
                self.display_botao(tela)
                pygame.mixer.Sound.play(self.som, fade_ms= 2)
            self.x_pos += self.direcao
            if self.x_pos >= self.x_inicial + 2:
                self.direcao = -0.1
            elif self.x_pos <= self.x_inicial - 2:
                self.direcao = 0.1
        else:
            if self.destacado:
                self.destacado = False
                self.cor = self.cor_original
                self.display_botao(tela)
            if (self.x_pos != self.x_inicial):
                if self.x_pos > self.x_inicial:
                    self.direcao = -0.1
                if self.x_pos < self.x_inicial:
                    self.direcao = 0.1
                self.x_pos += self.direcao