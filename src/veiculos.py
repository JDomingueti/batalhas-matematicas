import pygame
import random

class Veiculo:
    def __init__(self, caminho_imagem, x, y, largura, altura, tamanho):
        self.tamanho = tamanho
        self.x = x
        self.y = y
        self.integridade = 100
        self.largura = largura
        self.altura = altura
        self.imagem = None
        self.imagem = pygame.image.load(caminho_imagem)
        self.imagem = pygame.transform.scale(self.imagem, (self.tamanho, self.tamanho))

    def processar_movimento(self, teclas):
        limite_superior = 50  # Espaço do texto

        # Movimentação dos Veículos 
        if self.x < self.largura // 2:  # Para o veículo "v1" (esquerda)
            if teclas[pygame.K_w] and self.y > limite_superior:  # Cima
                self.y -= 5
                self.integridade -= 1
            if teclas[pygame.K_s] and self.y < self.altura - self.tamanho:  # Baixo
                self.y += 5
                self.integridade -= 1
            if teclas[pygame.K_a] and self.x > 0:  # Esquerda
                self.x -= 5
                self.integridade -= 1
            if teclas[pygame.K_d] and self.x < self.largura - self.tamanho:  # Direita
                self.x += 5
                self.integridade -= 1
        else:  # Para o veículo "v2" (direita)
            if teclas[pygame.K_UP] and self.y > limite_superior:  
                self.y -= 5
                self.integridade -= 1
            if teclas[pygame.K_DOWN] and self.y < self.altura - self.tamanho:  
                self.y += 5
                self.integridade -= 1
            if teclas[pygame.K_LEFT] and self.x > 0:  
                self.x -= 5
                self.integridade -= 1
            if teclas[pygame.K_RIGHT] and self.x < self.largura - self.tamanho:  
                self.x += 5
                self.integridade -= 1

    def draw(self, tela):
       tela.blit(self.imagem, (self.x, self.y))

    def mostrar_integridade(self, tela, posicao_texto):
        fonte = pygame.font.Font(None, 36)
        texto = fonte.render(f"Integridade: {self.integridade}", True, (0, 0, 0))
        tela.blit(texto, posicao_texto)

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, caminho_imagem, x, largura, altura, tamanho):
        super().__init__() 
        self.tamanho = tamanho
        self.image = pygame.image.load(caminho_imagem)
        self.image = pygame.transform.scale(self.image, (self.tamanho, self.tamanho))  
        self.rect = self.image.get_rect()  
        self.rect.x = x
        self.rect.y = 0
        self.largura = largura
        self.altura = altura
        self.velocidade_vertical = 2
        self.velocidade_horizontal = 3

    def atualizar(self):
        pass

    def draw(self, tela):
        tela.blit(self.image, (self.rect.x, self.rect.y)) 

class Inimigo1(Inimigo):
    def __init__(self, caminho_imagem, x, largura, altura, tamanho):
        super().__init__(caminho_imagem, x, largura, altura, tamanho)
        self.y_max = random.randint(100, 300)

    def atualizar(self):
        if self.rect.y < self.y_max:
            self.rect.y += self.velocidade_vertical

class Inimigo2(Inimigo):
    def __init__(self, caminho_imagem, x, largura, altura, tamanho):
        super().__init__(caminho_imagem, x, largura, altura, tamanho)
        self.rect.y = random.randint(50, 150)
        self.x_max = random.randint(self.rect.x, self.largura - self.tamanho) 
        self.y_max = random.randint(100, self.altura - self.tamanho)

    def atualizar(self):
        if self.rect.x < self.x_max and self.rect.y < self.y_max:
            self.rect.x += self.velocidade_horizontal  # Direita
            self.rect.y += self.velocidade_vertical  # Baixo

class Inimigo3(Inimigo):
    def __init__(self, caminho_imagem, x, largura, altura, tamanho):
        super().__init__(caminho_imagem, x, largura, altura, tamanho)
        self.rect.y = random.randint(50, 150)
        self.x_max = random.randint(0, self.rect.x - self.tamanho)
        self.y_max = random.randint(self.rect.y, self.altura - self.tamanho)

    def atualizar(self):
        if self.rect.x > self.x_max and self.rect.y < self.y_max:
            self.rect.x -= self.velocidade_horizontal  # Esquerda
            self.rect.y += self.velocidade_vertical  # Baixo

