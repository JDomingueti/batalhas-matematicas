import pygame, random
from abc import ABC, abstractmethod
from math import sin

''' Arquivo para implementação dos eventos dos cenários '''

class evento(ABC):
    @abstractmethod
    def __init__(self, tela: pygame.Surface, volume_efeitos):
        self.largura_tela = tela.get_width()
        self.altura_tela = tela.get_height()
        self.tela = tela
        self.comecou = False
        self.volume_efeitos = volume_efeitos
        self.lado_inicio = random.choice([-1,1])
        self.contador = pygame.time.get_ticks()
        self.caminho = "../assets/eventos/"

    def aviso_direcao(self):
        if self.comecou and (pygame.time.get_ticks() - self.contador <= 2500):
            self.tela.blit(self.img_aviso, self.rect_aviso)

    @abstractmethod
    def atualizar(self):
        if not self.comecou:
            self.contador = pygame.time.get_ticks()
            self.som.play(-1, fade_ms=2000)
            self.som.set_volume(self.volume_efeitos)
            self.comecou = True

    @abstractmethod
    def desenhar(self):
        pass

    @abstractmethod
    def verificar_colisao(self, rect_obj : pygame.Rect, dano: int):
        pass

    @abstractmethod
    def matar(self):
        pass

    @abstractmethod
    def pegar_rect(self):
        pass


class explosao(evento):
    def __init__(self, rect: pygame.Rect, tela: pygame.Surface, volume_efeitos: pygame.mixer.Sound):
        self.tela = tela
        caminho = "../assets/eventos/"
        self.imgs = []
        for i in range(1,4):
            img = pygame.image.load(caminho + f"explosao/{i}.png")
            img = pygame.transform.scale(img, rect.size)
            self.imgs.append(img)
        self.rect = pygame.Rect(rect.topleft, rect.size)
        self.volume_efeitos = volume_efeitos
        self.som = pygame.mixer.Sound(caminho + "sons/explosion.wav")
        self.comecou = False
        self.destruir = False
        self.sprite_atual = 0
        self.frame_atual = 0
        self.frames_por_sprites = 20

    def aviso_direcao(self):
        pass

    def atualizar(self):
        if not self.comecou:
            self.som.play(fade_ms=100)
            self.som.set_volume(self.volume_efeitos)
        if (self.frame_atual >= self.frames_por_sprites):
            if self.sprite_atual < 2:
                self.frame_atual = 0
                self.sprite_atual += 1
            else:

                self.destruir = True
        self.frame_atual += 1

    def desenhar(self):
        self.tela.blit(self.imgs[self.sprite_atual], self.rect)

    def verificar_colisao(self, rect_obj: pygame.Rect, dano: int):
        pass

    def matar(self, callback):
        if self.destruir:
            self.som.fadeout(100)
        return self.destruir

    def pegar_rect(self):
        return None