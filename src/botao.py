import pygame

pygame.font.init()

class botao:
    def __init__(self, pos, texto, fonte, tamanho, cor, cor_BG = "Black"):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.texto = texto
        self.fonte = pygame.font.SysFont(fonte, tamanho)
        self.cor = cor
        self.cor_BG = cor_BG
        self.texto = self.fonte.render(self.texto, False, self.cor, self.cor_BG)
        self.texto_rect : pygame.Rect = self.texto.get_rect(center = (self.x_pos, self.y_pos))

    def display_botao(self, screen: pygame.SurfaceType):
        screen.blit(self.texto, self.texto_rect)
    
    def verificar_clique(self, pos_do_mouse):
        if self.texto_rect.collidepoint(pos_do_mouse):
            return True