import pygame
import random
from abc import ABC, abstractmethod
from typing import List
import math

class Veiculo:
    def __init__(self, path_image, x, y, largura_tela, altura_tela, tamanho_veiculo):
        self.tamanho_veiculo = tamanho_veiculo
        self.x = x
        self.y = y
        self.integridade = 100
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.angulo = 0
        self.tiros = []
        self.ultimo_disparo = 0  # Armazena o tempo do último disparo
        self.intervalo_tiro = 2  # Intervalo entre tiros em segundos
        self.image = pygame.image.load(path_image)
        self.image = pygame.transform.scale(self.image, (self.tamanho_veiculo, self.tamanho_veiculo))

    def processar_movimento(self, keys, is_v1=True):
        limite_superior = 50  # Espaço do texto
        if is_v1:  # Para o veículo "v1" (esquerda)
            if keys[pygame.K_w] and self.y > limite_superior:  # Cima
                self.y -= 5
                self.integridade -= 0.1
            if keys[pygame.K_s] and self.y < self.altura_tela - self.tamanho_veiculo:  # Baixo
                self.y += 5
                self.integridade -= 0.1
            if keys[pygame.K_a] and self.x > 0:  # Esquerda
                self.x -= 5
                self.integridade -= 0.1
            if keys[pygame.K_d] and self.x < self.largura_tela - self.tamanho_veiculo:  # Direita
                self.x += 5
                self.integridade -= 0.1
                
        else:  # Para o veículo "v2" (direita)
            if keys[pygame.K_UP] and self.y > limite_superior:  
                self.y -= 5
                self.integridade -= 0.1
            if keys[pygame.K_DOWN] and self.y < self.altura_tela:  
                self.y += 5
                self.integridade -= 0.1
            if keys[pygame.K_LEFT] and self.x > 0:  
                self.x -= 5
                self.integridade -= 0.1
            if keys[pygame.K_RIGHT] and self.x < self.largura_tela - self.tamanho_veiculo:  
                self.x += 5
                self.integridade -= 0.1

        # Limita a posição dos veículos dentro da tela
        self.x = max(0, min(self.largura_tela, self.x))
        self.y = max(limite_superior, min(self.altura_tela - self.tamanho_veiculo, self.y))

    def rotacionar(self, keys, is_v1=True):
        keys = pygame.key.get_pressed()
        if is_v1:  # Para o veículo "v1" (esquerda)
            if keys[pygame.K_COMMA]:  # Tecla ',' para rotação anti-horária
                self.angulo += 0.5
            if keys[pygame.K_PERIOD]:  # Tecla '.' para rotação horária
                self.angulo -= 0.5
        else:  # Para o veículo "v2" (direita)
            if keys[pygame.K_x]:  # Tecla 'x' para rotação anti-horária
                self.angulo += 0.5
            if keys[pygame.K_z]:  # Tecla 'z' para rotação horária
                self.angulo -= 0.5

    def disparar(self, is_v1=True):
        # Checa se o tempo atual é maior que o tempo do último disparo + intervalo
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.ultimo_disparo >= self.intervalo_tiro:
            # Calcula o centro do jogador para a origem do tiro
            centro_x = self.x
            centro_y = self.y
            novo_tiro = Tiro(centro_x, centro_y, self.angulo)
            self.tiros.append(novo_tiro)
            self.ultimo_disparo = tempo_atual  # Atualiza o tempo do último disparo

    def draw(self, surface):
        # Rotaciona a sprite pelo ângulo fornecido
        image_rotacionada = pygame.transform.rotate(self.image, self.angulo)
        
        # Pega o novo retângulo na nova rotação
        novo_retangulo = image_rotacionada.get_rect(topleft=(self.x, self.y))
        
        # Desenha a sprite com a nova rotação
        surface.blit(image_rotacionada, novo_retangulo)
        
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

class Tiro:
    def __init__(self, x, y, angulo):
        self.x = x
        self.y = y
        self.velocidade = 3
        self.angulo = angulo
        self.raio = 5
    
    def mover(self):
        # Calcula o movimento a partir do ângulo fornecido
        self.x += math.cos(math.radians(self.angulo)) * self.velocidade
        self.y -= math.sin(math.radians(self.angulo)) * self.velocidade  # Y diminui para cima na tela
        
    def draw(self, tela):
        pygame.draw.circle(tela, (255, 255, 0), (int(self.x), int(self.y)), self.raio)

