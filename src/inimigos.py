import pygame
from abc import ABC, abstractmethod
import math
import time
from tiro import Tiro
from powerups import PowerUp

class Inimigo(pygame.sprite.Sprite, ABC):
    '''
    Classe dos inimigos do jogo.

    Atributos
    ---------
    tamanho: int
        Dimensão do veículo

    image: Surface
        Sprite do inimigo
    
    rect.x: int
        Posição do inimigo em relação ao eixo x

    rect.y: int
        Posição do inimigo em relação ao eixo y

    largura_tela: int
        Largura da tela

    altura_tela: int
        Altura da tela

    velocidade: int
        Velocidade padrão do inimigo
    
    velocidade_vertical: int
        Velocidade vertical do inimigo

    velocidade_horizontal: int
        Velocidade horizontal do inimigo

    ultimo_tempo_colisao: float
        Última vez que o inimigo colidiu com outro objeto

    angulo: float
        Ãngulo em que o inimigo atira

    tiros: list
        Lista que guarda os tiros do inimigo

    ultimo_disparo: float
        Última vez que o inimigo disparou

    intervalo_tiro: float
        Intervalo em segundos de um tiro e outro

    limite_distancia: int
        Distância mínima que um inimigo pode estar de um veículo
    
    integridade: float
        Integridade (vida) do inimigo

    powerup_image: str
        Sprite do powerup

    powerup_efeito: str
        Efeito correspondente ao powerup

    Métodos
    -------
    Métodos da classe:
        - __init__(path_image, x, largura_tela, altura_tela, tamanho, powerup_image, powerup_efeito)
        - perseguir_veiculo(veiculos)
        - disparar(veiculos)
        - draw(surface)
        - atualizar_tiros()
        - colisao(tiro, veiculos, powerups)
        - update(tiros, veiculos, powerups)
    '''
        
    def __init__(self, path_image, x, largura_tela, altura_tela, tamanho, powerup_image, powerup_efeito):
        '''
        Inicializa a classe Inimigo.

        Parâmetros
        ----------
        path_image: str
            Caminho do sprite do inimigo
        
        x: int
            Posição do inimigo em relação ao eixo x

        largura_tela: int
            Largura da tela

        altura_tela: int
            Altura da tela
        
        tamanho: int
            Dimensão do veículo

        powerup_image: str
            Sprite do powerup

        powerup_efeito: str
            Efeito correspondente ao powerup
        
        '''
        super().__init__() 
        self.tamanho = tamanho
        self.image = pygame.image.load(path_image)
        self.image = pygame.transform.scale(self.image, (self.tamanho, self.tamanho))  
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
        '''
        IA que faz os inimigos perseguirem os veículos.

        Parâmetros
        ----------
        veiculos: list
            Lista contendo o veiculo 1 (v1) e o veículo 2 (v2) 
        '''
        veiculo_proximo = min(veiculos, key=lambda veiculo: pygame.Vector2(veiculo.x, veiculo.y).distance_to(self.rect.center))
        direcao = pygame.Vector2(veiculo_proximo.x - self.rect.x, veiculo_proximo.y - self.rect.y)
        distancia_ate_veiculo = direcao.length()

        if distancia_ate_veiculo > self.limite_distancia:
            movimento = direcao.normalize() * self.velocidade
            self.rect.x += movimento.x
            self.rect.y += movimento.y
            self.angulo = -math.degrees(math.atan2(direcao.y, direcao.x))

            self.rect.x = max(0, min(self.largura_tela - self.tamanho, self.rect.x))
            self.rect.y = max(0, min(self.altura_tela - self.tamanho, self.rect.y))

    def disparar(self, veiculos):
        '''
        Função que faz os inimigos dispararem.

        Parâmetros
        ----------
        veiculos: list
            Lista contendo o veiculo 1 (v1) e o veículo 2 (v2) 
        '''
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
        '''
        Função que desenha as imagens dos inimigos e dos tiros.

        Parâmetros
        ----------
        surface: Surface
            Imagem do inimigo e do tiro
        '''
        image_rotacionada = pygame.transform.rotate(self.image, self.angulo+180)
        novo_retangulo = image_rotacionada.get_rect(topleft=(self.rect.x, self.rect.y))
        surface.blit(image_rotacionada, novo_retangulo)
        for tiro in self.tiros:
            tiro.draw(surface)

    def atualizar_tiros(self):
        '''
        Função que atualiza os tiros.
        '''
        for tiro in self.tiros[:]:
            tiro.mover()
            if tiro.x < 0 or tiro.x > self.largura_tela or tiro.y < 0 or tiro.y > self.altura_tela:
                self.tiros.remove(tiro)
    
    def colisao(self, tiro, veiculos, powerups):
        '''
        Função que checa colisão entre os inimigos e os tiros para gerar os powerups.

        Parâmetros
        ----------
        tiro: Surface
            Tiro dos veículos

        veiculos: list
            Lista contendo o veiculo 1 (v1) e o veículo 2 (v2)

        powerups: Surface
            Sprites dos powerups
        '''
        if tiro != None:
            if self.rect.colliderect(pygame.Rect(tiro.x - tiro.raio, tiro.y - tiro.raio, tiro.raio * 2, tiro.raio * 2)):
                self.integridade -= veiculos.dano

                if self.integridade <= 0:
                    powerup = PowerUp(self.powerup_image, self.rect.x, self.rect.y, self.powerup_efeito, self.tamanho)
                    powerups.append(powerup)
                return True  # Remove o inimigo da lista
        return False

    @abstractmethod
    def update(self, tiros, veiculos, powerups):
        '''
        Função que chama outras funções.

        Parâmetros
        ----------
        tiros: list
            Lista que guarda os tiros do inimigo

        veiculos: list
            Lista contendo o veiculo 1 (v1) e o veículo 2 (v2)

        powerups: Surface
            Sprites dos powerups
        '''
        self.perseguir_veiculo(veiculos)
        self.disparar(veiculos) 
        self.atualizar_tiros()

