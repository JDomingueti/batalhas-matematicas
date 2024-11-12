import pygame
import random
from abc import ABC, abstractmethod
from typing import List

class Veiculo:
    def __init__(self, path_image, x, y, largura, altura, tamanho):
        self.tamanho = tamanho
        self.x = x
        self.y = y
        self.integridade = 100
        self.largura = largura
        self.altura = altura
        self.image = pygame.image.load(path_image)
        self.image = pygame.transform.scale(self.image, (self.tamanho, self.tamanho))

    def processar_movimento(self, teclas, is_v1=True):
        limite_superior = 50  # Espaço do texto
        if is_v1:  # Para o veículo "v1" (esquerda)
            if teclas[pygame.K_w] and self.y > limite_superior:  # Cima
                self.y -= 5
                self.integridade -= 0.1
            if teclas[pygame.K_s] and self.y < self.altura - self.tamanho:  # Baixo
                self.y += 5
                self.integridade -= 0.1
            if teclas[pygame.K_a] and self.x > 0:  # Esquerda
                self.x -= 5
                self.integridade -= 0.1
            if teclas[pygame.K_d] and self.x < self.largura - self.tamanho:  # Direita
                self.x += 5
                self.integridade -= 0.1
        else:  # Para o veículo "v2" (direita)
            if teclas[pygame.K_UP] and self.y > limite_superior:  
                self.y -= 5
                self.integridade -= 0.1
            if teclas[pygame.K_DOWN] and self.y < self.altura - self.tamanho:  
                self.y += 5
                self.integridade -= 0.1
            if teclas[pygame.K_LEFT] and self.x > 0:  
                self.x -= 5
                self.integridade -= 0.1
            if teclas[pygame.K_RIGHT] and self.x < self.largura - self.tamanho:  
                self.x += 5
                self.integridade -= 0.1

        # Limita a posição dos veículos dentro da tela
        self.x = max(0, min(self.largura - self.tamanho, self.x))
        self.y = max(limite_superior, min(self.altura - self.tamanho, self.y))

    def draw(self, tela):
        tela.blit(self.image, (self.x, self.y))

    def mostrar_integridade(self, tela, posicao_texto):
        fonte = pygame.font.Font(None, 36)
        texto = fonte.render(f"Integridade: {self.integridade:,.2f}", True, (0, 0, 0))
        tela.blit(texto, posicao_texto)

class Inimigo(pygame.sprite.Sprite, ABC):
    def __init__(self, path_image, x, largura, altura, tamanho):
        super().__init__() 
        self.tamanho = tamanho
        self.image = pygame.image.load(path_image)
        self.image = pygame.transform.scale(self.image, (self.tamanho, self.tamanho))  
        self.rect = self.image.get_rect()  
        self.rect.x = x
        self.rect.y = 50  # Inimigos começam abaixo da integridade
        self.largura = largura
        self.altura = altura
        self.velocidade_vertical = 2
        self.velocidade_horizontal = 3
        self.limite_superior = 50

    @abstractmethod
    def update(self):
        pass
    
    def draw(self, tela):
        tela.blit(self.image, (self.rect.x, self.rect.y))
        
class Inimigo1(Inimigo):
    def __init__(self, path_image, x, largura, altura, tamanho):
        super().__init__(path_image, x, largura, altura, tamanho)
        self.velocidade_horizontal = 4
        self.velocidade_vertical = 3
        self.direcao_horizontal = random.choice([-1, 1])  
        self.direcao_vertical = random.choice([-1, 1]) 
        self.mudei_direcao_em = pygame.time.get_ticks()  # Guarda o momento em que a direção foi escolhida
        self.tempo_troca_direcao = random.randint(1, 3) * 1000
        
    def update(self):
        # Verifica se o tempo de troca de direção passou
        if pygame.time.get_ticks() - self.mudei_direcao_em > self.tempo_troca_direcao:
            self.mudei_direcao_em = pygame.time.get_ticks() 
            self.tempo_troca_direcao = random.randint(1, 3) * 1000

            # Escolhe uma nova direção aleatória
            self.direcao_horizontal = random.choice([-1, 1])  # -1 = esquerda, 1 = direita
            self.direcao_vertical = random.choice([-1, 1])    # -1 = cima, 1 = baixo

        # Novas posições
        nova_pos_x = self.rect.x + self.direcao_horizontal * self.velocidade_horizontal
        nova_pos_y = self.rect.y + self.direcao_vertical * self.velocidade_vertical

        # Verificando se a nova posição horizontal está dentro dos limites
        if 0 <= nova_pos_x <= self.largura - self.tamanho:
            self.rect.x = nova_pos_x
        else:
            self.direcao_horizontal *= -1 

        # Verificando se a nova posição vertical está dentro dos limites, respeitando o limite superior
        if self.limite_superior <= nova_pos_y <= self.altura - self.tamanho:
            self.rect.y = nova_pos_y
        else:
            self.direcao_vertical *= -1

