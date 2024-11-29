import pygame
import time
from tiro import Tiro

'''
Arquivo de códigos criado com o intuito de armazenar
as linhas de código dos veículos utilizados no jogo.
'''

class Veiculo:
    '''
    Classe criada com as configurações gerais dos
    veículos que serão controlados pelos jogadores.
    '''
    def __init__(self, caminho_imagem, x, y, largura_tela, altura_tela, tamanho_veiculo, teclas, tiro_inverso=False):
        
        '''
        Método que carrega e ajusta as configurações iniciais 
        dos veículos, 

        Parâmetros
        ----------
        caminho_imagem: str
            caminha da imagem do veículo

        x: float
            posição inicial no eixo x do veículo
    

        y: float
            posição inicial no eixo y do veículo
        
        largura_tela: float
            largura da tela
        
        altura_tela: float
            altura da tela

        tamanho_veículo: float
            tamanho do veículo nos eixos x e y

        teclas: dict
            Dicionário que guarda as teclas que o jogador
            irá utilizar para movimentar o veículo
        
        tiro_inverso: Boolean
            Se (tiro_inverso == False) o veículo inicia atirando da esquerda para direita
            Se (tiro_inverso = True) o veículo inicia atirando da direita para esquerda

        integridade: float
            Pontos de vida do veículo/jogador

        velocidade: float
            Velocidade do veículo
        
        angulo: float
            Ângulo que guarda a direção dos tiros do veículo
        
        tiro: List[Tiro]
            Lista que guarda os tiros ativos (que estão na tela
                e ainda não colidiram) do veículo
        
        dano: float
            Dano causado pelos tiros do veículo
        
        ultimo_disparo: float
            momento do último disparo
        
        intervalo_tiro: float
            intervalo de tempo mínimo entre cada disparo
        
        velocidade_tiro: float
            velocidade dos tiros do veículo    
        '''


        self.caminho_imagem = caminho_imagem
        self.x = x
        self.y = y
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.tamanho_veiculo = tamanho_veiculo
        self.teclas = teclas
        self.tiro_inverso = tiro_inverso

        self.integridade = 100
        self.velocidade = 10
        self.angulo = 0
        self.tiros = []
        self.dano = 1
        self.ultimo_disparo = 0 
        self.intervalo_tiro = 1
        self.velocidade_tiro = 10


    def processar_movimento(self, keys, is_v1=True):
        '''
        Método para processar o movimento do veículo

        Parâmetros:
        ----------
        keys: ScancoderWrapper
            decta quais teclas foram precionadas
            
        is_v1: Boolean
            Se (is_v1 == True) o presente veículo é o jogador 1 (esquerda)
            Se (is_v1 == False) o presente veículo é o jogador 2 (direita)

        '''
        keys = pygame.key.get_pressed()
        # variação da posição conforme as teclas são apertadas
        dx, dy = 0, 0
        
        if keys[self.teclas['esquerda']]:
            dx = -self.velocidade
        if keys[self.teclas['direita']]:
            dx = self.velocidade
        if keys[self.teclas['cima']]:
            dy = -self.velocidade
        if keys[self.teclas['baixo']]:
            dy = self.velocidade
        
        #atualização da posição horizontal
        novo_x = self.x + dx
        if(0 <= novo_x and novo_x <= self.largura_tela - self.tamanho_veiculo): self.x = novo_x
        # atualização da posição vertical
        novo_y = self.y + dy
        if(50 <= novo_y and novo_y <= self.altura_tela - self.tamanho_veiculo): self.y = novo_y

    def rotacionar(self):
        '''
        Método para rotacionar o veículo
        '''
        keys = pygame.key.get_pressed()
        
        # Se a tecla de rotação anti horária foi
        # apertada o ângulo aumenta
        if keys[self.teclas['rotacao_anti_horaria']]:
            self.angulo += 3
        
        # Se a tecla de rotação horária foi
        # apertada o ângulo aumenta
        if keys[self.teclas['rotacao_horaria']]:
            self.angulo -= 3
                
    def disparar(self, is_v1=True):
        '''
        Método para gerar os tiros e adicionar na lista self.tiros

        Parâmetros:
        -----------
        is_v1: Boolean
            Se (is_v1 == True) o presente veículo é o jogador 1 (esquerda)
            Se (is_v1 == False) o presente veículo é o jogador 2 (direita)
        '''
        tempo_atual = time.time()
        if tempo_atual - self.ultimo_disparo >= self.intervalo_tiro:
            centro_x = self.x + self.tamanho_veiculo / 2
            centro_y = self.y + self.tamanho_veiculo / 2
            angulo_tiro  = self.angulo
            if self.tiro_inverso:
                angulo_tiro += 180
            novo_tiro = Tiro(centro_x, centro_y, angulo_tiro, self.velocidade_tiro)
            self.tiros.append(novo_tiro)
            self.ultimo_disparo = tempo_atual

    def draw(self, surface):
        '''
        Método para desenhar o jogador e os seus tiros

        Parâmetros:
        -----------
        surface: Surface
            Imagem da tela
        '''
        imagem = pygame.image.load(self.caminho_imagem) #carregando imagem
        imagem = pygame.transform.scale(imagem, (self.tamanho_veiculo, self.tamanho_veiculo)) # mudando escala
        imagem_rotacionada = pygame.transform.rotate(imagem, self.angulo) # rotacionando imagem
        novo_retangulo = imagem_rotacionada.get_rect(center=(self.x + self.tamanho_veiculo / 2, self.y + self.tamanho_veiculo / 2))
        surface.blit(imagem_rotacionada, novo_retangulo.topleft)
        
        # Desenha os tiros
        for tiro in self.tiros:
            tiro.draw(surface)

    def atualizar_tiros(self):
        '''
        Método para mover os tiros e retirá-los quando saírem da tela
        '''
        for tiro in self.tiros[:]:
            tiro.mover()
            if tiro.x < 0 or tiro.x > self.largura_tela or tiro.y < 0 or tiro.y > self.altura_tela:
                self.tiros.remove(tiro)

    def mostrar_integridade(self, tela, posicao_texto):
        '''
        Método para mostra a integridade na tela

        Parâmetros:
        -----------
        tela: Surface
            Imagem da tela

        posicao_texto: List[float]
            Em que posição o texto será desenhado
        '''
        fonte = pygame.font.Font(None, 36)
        texto = fonte.render(f"Integridade: {self.integridade:,.2f}", True, (0, 0, 0))
        tela.blit(texto, posicao_texto)