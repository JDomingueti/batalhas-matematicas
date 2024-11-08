import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Movimentação do Jogador com Rotação")

class Jogador_1:
    def __init__(self, x, y, largura, altura, sprite):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.sprite = sprite  # A sprite agora é passada como uma superfície (pygame.Surface)
        self.velocidade = 0.5
        self.angulo = 0  # Inicializa o ângulo para 0
    
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
            self.angulo += 0.5  # Rotação horária (diminui o ângulo)
        if keys[pygame.K_PERIOD]:  # Tecla '.' para rotação horária
            self.angulo -= 0.5  # Rotação anti-horária (aumenta o ângulo)
    
    def desenhar(self, surface):
        # Rotaciona a sprite com base no ângulo
        sprite_rotacionada = pygame.transform.rotate(self.sprite, self.angulo)

        # Pega o novo retângulo da superfície rotacionada
        novo_retangulo = sprite_rotacionada.get_rect(center=(self.x + self.largura / 2, self.y + self.altura / 2))
        
        # Desenha a sprite rotacionada
        surface.blit(sprite_rotacionada, novo_retangulo.topleft)

# Carregar a imagem da sprite
sprite_path = "../assets/veiculos/foguete1.png"
sprite_imagem = pygame.image.load(sprite_path)  # Carrega a imagem como uma superfície
sprite_imagem = pygame.transform.scale(sprite_imagem, (50, 50))  # Redimensiona a imagem (caso necessário)

# Inicializar o jogador com a sprite carregada
jogador = Jogador_1(100, 100, 50, 50, sprite_imagem)  # Passa a superfície da sprite carregada

runing = True
while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
    
    jogador.mover()
    jogador.rotacionar()

    screen.fill((0, 0, 0))
    jogador.desenhar(screen)

    pygame.display.flip()

pygame.quit()
