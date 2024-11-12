import pygame, random, eventos
from typing import List
from abc import ABC, abstractmethod

class jogo(ABC):
    @abstractmethod
    def __init__(self, largura, altura, cor, musica, efeitos):
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.tamanho = (self.largura, self.altura)
        self.display = pygame.display.set_mode(self.tamanho)
        self.fundo = pygame.rect.Rect(0, 0, largura, altura)
        self.display.fill(self.cor)
        self.volume_musica = musica
        self.volume_efeitos = efeitos
        self.relogio = pygame.time.Clock()
        self.eventos : List[eventos.tubarao]= []
        self.frame_atual = 0
        self.contador_eventos = pygame.time.get_ticks()
        self.separador_eventos = 2000

    def atualizar(self):
        self.checar_eventos(None)
        self.gerar_eventos()
        if len(self.eventos) > 0:
            for evento in self.eventos:
                evento.aviso_direcao()
                evento.atualizar()
                if evento.matar():
                    self.eventos.remove(evento)
                    self.contador_eventos = pygame.time.get_ticks()
        self.checar_colisoes()
        pygame.display.flip()
        self.frame_atual += 1
    
    def desenhar(self):
        self.display.blit(self.fundo, (0, 0))
        self.obstaculos.draw(self.display)
        if len(self.eventos) > 0:
            for evento in self.eventos:
                evento.desenhar()
    
    def checar_eventos(self, evento):
        pass

    # @abstractmethod
    def checar_colisoes(self):
    # Colisão dos obstáculos com eventos
        for bloco in self.obstaculos:
            for evento in self.eventos:
                colisao = evento.verificar_colisao(bloco, 10)
                if colisao:
                    self.obstaculos.remove(bloco)

    def criar_obstaculos(self, vida, cor = (0, 0, 0), nome = None, alcance = 0):
        for num_linha, linha in enumerate(self.mapa):
            for num_coluna, coluna in enumerate(linha):
                if coluna == 'x':
                    esquerda = num_coluna * self.largura_blocos
                    topo = num_linha * self.altura_blocos
                    if (alcance != 0):
                        escolha = random.randint(1, alcance)
                        bloco = obstaculo(esquerda, topo, self.largura_blocos, self.altura_blocos, vida, nome = nome.format(escolha))    
                        self.obstaculos.add(bloco)
                    else:
                        bloco = obstaculo(esquerda, topo, self.largura_blocos, self.altura_blocos, vida, cor, nome)
                        self.obstaculos.add(bloco)
    
    # @abstractmethod
    def gerar_eventos(self):
        if len(self.eventos) == 0:
            if (pygame.time.get_ticks() - self.contador_eventos) >= self.separador_eventos:
                # self.eventos.append(eventos.tubarao(self.display, self.volume_efeitos))
                # self.eventos.append(eventos.caranguejo(self.display, self.volume_efeitos))
                # self.eventos.append(eventos.bando_aguas_vivas(self.display, self.volume_efeitos))
                # self.eventos.append(eventos.bola_de_feno(self.display, self.volume_efeitos))
                # self.eventos.append(eventos.verme_da_areia(self.display, self.volume_efeitos))
                # self.eventos.append(eventos.nuvem_gafanhotos(self.display, self.volume_efeitos))
                # self.eventos.append(eventos.invasores_do_espaco(self.display, self.volume_efeitos))
                # self.eventos.append(eventos.cometa(self.display, self.volume_efeitos))
                pass
    
class oceano(jogo):
    def __init__(self, largura, altura, cor, musica, efeitos):
        super().__init__(largura, altura, cor, musica, efeitos)
        pygame.display.set_caption("Mapa oceano")
        self.fundo = pygame.image.load("../assets/fundos/oceano_1.png")
        self.fundo = pygame.transform.scale(self.fundo, (self.largura, self.altura))
        self.mapa = mapa_oceano
        self.tamanho_mapa = (len(self.mapa[0]), len(self.mapa))
        self.largura_blocos = largura // self.tamanho_mapa[0]
        self.altura_blocos = altura // self.tamanho_mapa[1]
        self.obstaculos = pygame.sprite.Group()
        nome_obstaculo = "../assets/sprites/bloco_oceano_{0}.png"
        self.criar_obstaculos(100, nome = nome_obstaculo, alcance = 4)
        self.fundo_atual = 1

    def atualizar(self):
        super().atualizar()
        if self.frame_atual >= 30:
            self.frame_atual %= 30
            self.fundo_atual = (self.fundo_atual + 1) % 2
            self.fundo = pygame.image.load(f"../assets/fundos/oceano_{self.fundo_atual + 1}.png")
            self.fundo = pygame.transform.scale(self.fundo, (self.largura, self.altura))

