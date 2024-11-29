import pygame
import math

class Tiro:
    def __init__(self, x, y, angulo, velocidade, cor = (255, 255, 0), dano_tiro=5):
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.angulo = angulo
        self.raio = 5
        self.dano_tiro = dano_tiro
        self.cor = cor
        self.ativo = True
    
    def mover(self):
        # Calcula o movimento a partir do ângulo fornecido
        self.x += math.cos(math.radians(self.angulo)) * self.velocidade
        self.y -= math.sin(math.radians(self.angulo)) * self.velocidade  # Y diminui para cima na tela
        
    def draw(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)