class Inimigo(pygame.sprite.Sprite, ABC):
    def __init__(self, path_image, x, largura_tela, altura_tela, tamanho_veiculo):
        super().__init__() 
        self.tamanho_veiculo = tamanho_veiculo
        self.image = pygame.image.load(path_image)
        self.image = pygame.transform.scale(self.image, (self.tamanho_veiculo, self.tamanho_veiculo))  
        self.rect = self.image.get_rect()  
        self.rect.x = x
        self.rect.y = 50  # Inimigos começam abaixo da integridade
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.velocidade_vertical = 2
        self.velocidade_horizontal = 3
        self.limite_superior = 50
        self.ultimo_tempo_colisao = pygame.time.get_ticks()

    @abstractmethod
    def update(self):
        pass
    
    def draw(self, tela):
        tela.blit(self.image, (self.rect.x, self.rect.y))
        
class Inimigo1(Inimigo):
    def __init__(self, path_image, x, largura_tela, altura_tela, tamanho_veiculo):
        super().__init__(path_image, x, largura_tela, altura_tela, tamanho_veiculo)
        
        self.velocidade_horizontal = 2
        self.velocidade_vertical = 3
        self.direcao_horizontal = random.choice([-1, 1])  
        self.direcao_vertical = random.choice([-1, 1]) 
        
        self.mudei_direcao_em = pygame.time.get_ticks()
        self.tempo_troca_direcao = random.randint(2, 5) * 1000

    def update(self):
        # Verifica se o tempo para troca de direção já passou
        if pygame.time.get_ticks() - self.mudei_direcao_em > self.tempo_troca_direcao:
            self.mudei_direcao_em = pygame.time.get_ticks()
            self.tempo_troca_direcao = random.randint(2, 5) * 1000

            # Escolhe novas direções aleatórias
            self.direcao_horizontal = random.choice([-1, 1])
            self.direcao_vertical = random.choice([-1, 1])

        # Calcula as novas posições
        nova_pos_x = self.rect.x + self.direcao_horizontal * self.velocidade_horizontal
        nova_pos_y = self.rect.y + self.direcao_vertical * self.velocidade_vertical

        # Verifica se a nova posição está dentro dos limites da tela
        if 0 <= nova_pos_x <= self.largura_tela - self.tamanho_veiculo:
            self.rect.x = nova_pos_x
        else:
            self.direcao_horizontal *= -1 
        if self.limite_superior <= nova_pos_y <= self.altura_tela - self.tamanho_veiculo:
            self.rect.y = nova_pos_y
        else:
            # Se atingir o topo ou o fundo da tela, inverte a direção vertical, mas o inimigo não vai para baixo
            if nova_pos_y < self.limite_superior:  # Atingiu o topo
                self.direcao_vertical = 1  # Vai para baixo
            elif nova_pos_y > self.altura_tela - self.tamanho_veiculo:  # Atingiu o fundo
                self.direcao_vertical = -1  # Vai para cima
            else:
                self.direcao_vertical *= -1 

class Inimigo2(Inimigo):
    def __init__(self, path_image, x, largura_tela, altura_tela, tamanho_veiculo):
        super().__init__(path_image, x, largura_tela, altura_tela, tamanho_veiculo)
        
        self.velocidade_horizontal = 2
        self.velocidade_vertical = 3
        self.direcao_horizontal = random.choice([-1, 1])  
        self.direcao_vertical = random.choice([-1, 1]) 
        
        self.mudei_direcao_em = pygame.time.get_ticks()
        self.tempo_troca_direcao = random.randint(2, 5) * 1000

    def update(self):
        # Verifica se o tempo para troca de direção já passou
        if pygame.time.get_ticks() - self.mudei_direcao_em > self.tempo_troca_direcao:
            self.mudei_direcao_em = pygame.time.get_ticks()
            self.tempo_troca_direcao = random.randint(2, 5) * 1000

            # Escolhe novas direções aleatórias
            self.direcao_horizontal = random.choice([-1, 1])
            self.direcao_vertical = random.choice([-1, 1])

        # Calcula as novas posições
        nova_pos_x = self.rect.x + self.direcao_horizontal * self.velocidade_horizontal
        nova_pos_y = self.rect.y + self.direcao_vertical * self.velocidade_vertical

        # Verifica se a nova posição está dentro dos limites da tela
        if 0 <= nova_pos_x <= self.largura_tela - self.tamanho_veiculo:
            self.rect.x = nova_pos_x
        else:
            self.direcao_horizontal *= -1 
        if self.limite_superior <= nova_pos_y <= self.altura_tela - self.tamanho_veiculo:
            self.rect.y = nova_pos_y
        else:
            # Se atingir o topo ou o fundo da tela, inverte a direção vertical, mas o inimigo não vai para baixo
            if nova_pos_y < self.limite_superior:  # Atingiu o topo
                self.direcao_vertical = 1  # Vai para baixo
            elif nova_pos_y > self.altura_tela - self.tamanho_veiculo:  # Atingiu o fundo
                self.direcao_vertical = -1  # Vai para cima
            else:
                self.direcao_vertical *= -1 

