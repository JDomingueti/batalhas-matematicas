import pygame
import time

class PowerUp:
    '''
    Classe dos powerups do jogo.

    Atributos
    ---------
    x: int
        Posição do powerup em relação ao eixo x

    y: int
        Posição do powerup em relação ao eixo y
        
    tamanho: int
        Dimensão do powerup

    image: Surface
        Sprite do powerup

    rect: Rect
        Retângulo do powerup

    tempo_vida: int
        Tempo em segundos para o powerup expirar

    criado_em: float
        Momento em que o powerup foi criado

    efeito: str
        Efeito correspondente ao powerup

    Métodos
    -------
    Métodos da classe:
        - __init__(path_image, x, y, efeito, tamanho)
        - aplicar_efeito(veiculo)
        - draw(surface)
        - expirado()
    '''

    def __init__(self, path_image, x, y, efeito, tamanho):
        '''
        Inicializa a classe PowerUp.

        Parâmetros
        ----------
        path_image: str
            Caminho do sprite do powerup
        
        x: int
            Posição do powerup em relação ao eixo x

        y: int
            Posição do powerup em relação ao eixo y

        efeito: str
            Efeito correspondente ao powerup
        
        tamanho: int
            Dimensão do powerup       
        '''
        self.x = x
        self.y = y
        self.tamanho = tamanho
        self.image = pygame.image.load(path_image)
        self.image = pygame.transform.scale(self.image, (self.tamanho, self.tamanho))
        self.rect = pygame.Rect(self.x, self.y, self.tamanho, self.tamanho)
        self.tempo_vida = 5  # dura 5 segundos
        self.criado_em = time.time()
        self.efeito = efeito

    def aplicar_efeito(self, veiculo):
        '''
        Função que aplica o efeito no veiculo que colidir com o powerup.

        Parâmetros
        ----------
        veiculos: list
            Lista contendo o veiculo 1 (v1) e o veículo 2 (v2) 
        '''
        if self.efeito == "velocidade":
            veiculo.velocidade += 2
        elif self.efeito == "vida":
            veiculo.integridade = min(100, veiculo.integridade + 20)
        elif self.efeito == "tiro":
            veiculo.velocidade_tiro += 5
            veiculo.intervalo_tiro -= 0.05
        elif self.efeito == "dano":
            veiculo.dano += 1

    def draw(self, surface):
        '''
        Função que desenha as imagens dos powerups.

        Parâmetros
        ----------
        surface: Surface
            Imagem do powerup
        '''
        surface.blit(self.image, (self.x, self.y))

    def expirado(self):
        '''
        Função que faz com que o powerup expire.
        '''
        return time.time() - self.criado_em > self.tempo_vida