class deserto(jogo):
    def __init__(self, largura, altura, cor, musica, efeitos):
        pygame.display.set_caption("Mapa deserto")
        super().__init__(largura, altura, cor, musica, efeitos)
        self.fundo = pygame.image.load("../assets/fundos/deserto_1.png")
        self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
        self.mapa = mapa_deserto
        self.tamanho_mapa = (len(self.mapa[0]), len(self.mapa))
        self.largura_blocos = largura // self.tamanho_mapa[0]
        self.altura_blocos = altura // self.tamanho_mapa[1]
        self.obstaculos = pygame.sprite.Group()
        nome_obstaculo = "../assets/sprites/bloco_deserto_{0}.png"
        self.criar_obstaculos(100, nome = nome_obstaculo, alcance = 4)
        self.fundo_atual = 1
    
    def atualizar(self):
        super().atualizar()
        if self.frame_atual >= 90:
            self.frame_atual %= 90
            self.fundo_atual = (self.fundo_atual + 1) % 2
            self.fundo = pygame.image.load(f"../assets/fundos/deserto_{self.fundo_atual + 1}.png")
            self.fundo = pygame.transform.scale(self.fundo, (self.largura, self.altura))

class espaco(jogo):
    def __init__(self, largura, altura, cor, musica, efeitos):
        super().__init__(largura, altura, cor, musica, efeitos)
        pygame.display.set_caption("Mapa espaco")
        self.fundo = pygame.image.load("../assets/fundos/espaco_1.png")
        self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
        self.mapa = mapa_espaco
        self.tamanho_mapa = (len(self.mapa[0]), len(self.mapa))
        self.largura_blocos = largura // self.tamanho_mapa[0]
        self.altura_blocos = altura // self.tamanho_mapa[1]
        self.obstaculos = pygame.sprite.Group()
        nome_obstaculo = "../assets/sprites/bloco_espaco_{0}.png"
        self.criar_obstaculos(100, nome = nome_obstaculo, alcance = 4)
        self.fundo_atual = 1

    def atualizar(self):
        super().atualizar()
        if self.frame_atual >= 30:
            self.frame_atual %= 30
            self.fundo_atual = (self.fundo_atual + 1) % 2
            self.fundo = pygame.image.load(f"../assets/fundos/espaco_{self.fundo_atual + 1}.png")
            self.fundo = pygame.transform.scale(self.fundo, (self.largura, self.altura))

class obstaculo(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, vida, cor = (150,150,150), nome = None):
        super().__init__()
        if nome == None:
            self.image = pygame.Surface((largura, altura))
            self.image.fill(cor)
            self.rect = self.image.get_rect(topleft = (x, y))
        else:
            self.image = pygame.image.load(nome)
            self.image = pygame.transform.scale(self.image, (largura, altura))
            self.rect = self.image.get_rect(topleft = (x, y))
        self.vida = vida
        
mapa_oceano = [
    [" "," "," "," "," "," "," "," "," "," "," ","x","x","x","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," ","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x"," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x"," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," ","x"," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," ","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," ",],
    [" "," "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," ",],
    [" "," "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," ",],
    [" "," "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "," ",],
    [" "," "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "," ",],
    [" "," "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "," ",],
    [" "," "," "," "," ","x","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x","x"," "," "," "," "," ",],
    [" "," "," "," "," ","x","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x","x"," "," "," "," "," ",],
    [" "," "," "," "," ","x","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x","x"," "," "," "," "," ",],
    [" "," "," "," "," ","x","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x","x"," "," "," "," "," ",]
]

mapa_deserto = [
    [" "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," ","x"," "," "," "," ","x"," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," ","x","x","x","x","x","x"," "," "," "," "," "," "," "," "," "," ","x","x","x","x","x","x"," "," "," "," "," ",],
    [" "," "," "," "," "," ","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x"," "," "," "," "," "," ",],
    [" "," "," "," "," "," ","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x"," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," ","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x"," "," "," "," "," "," ",],
    [" "," "," "," "," "," ","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x"," "," "," "," "," "," ",],
    [" "," "," "," "," ","x","x","x","x","x","x"," "," "," "," "," "," "," "," "," "," ","x","x","x","x","x","x"," "," "," "," "," ",]
]

mapa_espaco = [
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," "," ","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x"," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," ","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x"," "," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "]
]