class Inimigo3(Inimigo):
    def __init__(self, path_image, x, largura_tela, altura_tela, tamanho_veiculo):
        super().__init__(path_image, x, largura_tela, altura_tela, tamanho_veiculo)
        
        self.velocidade_horizontal = 2
        self.velocidade_vertical = 3
        self.direcao_horizontal = random.choice([-1, 1])  
        self.direcao_vertical = random.choice([-1, 1]) 
        
        self.mudei_direcao_em = pygame.time.get_ticks()
        self.tempo_troca_direcao = random.randint(2, 5) * 1000

    def update(self):
        # Verifica se o tempo para troca de direção já passou
        if pygame.time.get_ticks() - self.mudei_direcao_em > self.tempo_troca_direcao:
            self.mudei_direcao_em = pygame.time.get_ticks()
            self.tempo_troca_direcao = random.randint(2, 5) * 1000

            # Escolhe novas direções aleatórias
            self.direcao_horizontal = random.choice([-1, 1])
            self.direcao_vertical = random.choice([-1, 1])

        # Calcula as novas posições
        nova_pos_x = self.rect.x + self.direcao_horizontal * self.velocidade_horizontal
        nova_pos_y = self.rect.y + self.direcao_vertical * self.velocidade_vertical

        # Verifica se a nova posição está dentro dos limites da tela
        if 0 <= nova_pos_x <= self.largura_tela - self.tamanho_veiculo:
            self.rect.x = nova_pos_x
        else:
            self.direcao_horizontal *= -1 
        if self.limite_superior <= nova_pos_y <= self.altura_tela - self.tamanho_veiculo:
            self.rect.y = nova_pos_y
        else:
            # Se atingir o topo ou o fundo da tela, inverte a direção vertical, mas o inimigo não vai para baixo
            if nova_pos_y < self.limite_superior:  # Atingiu o topo
                self.direcao_vertical = 1  # Vai para baixo
            elif nova_pos_y > self.altura_tela - self.tamanho_veiculo:  # Atingiu o fundo
                self.direcao_vertical = -1  # Vai para cima
            else:
                self.direcao_vertical *= -1 

class Inimigo4(Inimigo):
    def __init__(self, path_image, x, largura_tela, altura_tela, tamanho_veiculo):
        super().__init__(path_image, x, largura_tela, altura_tela, tamanho_veiculo)
        
        self.velocidade_horizontal = 2
        self.velocidade_vertical = 3
        self.direcao_horizontal = random.choice([-1, 1])  
        self.direcao_vertical = random.choice([-1, 1]) 
        
        self.mudei_direcao_em = pygame.time.get_ticks()
        self.tempo_troca_direcao = random.randint(2, 5) * 1000

    def update(self):
        # Verifica se o tempo para troca de direção já passou
        if pygame.time.get_ticks() - self.mudei_direcao_em > self.tempo_troca_direcao:
            self.mudei_direcao_em = pygame.time.get_ticks()
            self.tempo_troca_direcao = random.randint(2, 5) * 1000

            # Escolhe novas direções aleatórias
            self.direcao_horizontal = random.choice([-1, 1])
            self.direcao_vertical = random.choice([-1, 1])

        # Calcula as novas posições
        nova_pos_x = self.rect.x + self.direcao_horizontal * self.velocidade_horizontal
        nova_pos_y = self.rect.y + self.direcao_vertical * self.velocidade_vertical

        # Verifica se a nova posição está dentro dos limites da tela
        if 0 <= nova_pos_x <= self.largura_tela - self.tamanho_veiculo:
            self.rect.x = nova_pos_x
        else:
            self.direcao_horizontal *= -1 
        if self.limite_superior <= nova_pos_y <= self.altura_tela - self.tamanho_veiculo:
            self.rect.y = nova_pos_y
        else:
            # Se atingir o topo ou o fundo da tela, inverte a direção vertical, mas o inimigo não vai para baixo
            if nova_pos_y < self.limite_superior:  # Atingiu o topo
                self.direcao_vertical = 1  # Vai para baixo
            elif nova_pos_y > self.altura_tela - self.tamanho_veiculo:  # Atingiu o fundo
                self.direcao_vertical = -1  # Vai para cima
            else:
                self.direcao_vertical *= -1 

