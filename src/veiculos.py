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
    def __init__(self, caminho_imagem, x, y, largura_tela, altura_tela, tamanho, teclas, tiro_inverso = False, volume_tiro = 1):
        
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

        tamanho: float
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
        pygame.init()

        self.caminho_imagem = caminho_imagem
        self.x = x
        self.y = y
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.tamanho = tamanho
        self.rect = pygame.Rect(self.x, self.y, self.tamanho, self.tamanho)
        self.teclas = teclas
        self.tiro_inverso = tiro_inverso
        
        self.imagem_padrao = pygame.image.load(self.caminho_imagem) #carregando imagem
        self.imagem_padrao = pygame.transform.scale(self.imagem_padrao, (self.tamanho, self.tamanho)) # mudando escala
        self.imagem = self.imagem_padrao
        self.ativo = True
        self.integridade = 100
        self.levou_dano = False
        self.intervalo_dano = 100
        self.som_tiro = pygame.mixer.Sound("../assets/veiculos/laser_pl.mp3")
        self.volume_tiro = volume_tiro
        self.separador_dano = 0
        self.velocidade_padrao = 10
        self.velocidade = 10
        self.angulo = 0
        self.pontos = 100
        self.tiros = []
        self.dano = 5
        self.ultimo_disparo = 0 
        self.intervalo_tiro = 1
        self.velocidade_tiro = 10
        self.retomar_velocidade = 0
        self.parou = False


    def processar_movimento(self, keys):
        '''
        Método para processar o movimento e disparo do veículo

        Parâmetros:
        ----------
        keys: ScancoderWrapper
            decta quais teclas foram precionadas
            
        is_v1: Boolean
            Se (is_v1 == True) o presente veículo é o jogador 1 (esquerda)
            Se (is_v1 == False) o presente veículo é o jogador 2 (direita)

        '''
        if self.velocidade == 0 and not self.parou:
            self.retomar_velocidade = pygame.time.get_ticks()
            self.parou = True
        elif self.parou and pygame.time.get_ticks() - self.retomar_velocidade >= 100:
            self.velocidade = self.velocidade_padrao
            self.parou = False
        if self.levou_dano:
            tmp = pygame.time.get_ticks() - self.separador_dano
            if  tmp > 50 and tmp < 100:
                self.imagem = self.imagem_padrao
            elif tmp > self.intervalo_dano:
                self.levou_dano = False
        if not self.ativo:
            return
        (self.x, self.y) = self.rect.topleft
        
        # variação da posição conforme as teclas são apertadas
        dx, dy = 0, 0
        
        if keys[self.teclas['disparo']]:
            self.disparar()
        
        if keys[self.teclas['esquerda']]:
            dx = -self.velocidade
        if keys[self.teclas['direita']]:
            dx = self.velocidade
        if keys[self.teclas['cima']]:
            dy = -self.velocidade
        if keys[self.teclas['baixo']]:
            dy = self.velocidade
        
        self.rotacionar(keys)
        #atualização da posição horizontal
        novo_x = self.rect.x + dx
        if(0 <= novo_x and novo_x <= self.largura_tela - self.tamanho): self.rect.x = novo_x
        # atualização da posição vertical
        novo_y = self.rect.y + dy
        if(50 <= novo_y and novo_y <= self.altura_tela - self.tamanho): self.rect.y = novo_y
        (self.x, self.y) = self.rect.topleft
        # self.rect.topleft = (novo_x, novo_y)

    def rotacionar(self, keys):
        '''
        Método para rotacionar o veículo
        '''
        
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
            centro_x = self.rect.x + self.tamanho / 2
            centro_y = self.rect.y + self.tamanho / 2
            angulo_tiro  = self.angulo
            if self.tiro_inverso:
                angulo_tiro += 180
            self.som_tiro.play()
            self.som_tiro.set_volume(self.volume_tiro)
            novo_tiro = Tiro(centro_x, centro_y, angulo_tiro, self.velocidade_tiro, dano = self.dano, raio = self.tamanho//15)
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
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo) # rotacionando imagem
        novo_retangulo = imagem_rotacionada.get_rect(center=(self.rect.x + self.tamanho / 2, self.rect.y + self.tamanho / 2))
        # Desenha os tiros
        for tiro in self.tiros:
            tiro.draw(surface)
        surface.blit(imagem_rotacionada, novo_retangulo.topleft)

    def levar_dano(self, dano):
        if not(self.levou_dano) and self.ativo:
            imagem_dano = pygame.Surface.convert_alpha(self.imagem)
            imagem_dano.set_alpha(155)
            self.imagem = imagem_dano
            self.integridade = max(self.integridade - dano, 0)
            self.levou_dano = True
            self.separador_dano = pygame.time.get_ticks()

    def atualizar_tiros(self):
        '''
        Método para mover os tiros e retirá-los quando saírem da tela
        '''
        for tiro in self.tiros[:]:
            tiro.mover()
            if tiro.x < 0 or tiro.x > self.largura_tela or tiro.y < 0 or tiro.y > self.altura_tela:
                self.tiros.remove(tiro)

    def mostrar_integridade(self, tela: pygame.SurfaceType, posicao_texto):
        '''
        Método para mostra a integridade na tela

        Parâmetros:
        -----------
        tela: Surface
            Imagem da tela

        posicao_texto: List[float]
            Em que posição o texto será desenhado
        '''
        fonte = pygame.font.Font(None, self.altura_tela//17)
        texto = fonte.render(f"Integridade: {self.integridade:,.2f}", True, (0, 0, 0))
        rect = texto.get_rect()
        sfc = pygame.Surface((rect.width, rect.height))
        sfc.set_alpha(150)
        sfc.fill((255,255,255))
        tela.blit(sfc, posicao_texto)
        tela.blit(texto, posicao_texto)