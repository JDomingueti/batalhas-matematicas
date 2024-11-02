import pygame
import sys


# Tem dois codigos nesse arquivo por enquanto então comente um para rodar o outro

# 1ª código com integridade sendo um valor e utilizando classes

class Veiculo:
    def __init__(self, x, y, cor, largura, altura):
        self.posicao = [x, y]
        self.cor = cor
        self.integridade = 100
        self.tamanho = 50
        self.largura = largura
        self.altura = altura

    def processar_movimento(self, teclas):
        limite_superior = 50  # Espaço do texto

        # Movimentação do Veículo 1 (W, A, S, D)
        if self.cor == (255, 0, 0): 
            if teclas[pygame.K_w] and self.posicao[1] > limite_superior:  # Cima
                self.posicao[1] -= 5
                self.integridade -= 1
            if teclas[pygame.K_s] and self.posicao[1] < self.altura - self.tamanho:  # Baixo
                self.posicao[1] += 5
                self.integridade -= 1
            if teclas[pygame.K_a] and self.posicao[0] > 0:  # Esquerda
                self.posicao[0] -= 5
                self.integridade -= 1
            if teclas[pygame.K_d] and self.posicao[0] < self.largura - self.tamanho:  # Direita
                self.posicao[0] += 5
                self.integridade -= 1

        # Movimentação do Veículo 2 (setas)
        else:
            if teclas[pygame.K_UP] and self.posicao[1] > limite_superior:  
                self.posicao[1] -= 5
                self.integridade -= 1
            if teclas[pygame.K_DOWN] and self.posicao[1] < self.altura - self.tamanho:  
                self.posicao[1] += 5
                self.integridade -= 1
            if teclas[pygame.K_LEFT] and self.posicao[0] > 0:  
                self.posicao[0] -= 5
                self.integridade -= 1
            if teclas[pygame.K_RIGHT] and self.posicao[0] < self.largura - self.tamanho:  
                self.posicao[0] += 5
                self.integridade -= 1

    def draw(self, tela):
        pygame.draw.rect(tela, self.cor, (self.posicao[0], self.posicao[1], self.tamanho, self.tamanho))

    def mostrar_integridade(self, tela, posicao_texto):
        fonte = pygame.font.Font(None, 36)
        texto = fonte.render(f"Integridade: {self.integridade}", True, (0, 0, 0))
        tela.blit(texto, posicao_texto)

