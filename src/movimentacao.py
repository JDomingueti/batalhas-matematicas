import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Movimentação do Jogador")

class Jogador_1:
    def __init__(self, x, y, largura, altura, cor):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor = cor
        self.velocidade = 1
    
    def mover(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidade
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidade
    
    def desenhar(self, surface):
        pygame.draw.rect(surface, self.cor, self.rect)

jogador = Jogador_1(100, 100, 50, 50, (255, 255, 255))

runing = True
while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
        
    jogador.mover()

    screen.fill((0, 0, 0))
    jogador.desenhar(screen)

    pygame.display.flip()

pygame.quit()