class Gerenciador:
    def __init__(self) -> None:
        pygame.init()

        # Dimensões
        self.largura_tela = 800
        self.altura_tela = 600
        self.tamanho_veiculo = 70
        self.limite_superior = 50
        self.tela = pygame.display.set_mode((self.largura_tela, self.altura_tela))
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
        self.v1 = Veiculo(v1_img, 20, (self.altura_tela - self.tamanho_veiculo) // 2, self.largura_tela, self.altura_tela, self.tamanho_veiculo)  
        self.v2 = Veiculo(v2_img, self.largura_tela - self.tamanho_veiculo - 20, (self.altura_tela - self.tamanho_veiculo) // 2, self.largura_tela, self.altura_tela, self.tamanho_veiculo)
        self.veiculos = [
            self.v1,
            self.v2,
        ]

        self.clock = pygame.time.Clock()
        self.is_running = False

    def criar_inimigos(self, tipo, x, largura_tela, altura_tela, tamanho_veiculo):
        match tipo: 
            case 1:
                inimigo = Inimigo1(self.in1_img, x, largura_tela, altura_tela, tamanho_veiculo)
            case 2: 
                inimigo = Inimigo2(self.in2_img, x, largura_tela, altura_tela, tamanho_veiculo)
            case 3:
                inimigo = Inimigo3(self.in3_img, x, largura_tela, altura_tela, tamanho_veiculo)
            case 4:
                inimigo = Inimigo4(self.in4_img, x, largura_tela, altura_tela, tamanho_veiculo)
            case _: 
                return
        self.inimigos.append(inimigo)

    def verificar_colisoes_entre_inimigos(self):
        for i, inimigo1 in enumerate(self.inimigos):
            for inimigo2 in self.inimigos[i + 1:]:
                if inimigo1.rect.colliderect(inimigo2.rect):
                    # Movimenta inimigos para longe um do outro
                    inimigo1.rect.x -= 5
                    inimigo1.rect.y -= 2  
                    inimigo2.rect.x += 5
                    inimigo2.rect.y += 2
                    
                    inimigo1.velocidade_horizontal *= -1
                    inimigo2.velocidade_horizontal *= -1

                    # Limita os inimigos aos limites da tela
                    inimigo1.rect.x = max(0, min(self.largura_tela - self.tamanho_veiculo, inimigo1.rect.x))
                    inimigo1.rect.y = max(0, min(self.altura_tela - self.tamanho_veiculo, inimigo1.rect.y))
                    inimigo2.rect.x = max(0, min(self.largura_tela - self.tamanho_veiculo, inimigo2.rect.x))
                    inimigo2.rect.y = max(0, min(self.altura_tela - self.tamanho_veiculo, inimigo2.rect.y))

    def verificar_colisoes_entre_veiculos_e_inimigos(self):
        tempo_atual = pygame.time.get_ticks()
        for inimigo in self.inimigos:
            for veiculo in self.veiculos:
                veiculo_rect = pygame.Rect(veiculo.x, veiculo.y, veiculo.tamanho_veiculo, veiculo.tamanho_veiculo)
                if inimigo.rect.colliderect(veiculo_rect):
                    if tempo_atual - inimigo.ultimo_tempo_colisao > 10:
                        veiculo.integridade -= 1
                        inimigo.ultimo_tempo_colisao = tempo_atual  # Atualiza o tempo da última colisão

                        # Ajusta a posição do inimigo para longe do veiculo
                        if inimigo.rect.x < veiculo.x:
                            inimigo.rect.x -= 10  # Move para a esquerda
                            veiculo.x = min(self.largura_tela - veiculo.tamanho_veiculo, veiculo.x + 5)
                        elif inimigo.rect.x > veiculo.x:
                            inimigo.rect.x += 10  # Move para a direita
                            veiculo.x = max(0, veiculo.x - 5)

                        if inimigo.rect.y < veiculo.y:
                            inimigo.rect.y -= 10  # Move para cima
                            veiculo.y = min(self.altura_tela - veiculo.tamanho_veiculo, veiculo.y + 5)
                        elif inimigo.rect.y > veiculo.y:
                            inimigo.rect.y += 10  # Move para baixo
                            veiculo.y = max(90, veiculo.y - 5)

                        # Inverte a direção
                        inimigo.velocidade_horizontal *= -1
                        inimigo.velocidade_vertical *= -1

                        # Limita o inimigo aos limites da tela
                        inimigo.rect.x = max(0, min(self.largura_tela - inimigo.tamanho_veiculo, inimigo.rect.x))
                        inimigo.rect.y = max(self.limite_superior, min(self.altura_tela - inimigo.tamanho_veiculo, inimigo.rect.y))
                        veiculo.x = max(0, min(self.largura_tela - veiculo.tamanho_veiculo, veiculo.x))
                        veiculo.y = max(self.limite_superior, min(self.altura_tela - veiculo.tamanho_veiculo, veiculo.y))

    def verificar_colisoes_entre_veiculoS(self):
        if pygame.Rect(self.v1.x, self.v1.y, self.v1.tamanho_veiculo, self.v1.tamanho_veiculo).colliderect(
                pygame.Rect(self.v2.x, self.v2.y, self.v2.tamanho_veiculo, self.v2.tamanho_veiculo)):
            self.v1.integridade -= 1 
            self.v2.integridade -= 1

            if self.v1.x < self.v2.x:
                self.v1.x = max(0, self.v1.x - 5)
                self.v2.x = min(self.largura_tela - self.v2.tamanho_veiculo, self.v2.x + 5)
            else:
                self.v1.x = min(self.largura_tela - self.v1.tamanho_veiculo, self.v1.x + 5)
                self.v2.x = max(0, self.v2.x - 5)
            if self.v1.y < self.v2.y:
                self.v1.y = max(90, self.v1.y - 5)
                self.v2.y = min(self.altura_tela - self.v2.tamanho_veiculo, self.v2.y + 5)
            else:
                self.v1.y = min(self.altura_tela - self.v1.tamanho_veiculo, self.v1.y + 5)
                self.v2.y = max(90, self.v2.y - 5)

    def run(self):

        # Inicializa o jogo e faz aprecer um inimigo por vez
        self.is_running = True
        inimigos = [1, 2, 3, 4]
        while self.is_running:
            if len(self.inimigos) < self.max_inimigos and pygame.time.get_ticks() - self.timer_inimigos > 5000:
                idx = random.choice(inimigos)
                self.criar_inimigos(idx, self.largura_tela // 2, self.largura_tela, self.altura_tela, self.tamanho_veiculo)
                inimigos.remove(idx)
                self.timer_inimigos = pygame.time.get_ticks()

            # Checar a tecla de disparo
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SEMICOLON]:
                self.v1.disparar()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_z]:
                self.v2.disparar()

            self.v1.rotacionar(pygame.K_COMMA, pygame.K_PERIOD) 
            self.v1.atualizar_tiros()
            self.v2.rotacionar(pygame.K_x, pygame.K_z)
            self.v2.atualizar_tiros()

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
        keys = pygame.key.get_pressed()
        self.v1.processar_movimento(keys, is_v1=True)
        self.v2.processar_movimento(keys, is_v1=False)

        for inimigo in self.inimigos:
            inimigo.update()

        self.verificar_colisoes_entre_inimigos()
        self.verificar_colisoes_entre_veiculos_e_inimigos()
        self.verificar_colisoes_entre_veiculoS()

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
        self.v2.mostrar_integridade(self.tela, (self.largura_tela - 250, 25))  # v2 no canto superior direito
        
        pygame.display.flip()

if __name__ == '__main__':
    jogo = Gerenciador()
    jogo.run()