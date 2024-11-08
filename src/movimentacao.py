import pygame
import math
import time

pygame.init()
largura_tela = 800
altura_tela = 600
screen = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Movimentação do Jogador com Rotação")

class Tiro:
    def __init__(self, x, y, angulo):
        self.x = x
        self.y = y
        self.velocidade = 1
        self.angulo = angulo
        self.raio = 5
    
    def mover(self):
        # Calcula o movimento a partir do ângulo fornecido
        self.x += math.cos(math.radians(self.angulo)) * self.velocidade
        self.y -= math.sin(math.radians(self.angulo)) * self.velocidade  # Y diminui para cima na tela
        
    def desenhar(self, surface):
        pygame.draw.circle(surface, (255, 255, 0), (int(self.x), int(self.y)), self.raio)


class Jogador:
    def __init__(self, x, y, largura, altura, sprite):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.sprite = sprite
        self.velocidade = 0.5
        self.angulo = 0
        self.tiros = []
        self.ultimo_disparo = 0  # Armazena o tempo do último disparo
        self.intervalo_tiro = 0.5  # Intervalo entre tiros em segundos
    
    def mover(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        if keys[pygame.K_LEFT]:
            dx = -self.velocidade
        if keys[pygame.K_RIGHT]:
            dx = self.velocidade
        if keys[pygame.K_UP]:
            dy = -self.velocidade
        if keys[pygame.K_DOWN]:
            dy = self.velocidade
        
        self.x += dx
        self.y += dy

    def rotacionar(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_COMMA]:  # Tecla ',' para rotação anti-horária
            self.angulo += 0.3
        if keys[pygame.K_PERIOD]:  # Tecla '.' para rotação horária
            self.angulo -= 0.3

    def disparar(self):
        # Checa se o tempo atual é maior que o tempo do último disparo + intervalo
        tempo_atual = time.time()
        if tempo_atual - self.ultimo_disparo >= self.intervalo_tiro:
            # Calcula o centro do jogador para a origem do tiro
            centro_x = self.x + self.largura / 2
            centro_y = self.y + self.altura / 2
            novo_tiro = Tiro(centro_x, centro_y, self.angulo)
            self.tiros.append(novo_tiro)
            self.ultimo_disparo = tempo_atual  # Atualiza o tempo do último disparo
    
    def desenhar(self, surface):
        # Rotaciona a sprite pelo ângulo fornecido
        sprite_rotacionada = pygame.transform.rotate(self.sprite, self.angulo)
        
        # Pega o novo retângulo na nova rotação
        novo_retangulo = sprite_rotacionada.get_rect(center=(self.x + self.largura / 2, self.y + self.altura / 2))
        
        # Desenha a sprite com a nova rotação
        surface.blit(sprite_rotacionada, novo_retangulo.topleft)
        
        # Desenha os tiros
        for tiro in self.tiros:
            tiro.desenhar(surface)

    def atualizar_tiros(self):
        # Move os tiros e remove os que saíram da tela
        for tiro in self.tiros[:]:
            tiro.mover()
            if tiro.x < 0 or tiro.x > largura_tela or tiro.y < 0 or tiro.y > altura_tela:
                self.tiros.remove(tiro)


# Carregar a imagem da sprite
sprite_path = "../assets/veiculos/foguete1.png"
sprite_imagem_1 = pygame.image.load(sprite_path)  # Carregando a imagem

largura_imagem = 50
altura_imagem = 50
sprite_imagem_1 = pygame.transform.scale(sprite_imagem_1, (largura_imagem, altura_imagem))  # Tamanho da imagem no tamanho do bloco

# Inicia o jogador com a sprite
jogador_1 = Jogador(100, 100, largura_imagem, altura_imagem, sprite_imagem_1)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Checar a tecla de disparo
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SEMICOLON]:
        jogador_1.disparar()
    
    jogador_1.mover()
    jogador_1.rotacionar()
    jogador_1.atualizar_tiros()

    screen.fill((0, 0, 0))
    jogador_1.desenhar(screen)

    pygame.display.flip()

pygame.quit()
