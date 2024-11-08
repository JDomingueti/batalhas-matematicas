import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Movimentação do Jogador com Rotação")

class Jogador:
    def __init__(self, x, y, largura, altura, sprite):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.sprite = sprite
        self.velocidade = 0.2
        self.angulo = 0
    
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

        if keys[pygame.K_COMMA]:  # Tecla ',' para rotação horária
            self.angulo += 0.2
        if keys[pygame.K_PERIOD]:  # Tecla '.' para rotação anti-horária
            self.angulo -= 0.2
    
    def desenhar(self, surface):
        # Rotaciona a sprite pelo ângulo fornecido
        sprite_rotacionada = pygame.transform.rotate(self.sprite, self.angulo)

        # Pega o novo retângulo na nova rotação
        novo_retangulo = sprite_rotacionada.get_rect(center=(self.x + self.largura / 2, self.y + self.altura / 2))
        
        # Desenha a sprite com a nova rotação
        surface.blit(sprite_rotacionada, novo_retangulo.topleft)

# Carregar a imagem da sprite
sprite_path = "../assets/veiculos/foguete1.png"
sprite_imagem_1 = pygame.image.load(sprite_path)  # Carregando a imagem
sprite_imagem_1 = pygame.transform.scale(sprite_imagem_1, (50, 50))  # Tamanho da imagem no tamanho do bloco

# Inicia o jogador com a sprite
jogador_1 = Jogador(100, 100, 50, 50, sprite_imagem_1)

runing = True
while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
    
    jogador_1.mover()
    jogador_1.rotacionar()

    screen.fill((0, 0, 0))
    jogador_1.desenhar(screen)

    pygame.display.flip()

pygame.quit()
