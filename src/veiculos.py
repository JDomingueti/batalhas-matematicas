import pygame
import random

class Veiculo:
    def __init__(self, caminho_imagem, x, y, largura, altura):
        self.x = x
        self.y = y
        self.integridade = 100
        self.largura = largura
        self.altura = altura
        self.imagem = None
        tamanho = 70

        self.imagem = pygame.image.load(caminho_imagem)
        self.imagem = pygame.transform.scale(self.imagem, (tamanho, tamanho))

    def processar_movimento(self, teclas):
        tamanho = 70
        limite_superior = 50  # Espaço do texto

        # Movimentação dos Veículos 
        if self.x < self.largura // 2:  # Para o veículo "v1" (esquerda)
            if teclas[pygame.K_w] and self.y > limite_superior:  # Cima
                self.y -= 5
                self.integridade -= 1
            if teclas[pygame.K_s] and self.y < self.altura - tamanho:  # Baixo
                self.y += 5
                self.integridade -= 1
            if teclas[pygame.K_a] and self.x > 0:  # Esquerda
                self.x -= 5
                self.integridade -= 1
            if teclas[pygame.K_d] and self.x < self.largura - tamanho:  # Direita
                self.x += 5
                self.integridade -= 1
        else:  # Para o veículo "v2" (direita)
            if teclas[pygame.K_UP] and self.y > limite_superior:  
                self.y -= 5
                self.integridade -= 1
            if teclas[pygame.K_DOWN] and self.y < self.altura - tamanho:  
                self.y += 5
                self.integridade -= 1
            if teclas[pygame.K_LEFT] and self.x > 0:  
                self.x -= 5
                self.integridade -= 1
            if teclas[pygame.K_RIGHT] and self.x < self.largura - tamanho:  
                self.x += 5
                self.integridade -= 1

    def draw(self, tela):
       tela.blit(self.imagem, (self.x, self.y))

    def mostrar_integridade(self, tela, posicao_texto):
        fonte = pygame.font.Font(None, 36)
        texto = fonte.render(f"Integridade: {self.integridade}", True, (0, 0, 0))
        tela.blit(texto, posicao_texto)

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, caminho_imagem, x, largura, altura):
        tamanho = 70
        self.image = pygame.image.load(caminho_imagem)
        self.image = pygame.transform.scale(self.image, (tamanho, tamanho))  
        
        self.x = x
        self.y = 0
        self.largura = largura
        self.altura = altura
        self.velocidade_vertical = 2
        self.velocidade_horizontal = 3

    def atualizar(self):
        pass

    def draw(self, tela):
        tela.blit(self.image, (self.x, self.y)) 

class Inimigo1(Inimigo):
    def __init__(self, caminho_imagem, x, largura, altura):
       super().__init__(caminho_imagem, x, largura, altura)
       self.y_max = random.randint(100, 300)

    def atualizar(self):
        # inimigo descendo
        if self.y < self.y_max:
            self.y += self.velocidade_vertical

class Inimigo2(Inimigo):
    def __init__(self, caminho_imagem, x, largura, altura):
        super().__init__(caminho_imagem, x, largura, altura)
        self.x = 0
        self.y = random.randint(50, 150)
        self.x_max = random.randint(self.x, self.largura - 70) 
        self.y_max = random.randint(100, self.altura - 70)

    def atualizar(self):
        if self.x < self.x_max and self.y < self.y_max:
            self.x += self.velocidade_horizontal  # direita
            self.y += self.velocidade_vertical  # baixo

        if self.x >= self.x_max and self.y >= self.y_max:
            pass 

class Inimigo3(Inimigo):
    def __init__(self, caminho_imagem, x, largura, altura):
        super().__init__(caminho_imagem, x, largura, altura)
        self.y = random.randint(50, 150)  
        self.x_max = random.randint(0, self.x - 70)  
        self.y_max = random.randint(self.y, self.altura - 70)  

    def atualizar(self):
        if self.x > self.x_max and self.y < self.y_max:
            self.x -= self.velocidade_horizontal  # esquerda
            self.y += self.velocidade_vertical  # baixo

        if self.x <= self.x_max and self.y >= self.y_max:
            pass  

class Gerenciador:
    def __init__(self) -> None:
        pygame.init()

        # Dimensões
        self.largura = 800
        self.altura = 600
        tamanho = 70
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Batalhas Matemáticas")

        # Caminhos das imagens
        v1_img = "batalhas-matematicas/assets/veiculos/foguete2.png"
        v2_img = "batalhas-matematicas/assets/veiculos/foguete1.png"
        in1_img = "batalhas-matematicas/assets/inimigos/inimigo1_deserto.png"
        in2_img = "batalhas-matematicas/assets/inimigos/inimigo2_deserto.png"
        in3_img = "batalhas-matematicas/assets/inimigos/inimigo3_deserto.png"

        # Objetos
        self.v1 = Veiculo(v1_img, 20, (self.altura - tamanho) // 2, self.largura, self.altura)  
        self.v2 = Veiculo(v2_img, self.largura - 70, (self.altura - tamanho) // 2, self.largura, self.altura)
        self.inimigo1 = Inimigo1(in1_img, self.largura // 2, self.largura, self.altura)
        self.inimigo2 = Inimigo2(in2_img, self.largura // 2 - 100, self.largura, self.altura)
        self.inimigo3 = Inimigo3(in3_img, self.largura // 2 + 100, self.largura, self.altura)

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
        
        # Exibe a integridade no topo
        self.v1.mostrar_integridade(self.tela, (20, 25))  # v1 no canto superior esquerdo
        self.v2.mostrar_integridade(self.tela, (self.largura - 200, 25))  # v2 no canto superior direito
        
        pygame.display.flip()

if __name__ == '__main__':
    jogo = Gerenciador()
    jogo.run()