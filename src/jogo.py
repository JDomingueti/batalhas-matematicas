import pygame, random #, json
from typing import List
from abc import ABC, abstractmethod
from eventos import evento, eventos_oceano, eventos_deserto, eventos_espaco

class jogo(ABC):
    @abstractmethod
    def __init__(self, largura, altura, cor, musica, efeitos, display):
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.tamanho = (self.largura, self.altura)
        self.display = display
        if pygame.display.is_fullscreen():
            self.display = pygame.display.set_mode((largura, altura), pygame.FULLSCREEN)
        else:
            self.display = pygame.display.set_mode((largura, altura))
        self.fundo = pygame.rect.Rect(0, 0, largura, altura)
        self.display.fill(self.cor)
        self.volume_musica = musica
        self.volume_efeitos = efeitos
        self.relogio = pygame.time.Clock()
        self.eventos : List[evento.evento]= []
        self.frame_atual = 0
        self.contador_eventos = pygame.time.get_ticks()
        self.separador_eventos = 2000

        # self.player_1 = ...(...)
        # self.player_2 = ...(...)
        # self.inimigos = []
        # with open("...", "r", encoding="utf-8") as config_file:
        #   self.configuracoes = json.load(config_file)

    def atualizar(self):
        self.gerar_eventos()
        if len(self.eventos) > 0:
            for evento in self.eventos:
                evento.aviso_direcao()
                evento.atualizar()
                if evento.matar(self.explodir):
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

    # @abstractmethod
    def checar_colisoes(self):
    # Colisão dos tiros
        # Com obstáculos
        # ...
        # Com eventos
        # ...
        # Com players
        # ...
        # Com inimigos
        # ...
    # Colisão dos obstáculos
        for bloco in self.obstaculos:
            # Com eventos
            for evento in self.eventos:
                colisao = evento.verificar_colisao(bloco, 10)
                if colisao:
                    self.obstaculos.remove(bloco)
            # Com players
            # ...
            # Com inimigos
            # ...
    # Colisão eventos
        # Com players
        # ...
        # Com inimigos
        # ...
    # Colisão players
        # Com inimigos
        # ...
    
    def gerar_inimigos(self):
        # Implementar geração de inimigos
        # ...
        pass

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
    
    def movimento_players(self, eventos : pygame.key):
        # Movimento player_1
        # ...
        # Movimento player_2
        # ...
        pass

    @abstractmethod
    def gerar_eventos(self):
        pass
    
    def explodir(self, rect):
        if isinstance(rect, pygame.Rect):
            self.eventos.append(evento.explosao(rect, self.display, self.volume_efeitos))

class oceano(jogo):
    def __init__(self, largura, altura, cor, musica, efeitos, display):
        super().__init__(largura, altura, cor, musica, efeitos, display)
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
        self.chances = {
            'tubarao': 0.3,
            'caranguejo': 0.3,
            'bando_aguas_vivas': 0.4
        }

    def atualizar(self):
        super().atualizar()
        if self.frame_atual >= 30:
            self.frame_atual %= 30
            self.fundo_atual = (self.fundo_atual + 1) % 2
            self.fundo = pygame.image.load(f"../assets/fundos/oceano_{self.fundo_atual + 1}.png")
            self.fundo = pygame.transform.scale(self.fundo, (self.largura, self.altura))

    def gerar_eventos(self):
        if len(self.eventos) == 0:
            if (pygame.time.get_ticks() - self.contador_eventos) >= self.separador_eventos:
                chance_tubarao = random.random()
                if chance_tubarao <= self.chances['tubarao']:
                    self.eventos.append(eventos_oceano.tubarao(self.display, self.volume_efeitos))
                chance_caranguejo = random.random()
                if chance_caranguejo <= self.chances['caranguejo']:
                    self.eventos.append(eventos_oceano.caranguejo(self.display, self.volume_efeitos))
                chance_bando_aguas_vivas = random.random()
                if chance_bando_aguas_vivas <= self.chances['bando_aguas_vivas']:
                    self.eventos.append(eventos_oceano.bando_aguas_vivas(self.display, self.volume_efeitos))

class deserto(jogo):
    def __init__(self, largura, altura, cor, musica, efeitos, display):
        super().__init__(largura, altura, cor, musica, efeitos, display)
        pygame.display.set_caption("Mapa deserto")
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
        self.chances = {
            "bola_de_feno" : 0.4,
            "verme_da_areia" : 0.3,
            "nuvem_gafanhotos" : 0.3
        }
    
    def atualizar(self):
        super().atualizar()
        if self.frame_atual >= 90:
            self.frame_atual %= 90
            self.fundo_atual = (self.fundo_atual + 1) % 2
            self.fundo = pygame.image.load(f"../assets/fundos/deserto_{self.fundo_atual + 1}.png")
            self.fundo = pygame.transform.scale(self.fundo, (self.largura, self.altura))

    def gerar_eventos(self):
        if len(self.eventos) == 0:
            if (pygame.time.get_ticks() - self.contador_eventos) >= self.separador_eventos:
                chance_bola_de_feno = random.random()
                if chance_bola_de_feno <= self.chances['bola_de_feno']:
                    self.eventos.append(eventos_deserto.bola_de_feno(self.display, self.volume_efeitos))
                chance_verme_da_areia = random.random()
                if chance_verme_da_areia <= self.chances['verme_da_areia']:
                    self.eventos.append(eventos_deserto.verme_da_areia(self.display, self.volume_efeitos))
                chance_nuvem_gafanhotos = random.random()
                if chance_nuvem_gafanhotos <= self.chances['nuvem_gafanhotos']:
                    self.eventos.append(eventos_deserto.nuvem_gafanhotos(self.display, self.volume_efeitos))
                self.contador_eventos = pygame.time.get_ticks()

class espaco(jogo):
    def __init__(self, largura, altura, cor, musica, efeitos, display):
        super().__init__(largura, altura, cor, musica, efeitos, display)
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
        self.chances = {
            "cometa" : 0.4,
            "space" : 0.3
        }

    def atualizar(self):
        super().atualizar()
        if self.frame_atual >= 30:
            self.frame_atual %= 30
            self.fundo_atual = (self.fundo_atual + 1) % 2
            self.fundo = pygame.image.load(f"../assets/fundos/espaco_{self.fundo_atual + 1}.png")
            self.fundo = pygame.transform.scale(self.fundo, (self.largura, self.altura))

    def gerar_eventos(self):
        if len(self.eventos) == 0:
            if (pygame.time.get_ticks() - self.contador_eventos) >= self.separador_eventos:
                chance_cometa = random.random()
                if chance_cometa <= self.chances['cometa']:
                    self.eventos.append(eventos_espaco.cometa(self.display, self.volume_efeitos))
                chance_space = random.random()
                if chance_space <= self.chances['space']:
                    self.eventos.append(eventos_espaco.invasores_do_espaco(self.display, self.volume_efeitos))
                self.contador_eventos = pygame.time.get_ticks()

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