class Inimigo4(Inimigo):
    def __init__(self, caminho_imagem, x, largura, altura, tamanho):
        super().__init__(caminho_imagem, x, largura, altura, tamanho)
        self.velocidade_horizontal = 4
        self.velocidade_vertical = 3
        self.direcao_horizontal = random.choice([-1, 1])  
        self.direcao_vertical = random.choice([-1, 1]) 
        self.momento = pygame.time.get_ticks()  # Guarda o momento em que a direção foi escolhida
        self.tempo_troca_direcao = random.randint(1000, 3000)
        
    def atualizar(self):
        # Verifica se o tempo de troca de direção passou
        if pygame.time.get_ticks() - self.momento > self.tempo_troca_direcao:
            self.momento = pygame.time.get_ticks() 
            self.tempo_troca_direcao = random.randint(1000, 3000) 

            # Escolhe uma nova direção aleatória
            self.direcao_horizontal = random.choice([-1, 1])  # -1 = esquerda, 1 = direita
            self.direcao_vertical = random.choice([-1, 1])    # -1 = cima, 1 = baixo

        # Novas posições
        nova_pos_x = self.rect.x + self.direcao_horizontal * self.velocidade_horizontal
        nova_pos_y = self.rect.y + self.direcao_vertical * self.velocidade_vertical

        # Verificando se a nova posição horizontal está dentro dos limites
        if 0 <= nova_pos_x <= self.largura - self.tamanho:
            self.rect.x = nova_pos_x

        # Verificando se a nova posição vertical está dentro dos limites
        if 0 <= nova_pos_y <= self.altura - self.tamanho:
            self.rect.y = nova_pos_y

        # Verifica se atingiu as bordas horizontais e inverte a direção
        if self.rect.x <= 0 or self.rect.x >= self.largura - self.tamanho:
            self.direcao_horizontal *= -1 

        # Verifica se atingiu as bordas verticais e inverte a direção
        if self.rect.y <= 0 or self.rect.y >= self.altura - self.tamanho:
            self.direcao_vertical *= -1 

class Gerenciador:
    def __init__(self) -> None:
        pygame.init()

        # Dimensões
        self.largura = 800
        self.altura = 600
        self.tamanho = 70
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Batalhas Matemáticas")

        # Caminhos das imagens
        v1_img = "batalhas-matematicas/assets/veiculos/foguete2.png"
        v2_img = "batalhas-matematicas/assets/veiculos/foguete1.png"
        in1_img = "batalhas-matematicas/assets/inimigos/inimigo1_deserto.png"
        in2_img = "batalhas-matematicas/assets/inimigos/inimigo2_deserto.png"
        in3_img = "batalhas-matematicas/assets/inimigos/inimigo3_deserto.png"
        in4_img = "batalhas-matematicas/assets/inimigos/inimigo4_deserto.png"

        # Objetos
        self.v1 = Veiculo(v1_img, 20, (self.altura - self.tamanho) // 2, self.largura, self.altura, self.tamanho)  
        self.v2 = Veiculo(v2_img, self.largura - self.tamanho, (self.altura - self.tamanho) // 2, self.largura, self.altura, self.tamanho)
        self.inimigo1 = Inimigo1(in1_img, self.largura // 2, self.largura, self.altura, self.tamanho)
        self.inimigo2 = Inimigo2(in2_img, self.largura // 2 - 100, self.largura, self.altura, self.tamanho)
        self.inimigo3 = Inimigo3(in3_img, self.largura // 2 + 100, self.largura, self.altura, self.tamanho)
        self.inimigo4 = Inimigo4(in4_img, self.largura // 2, self.largura, self.altura, self.tamanho)

        self.clock = pygame.time.Clock()
        self.is_running = False

    def run(self):
        # Inicializa o jogo
        self.is_running = True
        while self.is_running:
            self.eventos()
            self.atualizar()
            self.draw()
            self.clock.tick(30)
        pygame.quit()

    def eventos(self):
        # Processa eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.is_running = False

    def atualizar(self):
        # Atualiza a posição
        teclas = pygame.key.get_pressed()
        self.v1.processar_movimento(teclas)
        self.v2.processar_movimento(teclas)
        self.inimigo1.atualizar() 
        self.inimigo2.atualizar()
        self.inimigo3.atualizar()
        self.inimigo4.atualizar()

        # Verifica se a integridade de algum veículo chegou a zero
        if self.v1.integridade <= 0 or self.v2.integridade <= 0:
            print("Fim de Jogo!")
            self.is_running = False

    def draw(self):
        self.tela.fill((255, 255, 255))  # Fundo branco
        self.v1.draw(self.tela)
        self.v2.draw(self.tela)
        self.inimigo1.draw(self.tela) 
        self.inimigo2.draw(self.tela)
        self.inimigo3.draw(self.tela)
        self.inimigo4.draw(self.tela)
        
        # Exibe a integridade no topo
        self.v1.mostrar_integridade(self.tela, (20, 25))  # v1 no canto superior esquerdo
        self.v2.mostrar_integridade(self.tela, (self.largura - 200, 25))  # v2 no canto superior direito
        
        pygame.display.flip()

if __name__ == '__main__':
    jogo = Gerenciador()
    jogo.run()