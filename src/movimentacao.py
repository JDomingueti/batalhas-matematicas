import pygame
import math
import time

pygame.init()
largura_tela = 800
altura_tela = 600
screen = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Criando o segundo jogador")

class Tiro:
    def __init__(self, x, y, angulo):
        self.x = x
        self.y = y
        self.velocidade = 1
        self.angulo = angulo
        self.raio = 5
    
    def mover(self):
        self.x += math.cos(math.radians(self.angulo)) * self.velocidade
        self.y -= math.sin(math.radians(self.angulo)) * self.velocidade
        
    def desenhar(self, surface):
        pygame.draw.circle(surface, (255, 255, 0), (int(self.x), int(self.y)), self.raio)


class Jogador:
    def __init__(self, x, y, largura, altura, sprite, teclas, tiro_inverso=False):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.sprite = sprite
        self.velocidade = 0.5
        self.angulo = 0
        self.tiros = []
        self.ultimo_disparo = 0
        self.intervalo_tiro = 0.5
        self.teclas = teclas
        self.tiro_inverso = tiro_inverso
    
    def mover(self):
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
        
        self.x += dx
        self.y += dy

    def rotacionar(self):
        keys = pygame.key.get_pressed()

        if keys[self.teclas['rotacao_anti_horaria']]:
            self.angulo += 0.3
        if keys[self.teclas['rotacao_horaria']]:
            self.angulo -= 0.3

    def disparar(self):
        tempo_atual = time.time()
        if tempo_atual - self.ultimo_disparo >= self.intervalo_tiro:
            centro_x = self.x + self.largura / 2
            centro_y = self.y + self.altura / 2
            angulo_tiro  = self.angulo
            if self.tiro_inverso:
                angulo_tiro += 180
            novo_tiro = Tiro(centro_x, centro_y, angulo_tiro)
            self.tiros.append(novo_tiro)
            self.ultimo_disparo = tempo_atual
    
    def desenhar(self, surface):
        sprite_rotacionada = pygame.transform.rotate(self.sprite, self.angulo)
        novo_retangulo = sprite_rotacionada.get_rect(center=(self.x + self.largura / 2, self.y + self.altura / 2))
        surface.blit(sprite_rotacionada, novo_retangulo.topleft)
        
        for tiro in self.tiros:
            tiro.desenhar(surface)

    def atualizar_tiros(self):
        for tiro in self.tiros[:]:
            tiro.mover()
            if tiro.x < 0 or tiro.x > largura_tela or tiro.y < 0 or tiro.y > altura_tela:
                self.tiros.remove(tiro)


# Carregar a imagem da sprite
sprite_path_1 = "../assets/veiculos/foguete1.png"
sprite_imagem_1 = pygame.image.load(sprite_path_1)
sprite_path_2 = "../assets/veiculos/foguete2.png"
sprite_imagem_2 = pygame.image.load(sprite_path_2)

largura_imagem = 50
altura_imagem = 50
sprite_imagem_1 = pygame.transform.scale(sprite_imagem_1, (largura_imagem, altura_imagem))
sprite_imagem_2 = pygame.transform.scale(sprite_imagem_2, (largura_imagem, altura_imagem))

# Controles para cada jogador
controles_jogador_1 = {
    'esquerda': pygame.K_LEFT,
    'direita': pygame.K_RIGHT,
    'cima': pygame.K_UP,
    'baixo': pygame.K_DOWN,
    'rotacao_anti_horaria': pygame.K_COMMA,
    'rotacao_horaria': pygame.K_PERIOD,
    'disparo': pygame.K_SEMICOLON
}

controles_jogador_2 = {
    'esquerda': pygame.K_a,
    'direita': pygame.K_d,
    'cima': pygame.K_w,
    'baixo': pygame.K_s,
    'rotacao_anti_horaria': pygame.K_c,
    'rotacao_horaria': pygame.K_v,
    'disparo': pygame.K_b
}

# Iniciando os jogadores
jogador_1 = Jogador(100, 100, largura_imagem, altura_imagem, sprite_imagem_1, controles_jogador_1, False)
jogador_2 = Jogador(300, 300, largura_imagem, altura_imagem, sprite_imagem_2, controles_jogador_2, True)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Tecla de disparo de cada jogador
    keys = pygame.key.get_pressed()
    if keys[controles_jogador_1['disparo']]:
        jogador_1.disparar()
    if keys[controles_jogador_2['disparo']]:
        jogador_2.disparar()
    
    jogador_1.mover()
    jogador_1.rotacionar()
    jogador_1.atualizar_tiros()

    jogador_2.mover()
    jogador_2.rotacionar()
    jogador_2.atualizar_tiros()

    screen.fill((0, 0, 0))
    jogador_1.desenhar(screen)
    jogador_2.desenhar(screen)

    pygame.display.flip()

pygame.quit()