class Inimigo2(Inimigo):
    def __init__(self, path_image, x, largura, altura, tamanho):
        super().__init__(path_image, x, largura, altura, tamanho)
        self.velocidade_horizontal = 4
        self.velocidade_vertical = 3
        self.direcao_horizontal = random.choice([-1, 1])  
        self.direcao_vertical = random.choice([-1, 1]) 
        self.mudei_direcao_em = pygame.time.get_ticks()  # Guarda o momento em que a direção foi escolhida
        self.tempo_troca_direcao = random.randint(1, 3) * 1000
        
    def update(self):
        # Verifica se o tempo de troca de direção passou
        if pygame.time.get_ticks() - self.mudei_direcao_em > self.tempo_troca_direcao:
            self.mudei_direcao_em = pygame.time.get_ticks() 
            self.tempo_troca_direcao = random.randint(1, 3) * 1000

            # Escolhe uma nova direção aleatória
            self.direcao_horizontal = random.choice([-1, 1])  # -1 = esquerda, 1 = direita
            self.direcao_vertical = random.choice([-1, 1])    # -1 = cima, 1 = baixo

        # Novas posições
        nova_pos_x = self.rect.x + self.direcao_horizontal * self.velocidade_horizontal
        nova_pos_y = self.rect.y + self.direcao_vertical * self.velocidade_vertical

        # Verificando se a nova posição horizontal está dentro dos limites
        if 0 <= nova_pos_x <= self.largura - self.tamanho:
            self.rect.x = nova_pos_x
        else:
            self.direcao_horizontal *= -1 

        # Verificando se a nova posição vertical está dentro dos limites, respeitando o limite superior
        if self.limite_superior <= nova_pos_y <= self.altura - self.tamanho:
            self.rect.y = nova_pos_y
        else:
            self.direcao_vertical *= -1

class Inimigo3(Inimigo):
    def __init__(self, path_image, x, largura, altura, tamanho):
        super().__init__(path_image, x, largura, altura, tamanho)
        self.velocidade_horizontal = 4
        self.velocidade_vertical = 3
        self.direcao_horizontal = random.choice([-1, 1])  
        self.direcao_vertical = random.choice([-1, 1]) 
        self.mudei_direcao_em = pygame.time.get_ticks()  # Guarda o momento em que a direção foi escolhida
        self.tempo_troca_direcao = random.randint(1, 3) * 1000
        
    def update(self):
        # Verifica se o tempo de troca de direção passou
        if pygame.time.get_ticks() - self.mudei_direcao_em > self.tempo_troca_direcao:
            self.mudei_direcao_em = pygame.time.get_ticks() 
            self.tempo_troca_direcao = random.randint(1, 3) * 1000

            # Escolhe uma nova direção aleatória
            self.direcao_horizontal = random.choice([-1, 1])  # -1 = esquerda, 1 = direita
            self.direcao_vertical = random.choice([-1, 1])    # -1 = cima, 1 = baixo

        # Novas posições
        nova_pos_x = self.rect.x + self.direcao_horizontal * self.velocidade_horizontal
        nova_pos_y = self.rect.y + self.direcao_vertical * self.velocidade_vertical

        # Verificando se a nova posição horizontal está dentro dos limites
        if 0 <= nova_pos_x <= self.largura - self.tamanho:
            self.rect.x = nova_pos_x
        else:
            self.direcao_horizontal *= -1 

        # Verificando se a nova posição vertical está dentro dos limites, respeitando o limite superior
        if self.limite_superior <= nova_pos_y <= self.altura - self.tamanho:
            self.rect.y = nova_pos_y
        else:
            self.direcao_vertical *= -1

