import pygame
import time

class PowerUp:
    def __init__(self, path_image, x, y, efeito, tamanho_veiculo):
        self.x = x
        self.y = y
        self.tamanho_veiculo = tamanho_veiculo
        self.image = pygame.image.load(path_image)
        self.image = pygame.transform.scale(self.image, (self.tamanho_veiculo, self.tamanho_veiculo))
        self.rect = pygame.Rect(self.x, self.y, self.tamanho_veiculo, self.tamanho_veiculo)
        self.tempo_vida = 5  # dura 5 segundos
        self.criado_em = time.time()
        self.efeito = efeito

    def aplicar_efeito(self, veiculo):
        if self.efeito == "velocidade":
            veiculo.velocidade += 2
        elif self.efeito == "vida":
            veiculo.integridade = min(100, veiculo.integridade + 20)
        elif self.efeito == "tiro":
            veiculo.velocidade_tiro += 5
        elif self.efeito == "dano":
            veiculo.dano += 1

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def expirado(self):
        return time.time() - self.criado_em > self.tempo_vida