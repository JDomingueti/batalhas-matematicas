import pygame
import time
from tiro import Tiro

class Veiculo:
    def __init__(self, caminho_imagem, x, y, largura_tela, altura_tela, tamanho_veiculo, teclas, tiro_inverso=False):
        self.caminho_imagem = caminho_imagem
        self.tamanho_veiculo = tamanho_veiculo
        self.x = x
        self.y = y
        self.integridade = 100
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.velocidade = 10
        self.angulo = 0
        self.tiros = []
        self.dano = 1
        self.ultimo_disparo = 0 
        self.intervalo_tiro = 1
        self.velocidade_tiro = 10
        self.teclas = teclas
        self.tiro_inverso = tiro_inverso

    def processar_movimento(self, keys, is_v1=True):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        if keys[self.teclas['esquerda']]:
            dx = -self.velocidade
        if keys[self.teclas['direita']]:
            dx = self.velocidade
        if keys[self.teclas['cima']]:
            dy = -self.velocidade
        if keys[self.teclas['baixo']]:
            dy = self.velocidade
        
        novo_x = self.x + dx
        if(0 <= novo_x and novo_x <= self.largura_tela - self.tamanho_veiculo): self.x = novo_x

        novo_y = self.y + dy
        if(50 <= novo_y and novo_y <= self.altura_tela - self.tamanho_veiculo): self.y = novo_y

    def rotacionar(self):
        keys = pygame.key.get_pressed()

        if keys[self.teclas['rotacao_anti_horaria']]:
            self.angulo += 3
        if keys[self.teclas['rotacao_horaria']]:
            self.angulo -= 3
                
    def disparar(self, is_v1=True):
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
        # Desenhar o jogador
        imagem = pygame.image.load(self.caminho_imagem)
        imagem = pygame.transform.scale(imagem, (self.tamanho_veiculo, self.tamanho_veiculo))
        imagem_rotacionada = pygame.transform.rotate(imagem, self.angulo)
        novo_retangulo = imagem_rotacionada.get_rect(center=(self.x + self.tamanho_veiculo / 2, self.y + self.tamanho_veiculo / 2))
        surface.blit(imagem_rotacionada, novo_retangulo.topleft)
        
        # Desenha os tiros
        for tiro in self.tiros:
            tiro.draw(surface)

    def atualizar_tiros(self):
        # Move os tiros e remove os que saíram da tela
        for tiro in self.tiros[:]:
            tiro.mover()
            if tiro.x < 0 or tiro.x > self.largura_tela or tiro.y < 0 or tiro.y > self.altura_tela:
                self.tiros.remove(tiro)

    def mostrar_integridade(self, tela, posicao_texto):
        fonte = pygame.font.Font(None, 36)
        texto = fonte.render(f"Integridade: {self.integridade:,.2f}", True, (0, 0, 0))
        tela.blit(texto, posicao_texto)