class Inimigo4(Inimigo):
    def __init__(self, path_image, x, largura, altura, tamanho):
        super().__init__(path_image, x, largura, altura, tamanho)
        self.velocidade_horizontal = 4
        self.velocidade_vertical = 3
        self.direcao_horizontal = random.choice([-1, 1])  
        self.direcao_vertical = random.choice([-1, 1]) 
        self.mudei_direcao_em = pygame.time.get_ticks()  # Guarda o momento em que a direção foi escolhida
        self.tempo_troca_direcao = random.randint(1, 3) * 1000
        
    def update(self):
        # Verifica se o tempo de troca de direção passou
        if pygame.time.get_ticks() - self.mudei_direcao_em > self.tempo_troca_direcao:
            self.mudei_direcao_em = pygame.time.get_ticks() 
            self.tempo_troca_direcao = random.randint(1, 3) * 1000 

            # Escolhe uma nova direção aleatória
            self.direcao_horizontal = random.choice([-1, 1])  # -1 = esquerda, 1 = direita
            self.direcao_vertical = random.choice([-1, 1])    # -1 = cima, 1 = baixo

        # Novas posições
        nova_pos_x = self.rect.x + self.direcao_horizontal * self.velocidade_horizontal
        nova_pos_y = self.rect.y + self.direcao_vertical * self.velocidade_vertical

        # Verificando se a nova posição horizontal está dentro dos limites
        if 0 <= nova_pos_x <= self.largura - self.tamanho:
            self.rect.x = nova_pos_x
        else:
            self.direcao_horizontal *= -1 

        # Verificando se a nova posição vertical está dentro dos limites, respeitando o limite superior
        if self.limite_superior <= nova_pos_y <= self.altura - self.tamanho:
            self.rect.y = nova_pos_y
        else:
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

        # Caminhos das imagens ! o.s.path.join colocar depois
        v1_img = "batalhas-matematicas/assets/veiculos/foguete2.png"
        v2_img = "batalhas-matematicas/assets/veiculos/foguete1.png"
        self.in1_img = "batalhas-matematicas/assets/inimigos/inimigo1_deserto.png"
        self.in2_img = "batalhas-matematicas/assets/inimigos/inimigo2_deserto.png"
        self.in3_img = "batalhas-matematicas/assets/inimigos/inimigo3_deserto.png"
        self.in4_img = "batalhas-matematicas/assets/inimigos/inimigo4_deserto.png"

        self.inimigos : List[Inimigo] = []
        self.max_inimigos = 4
        self.timer_inimigos = pygame.time.get_ticks()

        # veiculos
        self.v1 = Veiculo(v1_img, 20, (self.altura - self.tamanho) // 2, self.largura, self.altura, self.tamanho)  
        self.v2 = Veiculo(v2_img, self.largura - self.tamanho, (self.altura - self.tamanho) // 2, self.largura, self.altura, self.tamanho)
        self.veiculos = [
            self.v1,
            self.v2,
        ]

        self.clock = pygame.time.Clock()
        self.is_running = False

    def criar_inimigos(self, tipo, x, largura, altura, tamanho):
        match tipo: 
            case 1:
                inimigo = Inimigo1(self.in1_img, x, largura, altura, tamanho)
            case 2: 
                inimigo = Inimigo2(self.in2_img, x, largura, altura, tamanho)
            case 3:
                inimigo = Inimigo3(self.in3_img, x, largura, altura, tamanho)
            case 4:
                inimigo = Inimigo4(self.in4_img, x, largura, altura, tamanho)
            case _: 
                return
        self.inimigos.append(inimigo)

    def verificar_colisoes_entre_inimigos(self):
        for i, inimigo1 in enumerate(self.inimigos):
            for inimigo2 in self.inimigos[i + 1:]:
                if inimigo1.rect.colliderect(inimigo2.rect):
                    inimigo1.rect.x -= 5
                    inimigo2.rect.x += 5
                    inimigo1.velocidade_horizontal *= -1
                    inimigo2.velocidade_horizontal *= -1

                    # Limita os inimigos aos limites da tela após a colisão
                    inimigo1.rect.x = max(0, min(self.largura - self.tamanho, inimigo1.rect.x))
                    inimigo1.rect.y = max(0, min(self.altura - self.tamanho, inimigo1.rect.y))
                    inimigo2.rect.x = max(0, min(self.largura - self.tamanho, inimigo2.rect.x))
                    inimigo2.rect.y = max(0, min(self.altura - self.tamanho, inimigo2.rect.y))

    def verificar_colisoes_entre_veiculos_e_inimigos(self):
        for inimigo in self.inimigos:
            for veiculo in self.veiculos:
                veiculo_rect = pygame.Rect(veiculo.x, veiculo.y, veiculo.tamanho, veiculo.tamanho)
                if inimigo.rect.colliderect(veiculo_rect):
                    veiculo.integridade -= 1
                    inimigo.velocidade_horizontal *= -1
                    inimigo.velocidade_vertical *= -1

                    #Ajusta a posição do veículo e limita ele aos limites da tela considerando o espaço do texto
                    if veiculo.x < inimigo.rect.x:
                        veiculo.x = max(0, veiculo.x - 5)
                    elif veiculo.x > inimigo.rect.x:
                        veiculo.x = min(self.largura - veiculo.tamanho, veiculo.x + 5)

                    if veiculo.y < inimigo.rect.y:
                        veiculo.y = max(50, veiculo.y - 5) 
                    elif veiculo.y > inimigo.rect.y:
                        veiculo.y = min(self.altura - veiculo.tamanho, veiculo.y + 5)

                    # Limita o inimigo dentro dos limites da tela após a colisão
                    inimigo.rect.x = max(0, min(self.largura - self.tamanho, inimigo.rect.x))
                    inimigo.rect.y = max(0, min(self.altura - self.tamanho, inimigo.rect.y))

    def verificar_colisoes_entre_veiculoa(self):
        if pygame.Rect(self.v1.x, self.v1.y, self.v1.tamanho, self.v1.tamanho).colliderect(
                pygame.Rect(self.v2.x, self.v2.y, self.v2.tamanho, self.v2.tamanho)):
            self.v1.integridade -= 1 
            self.v2.integridade -= 1

            if self.v1.x < self.v2.x:
                self.v1.x = max(0, self.v1.x - 5)
                self.v2.x = min(self.largura - self.v2.tamanho, self.v2.x + 5)
            else:
                self.v1.x = min(self.largura - self.v1.tamanho, self.v1.x + 5)
                self.v2.x = max(0, self.v2.x - 5)
            if self.v1.y < self.v2.y:
                self.v1.y = max(50, self.v1.y - 5)
                self.v2.y = min(self.altura - self.v2.tamanho, self.v2.y + 5)
            else:
                self.v1.y = min(self.altura - self.v1.tamanho, self.v1.y + 5)
                self.v2.y = max(50, self.v2.y - 5)

    def run(self):
        # Inicializa o jogo e faz aparecer um inimigo por vez
        self.is_running = True
        inimigos = [1, 2, 3, 4]
        while self.is_running:
            if len(self.inimigos) < self.max_inimigos and pygame.time.get_ticks() - self.timer_inimigos > 5000:
                idx = random.choice(inimigos)
                self.criar_inimigos(idx, self.largura // 2, self.largura, self.altura, self.tamanho)
                inimigos.remove(idx)
                self.timer_inimigos = pygame.time.get_ticks()

            self.eventos()
            self.update()
            self.draw()
            self.clock.tick(30)

        pygame.quit()

    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.is_running = False

    def update(self):
        # Atualiza a posição dos veículos e inimigos
        teclas = pygame.key.get_pressed()
        self.v1.processar_movimento(teclas, is_v1=True)
        self.v2.processar_movimento(teclas, is_v1=False)

        for inimigo in self.inimigos:
            inimigo.update()

        self.verificar_colisoes_entre_inimigos()
        self.verificar_colisoes_entre_veiculos_e_inimigos()
        self.verificar_colisoes_entre_veiculoa()

        # # Verifica se a integridade de algum veículo chegou a zero e fecha o programa
        # if self.v1.integridade <= 0 or self.v2.integridade <= 0:
        #     print("Fim de Jogo!")
        #     self.is_running = False

    def draw(self):
        self.tela.fill((255, 255, 255))  # Fundo branco
        self.v1.draw(self.tela)
        self.v2.draw(self.tela)
        for inimigo in self.inimigos:
            inimigo.draw(self.tela)
        
        # Exibe a integridade no topo
        self.v1.mostrar_integridade(self.tela, (20, 25))  # v1 no canto superior esquerdo
        self.v2.mostrar_integridade(self.tela, (self.largura - 200, 25))  # v2 no canto superior direito
        
        pygame.display.flip()

if __name__ == '__main__':
    jogo = Gerenciador()
    jogo.run()