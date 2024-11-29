import pygame
from abc import ABC, abstractmethod
import math
import time
from tiro import Tiro
from powerups import PowerUp

class Inimigo(pygame.sprite.Sprite, ABC):
    def __init__(self, path_image, x, largura_tela, altura_tela, tamanho_veiculo, powerup_image, powerup_efeito):
        super().__init__() 
        self.tamanho_veiculo = tamanho_veiculo
        self.image = pygame.image.load(path_image)
        self.image = pygame.transform.scale(self.image, (self.tamanho_veiculo, self.tamanho_veiculo))  
        self.rect = self.image.get_rect()  
        self.rect.x = x
        self.rect.y = 50
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.velocidade = 2
        self.velocidade_vertical = 2
        self.velocidade_horizontal = 3
        self.ultimo_tempo_colisao = pygame.time.get_ticks()
        self.angulo = 0
        self.tiros = []
        self.ultimo_disparo = 0
        self.intervalo_tiro = 5 # 5 segundos
        self.limite_distancia = 200
        self.integridade = 10
        self.powerup_image = powerup_image
        self.powerup_efeito = powerup_efeito
           
    def perseguir_veiculo(self, veiculos):
        veiculo_proximo = min(veiculos, key=lambda veiculo: pygame.Vector2(veiculo.x, veiculo.y).distance_to(self.rect.center))
        direcao = pygame.Vector2(veiculo_proximo.x - self.rect.x, veiculo_proximo.y - self.rect.y)
        distancia_ate_veiculo = direcao.length()

        if distancia_ate_veiculo > self.limite_distancia:
            movimento = direcao.normalize() * self.velocidade
            self.rect.x += movimento.x
            self.rect.y += movimento.y
            self.angulo = -math.degrees(math.atan2(direcao.y, direcao.x))

            self.rect.x = max(0, min(self.largura_tela - self.tamanho_veiculo, self.rect.x))
            self.rect.y = max(0, min(self.altura_tela - self.tamanho_veiculo, self.rect.y))

    def disparar(self, veiculos):
        veiculo_proximo = min(veiculos, key=lambda veiculo: pygame.Vector2(veiculo.x, veiculo.y).distance_to(self.rect.center))
        direcao_x = veiculo_proximo.x - self.rect.x
        direcao_y = veiculo_proximo.y - self.rect.y
        self.angulo = -math.degrees(math.atan2(direcao_y, direcao_x))

        tempo_atual = time.time()
        if tempo_atual - self.ultimo_disparo >= self.intervalo_tiro:
            centro_x = self.rect.centerx
            centro_y = self.rect.centery
            novo_tiro = Tiro(centro_x, centro_y, self.angulo, 3, (255, 0, 0))
            self.tiros.append(novo_tiro)
            self.ultimo_disparo = tempo_atual

    def draw(self, surface):
        image_rotacionada = pygame.transform.rotate(self.image, self.angulo+180)
        novo_retangulo = image_rotacionada.get_rect(topleft=(self.rect.x, self.rect.y))
        surface.blit(image_rotacionada, novo_retangulo)
        for tiro in self.tiros:
            tiro.draw(surface)

    def atualizar_tiros(self):
        for tiro in self.tiros[:]:
            tiro.mover()
            if tiro.x < 0 or tiro.x > self.largura_tela or tiro.y < 0 or tiro.y > self.altura_tela:
                self.tiros.remove(tiro)
    
    def colisao(self, tiro, veiculos, powerups):
        if tiro != None:
            if self.rect.colliderect(pygame.Rect(tiro.x - tiro.raio, tiro.y - tiro.raio, tiro.raio * 2, tiro.raio * 2)):
                self.integridade -= veiculos.dano

                if self.integridade <= 0:
                    powerup = PowerUp(self.powerup_image, self.rect.x, self.rect.y, self.powerup_efeito, self.tamanho_veiculo)
                    powerups.append(powerup)
                return True  # Remove o inimigo da lista
        return False

    @abstractmethod
    def update(self, tiros, veiculos, powerups):
        self.perseguir_veiculo(veiculos)
        self.disparar(veiculos) 
        self.atualizar_tiros()

class Inimigo1(Inimigo):       
    def __init__(self, path_image, x, largura_tela, altura_tela, tamanho_veiculo, powerup_img, powerup_efeito):
        super().__init__(path_image, x, largura_tela, altura_tela, tamanho_veiculo, powerup_img, powerup_efeito)

    def update(self, tiros, veiculos, powerups):  
        return super().update(tiros, veiculos, powerups)

class Inimigo2(Inimigo):       
    def __init__(self, path_image, x, largura_tela, altura_tela, tamanho_veiculo, powerup_img, powerup_efeito):
        super().__init__(path_image, x, largura_tela, altura_tela, tamanho_veiculo, powerup_img, powerup_efeito)

    def update(self, tiros, veiculos, powerups):  
        return super().update(tiros, veiculos, powerups)

class Inimigo3(Inimigo):       
    def __init__(self, path_image, x, largura_tela, altura_tela, tamanho_veiculo, powerup_img, powerup_efeito):
        super().__init__(path_image, x, largura_tela, altura_tela, tamanho_veiculo, powerup_img, powerup_efeito)

    def update(self, tiros, veiculos, powerups):  
        return super().update(tiros, veiculos, powerups)

class Inimigo4(Inimigo):       
    def __init__(self, path_image, x, largura_tela, altura_tela, tamanho_veiculo, powerup_img, powerup_efeito):
        super().__init__(path_image, x, largura_tela, altura_tela, tamanho_veiculo, powerup_img, powerup_efeito)

    def update(self, tiros, veiculos, powerups):  
        return super().update(tiros, veiculos, powerups)