class Gerenciador:
    def __init__(self) -> None:
        pygame.init()

        # Dimensões da tela
        self.largura = 800
        self.altura = 600
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Veículos")

        # Objetos
        self.v1 = Veiculo(20, (self.altura - 50) // 2, (255, 0, 0), self.largura, self.altura)  # Vermelho
        self.v2 = Veiculo(self.largura - 70, (self.altura - 50) // 2, (0, 0, 255), self.largura, self.altura)  # Azul

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
        # Atualiza a posição dos veículos
        teclas = pygame.key.get_pressed()
        self.v1.processar_movimento(teclas)
        self.v2.processar_movimento(teclas)

        # Verifica se a integridade de algum veículo chegou a zero
        if self.v1.integridade <= 0 or self.v2.integridade <= 0:
            print("Fim de Jogo!")
            self.is_running = False

    def draw(self):
        self.tela.fill((255, 255, 255))  # Fundo branco
        self.v1.draw(self.tela)
        self.v2.draw(self.tela)
        
        # Exibe a integridade no topo
        self.v1.mostrar_integridade(self.tela, (20, 25))  # v1 no canto superior esquerdo
        self.v2.mostrar_integridade(self.tela, (self.largura - 200, 25))  # v2 no canto superior direito
        
        pygame.display.flip()

if __name__ == '__main__':
    jogo = Gerenciador()
    jogo.run()





# 2ª código usando barras para indicar a integridade e ainda não consegui colocar em classes


import pygame
import sys

pygame.init()

# Dimensões da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Barras")

# Cores
cor_v1 = (255, 0, 0)  # Vermelho
cor_v2 = (0, 0, 255)  # Azul
cor_fundo = (255, 255, 255)  # Branco
cor_fundo_barras = (200, 200, 200)  # Cinza pro fundo das barras

# Tamanhos dos veículos
tamanho_v = 50

# Posições iniciaiss dos veículos
v1 = [20, (altura - tamanho_v) // 2]
v2 = [largura - tamanho_v - 20, (altura - tamanho_v) // 2]

integridade_v1 = 100
integridade_v2 = 100

def mostrar_integridade():
    largura_barra = 100  
    altura_barra = 25  
    pos_y = 30  

    # Fundo cinza das barras
    pygame.draw.rect(tela, cor_fundo_barras, (20, pos_y, largura_barra, altura_barra))
    pygame.draw.rect(tela, cor_fundo_barras, (largura - largura_barra - 20, pos_y, largura_barra, altura_barra))

    # Cor e largura da barra do v1
    largura_atual_v1 = largura_barra * (integridade_v1 / 100)
    if integridade_v1 > 75:
        cor_barra_v1 = (0, 255, 0)  # Verde
    elif integridade_v1 > 50:
        cor_barra_v1 = (255, 255, 0)  # Amarelo
    else:
        cor_barra_v1 = (255, 0, 0)  # Vermelho
    pygame.draw.rect(tela, cor_barra_v1, (20, pos_y, largura_atual_v1, altura_barra))

    # Cor e largura da barra do v2
    largura_atual_v2 = largura_barra * (integridade_v2 / 100)
    if integridade_v2 > 75:
        cor_barra_v2 = (0, 255, 0)  # Verde
    elif integridade_v2 > 50:
        cor_barra_v2 = (255, 255, 0)  # Amarelo
    else:
        cor_barra_v2 = (255, 0, 0)  # Vermelho
    pygame.draw.rect(tela, cor_barra_v2, (largura - largura_atual_v2 - 20, pos_y, largura_atual_v2, altura_barra))

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimentação dos veículos
    teclas = pygame.key.get_pressed()
    movimento_v1 = False
    movimento_v2 = False

    # Limites de movimento (considerando a altura do texto)
    limite_superior = 70  # Espaço para as barras de integridade

    # Veículo 1 (W, A, S, D)
    if teclas[pygame.K_w] and v1[1] > limite_superior:  # Cima
        v1[1] -= 5
        movimento_v1 = True
    if teclas[pygame.K_s] and v1[1] < altura - tamanho_v:  # Baixo
        v1[1] += 5
        movimento_v1 = True
    if teclas[pygame.K_a] and v1[0] > 0:  # Esquerda
        v1[0] -= 5
        movimento_v1 = True
    if teclas[pygame.K_d] and v1[0] < largura - tamanho_v:  # Direita
        v1[0] += 5
        movimento_v1 = True

    # Veículo 2 (setas)
    if teclas[pygame.K_UP] and v2[1] > limite_superior: 
        v2[1] -= 5
        movimento_v2 = True
    if teclas[pygame.K_DOWN] and v2[1] < altura - tamanho_v: 
        v2[1] += 5
        movimento_v2 = True
    if teclas[pygame.K_LEFT] and v2[0] > 0: 
        v2[0] -= 5
        movimento_v2 = True
    if teclas[pygame.K_RIGHT] and v2[0] < largura - tamanho_v: 
        v2[0] += 5
        movimento_v2 = True

    # Reduz a integridade se os veículos se movimentarem
    if movimento_v1:
        integridade_v1 -= 1  
    if movimento_v2:
        integridade_v2 -= 1  

    # Preenche o fundo
    tela.fill((255, 255, 255))  # Fundo branco

    # Desenha os veículos
    pygame.draw.rect(tela, cor_v1, (v1[0], v1[1], tamanho_v, tamanho_v))  
    pygame.draw.rect(tela, cor_v2, (v2[0], v2[1], tamanho_v, tamanho_v)) 

    mostrar_integridade()

    # Verifica se a integridade de algum veículo chegou a zero
    if integridade_v1 <= 0 or integridade_v2 <= 0:
        print("Fim de Jogo!")
        pygame.quit()
        sys.exit()

    # Atualiza a tela
    pygame.display.flip()