class Inimigo1(Inimigo):
    '''
    Inimigo que gera o powerup de "vida".
    '''      
    def __init__(self, path_image, x, largura_tela, altura_tela, tamanho, powerup_img, powerup_efeito):
        super().__init__(path_image, x, largura_tela, altura_tela, tamanho, powerup_img, powerup_efeito)

    def update(self, tiros, veiculos, powerups):  
        return super().update(tiros, veiculos, powerups)

class Inimigo2(Inimigo): 
    '''
    Inimigo que gera o powerup de "velocidade".
    '''      
    def __init__(self, path_image, x, largura_tela, altura_tela, tamanho, powerup_img, powerup_efeito):
        super().__init__(path_image, x, largura_tela, altura_tela, tamanho, powerup_img, powerup_efeito)

    def update(self, tiros, veiculos, powerups):  
        return super().update(tiros, veiculos, powerups)

class Inimigo3(Inimigo):
    '''
    Inimigo que gera o powerup de "tiro".
    ''' 
    def __init__(self, path_image, x, largura_tela, altura_tela, tamanho, powerup_img, powerup_efeito):
        super().__init__(path_image, x, largura_tela, altura_tela, tamanho, powerup_img, powerup_efeito)

    def update(self, tiros, veiculos, powerups):  
        return super().update(tiros, veiculos, powerups)

class Inimigo4(Inimigo):
    '''
    Inimigo que gera o powerup de "dano".
    ''' 
    def __init__(self, path_image, x, largura_tela, altura_tela, tamanho, powerup_img, powerup_efeito):
        super().__init__(path_image, x, largura_tela, altura_tela, tamanho, powerup_img, powerup_efeito)

    def update(self, tiros, veiculos, powerups):  
        return super().update(tiros, veiculos, powerups)