import pygame
import random
from typing import List
from veiculos import Veiculo
from inimigos import *

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
        v1_img = "batalhas-matematicas/assets/veiculos/foguete1.png"
        v2_img = "batalhas-matematicas/assets/veiculos/foguete2.png"
        self.in1_img = "batalhas-matematicas/assets/inimigos/inimigo1_deserto.png"
        self.in2_img = "batalhas-matematicas/assets/inimigos/inimigo2_deserto.png"
        self.in3_img = "batalhas-matematicas/assets/inimigos/inimigo3_deserto.png"
        self.in4_img = "batalhas-matematicas/assets/inimigos/inimigo4_deserto.png"
        
        # Caminhos das imagens dos powerups
        self.powerup1_img = "batalhas-matematicas/assets/poderes/vida.png"
        self.powerup2_img = "batalhas-matematicas/assets/poderes/velocidade.png"
        self.powerup3_img = "batalhas-matematicas/assets/poderes/bala.png"
        self.powerup4_img = "batalhas-matematicas/assets/poderes/dano.png"

        self.inimigos : List[Inimigo] = []
        self.max_inimigos = 4
        self.timer_inimigos = pygame.time.get_ticks()
        self.powerups = []

        # veiculos
        # Controles para cada jogador
        controles_v1 = {
            'esquerda': pygame.K_a,
            'direita': pygame.K_d,
            'cima': pygame.K_w,
            'baixo': pygame.K_s,
            'rotacao_anti_horaria': pygame.K_c,
            'rotacao_horaria': pygame.K_v,
            'disparo': pygame.K_b
        }

        controles_v2 = {
            'esquerda': pygame.K_LEFT,
            'direita': pygame.K_RIGHT,
            'cima': pygame.K_UP,
            'baixo': pygame.K_DOWN,
            'rotacao_anti_horaria': pygame.K_COMMA,
            'rotacao_horaria': pygame.K_PERIOD,
            'disparo': pygame.K_SEMICOLON
        }
        
        self.v1 = Veiculo(v1_img, 20, (self.altura_tela - self.tamanho_veiculo) // 2, self.largura_tela, self.altura_tela, self.tamanho_veiculo, controles_v1)  
        self.v2 = Veiculo(v2_img, self.largura_tela - self.tamanho_veiculo - 20, (self.altura_tela - self.tamanho_veiculo) // 2, self.largura_tela, self.altura_tela, self.tamanho_veiculo, controles_v2, True)
        self.veiculos = [
            self.v1,
            self.v2,
        ]

        self.clock = pygame.time.Clock()
        self.is_running = False

    def criar_inimigos(self, tipo, x, largura_tela, altura_tela, tamanho_veiculo):
        match tipo: 
            case 1:
                inimigo = Inimigo1(self.in1_img, x, largura_tela, altura_tela, tamanho_veiculo, self.powerup1_img, "vida")
            case 2: 
                inimigo = Inimigo2(self.in2_img, x, largura_tela, altura_tela, tamanho_veiculo, self.powerup2_img, "velocidade")
            case 3:
                inimigo = Inimigo3(self.in3_img, x, largura_tela, altura_tela, tamanho_veiculo, self.powerup3_img, "tiro")
            case 4:
                inimigo = Inimigo4(self.in4_img, x, largura_tela, altura_tela, tamanho_veiculo, self.powerup4_img, "dano")
            case _: 
                return
        self.inimigos.append(inimigo)

    def criar_powerups(self, tipo, x, largura_tela, altura_tela, tamanho_veiculo):
        inimigo_powerups = {
            1: (self.in1_img, self.powerup1_img, "vida"),
            2: (self.in2_img, self.powerup2_img, "velocidade"),
            3: (self.in3_img, self.powerup3_img, "tiro"),
            4: (self.in4_img, self.powerup4_img, "dano"),
        }

        if tipo in inimigo_powerups:
            inimigo_img, powerup_img, powerup_efeito = inimigo_powerups[tipo]
            inimigo = Inimigo(inimigo_img, x, largura_tela, altura_tela, tamanho_veiculo, powerup_img, powerup_efeito)
            self.inimigos.append(inimigo)
  
    def colisao_tiro(self, tiro, objeto):
        """Verifica colisão com outro objeto (Tiro ou Jogador)."""
        if isinstance(objeto, Veiculo):
            # Colisão do tiro com o jogador
            if objeto.x <= tiro.x <= objeto.x + objeto.tamanho_veiculo \
                and objeto.y <= tiro.y <= objeto.y + objeto.tamanho_veiculo:
                objeto.integridade -= tiro.dano_tiro  # Dano fixo por tiro
                tiro.ativo = False
        
        if isinstance(objeto, Inimigo):
            #Colisão do tiro com o inimigo
            if objeto.rect.x <= tiro.x <= objeto.rect.x + objeto.tamanho_veiculo \
                and objeto.rect.y <= tiro.y <= objeto.rect.y + objeto.tamanho_veiculo:
                objeto.integridade -= tiro.dano_tiro  # Dano fixo por tiro
                tiro.ativo = False

    def verificar_colisoes_powerups(self):
        for powerup in self.powerups[:]:
            for veiculo in self.veiculos:
                veiculo_rect = pygame.Rect(veiculo.x, veiculo.y, veiculo.tamanho_veiculo, veiculo.tamanho_veiculo)
                if powerup.rect.colliderect(veiculo_rect):
                    powerup.aplicar_efeito(veiculo) 
                    self.powerups.remove(powerup)

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
                        inimigo.ultimo_tempo_colisao = tempo_atual

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
                            veiculo.y = max(self.limite_superior, veiculo.y - 5)

                        # Inverte a direção
                        inimigo.velocidade_horizontal *= -1
                        inimigo.velocidade_vertical *= -1

                        # Limita o inimigo aos limites da tela
                        inimigo.rect.x = max(0, min(self.largura_tela - inimigo.tamanho_veiculo, inimigo.rect.x))
                        inimigo.rect.y = max(self.limite_superior, min(self.altura_tela - inimigo.tamanho_veiculo, inimigo.rect.y))
                        veiculo.x = max(0, min(self.largura_tela - veiculo.tamanho_veiculo, veiculo.x))
                        veiculo.y = max(self.limite_superior, min(self.altura_tela - veiculo.tamanho_veiculo, veiculo.y))

    def verificar_colisoes_entre_veiculos(self):
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
                self.v1.y = max(self.limite_superior, self.v1.y - 5)
                self.v2.y = min(self.altura_tela - self.v2.tamanho_veiculo, self.v2.y + 5)
            else:
                self.v1.y = min(self.altura_tela - self.v1.tamanho_veiculo, self.v1.y + 5)
                self.v2.y = max(self.limite_superior, self.v2.y - 5)

    def colisoes_dos_tiros(self):

        for inimigo in self.inimigos:
            for tiro in inimigo.tiros[:]:
                self.colisao_tiro(tiro, self.v1)
                self.colisao_tiro(tiro, self.v2)
                # tiro.colisao(self.v1)
                # tiro.colisao(self.v2)
                if not tiro.ativo:
                    inimigo.tiros.remove(tiro)
        
        for tiro in self.v1.tiros[:]:
            self.colisao_tiro(tiro, self.v2)
            # tiro.colisao(self.v2)
            for inimigo in self.inimigos:
                self.colisao_tiro(tiro, inimigo)
                # tiro.colisao(inimigo)
            if not tiro.ativo:
                self.v1.tiros.remove(tiro)
        
        for tiro in self.v2.tiros[:]:
            self.colisao_tiro(tiro, self.v1)
            # tiro.colisao(self.v1)
            for inimigo in self.inimigos:
                self.colisao_tiro(tiro, inimigo)
                # tiro.colisao(inimigo)
            if not tiro.ativo:
                self.v2.tiros.remove(tiro)

    def run(self):
        # Inicializa o jogo e faz aprecer um inimigo por vez
        self.is_running = True
        inimigos = [1, 2, 3, 4]
        while self.is_running:
            if len(self.inimigos) < self.max_inimigos and pygame.time.get_ticks() - self.timer_inimigos > 20000:
                if inimigos:
                    idx = random.choice(inimigos)
                    self.criar_inimigos(idx, self.largura_tela // 2, self.largura_tela, self.altura_tela, self.tamanho_veiculo)
                    inimigos.remove(idx)
                    self.timer_inimigos = pygame.time.get_ticks()

            if len(inimigos) == 0:
                inimigos = [1, 2, 3, 4]

            # Checar a tecla de disparo
            keys = pygame.key.get_pressed()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_b]:
                self.v1.disparar()
            if keys[pygame.K_SEMICOLON]:
                self.v2.disparar()

            self.v1.rotacionar()
            self.v2.rotacionar()
            self.v1.atualizar_tiros()
            self.v2.atualizar_tiros()

            self.eventos()
            self.draw()
            self.update()
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

        for inimigo in self.inimigos[:]:
            if len(self.v1.tiros) > 0 or len(self.v2.tiros) > 0:
                for tiro in self.v1.tiros:
                    if inimigo.colisao(tiro, self.veiculos[0], self.powerups):
                        self.v1.tiros.remove(tiro)
                        if inimigo.integridade <= 0:
                            # Cria um power-up correspondente ao tipo do inimigo
                            self.inimigos.remove(inimigo)
                            break
                for tiro in self.v2.tiros:
                    if inimigo.colisao(tiro, self.veiculos[1], self.powerups):
                        self.v2.tiros.remove(tiro)
                        if inimigo.integridade <= 0:
                            # Cria um power-up correspondente ao tipo do inimigo
                            self.inimigos.remove(inimigo)
                            break
            inimigo.update(None, self.veiculos, self.powerups)

        self.verificar_colisoes_powerups()
        self.verificar_colisoes_entre_inimigos()
        self.verificar_colisoes_entre_veiculos_e_inimigos()
        self.verificar_colisoes_entre_veiculos()
        self.colisoes_dos_tiros()

        # Verifica se a integridade de algum veículo chegou a zero
        if self.v1.integridade <= 0 or self.v2.integridade <= 0:
            print("Fim de Jogo!")
            self.is_running = False

    def draw(self):
        self.tela.fill((255, 255, 255)) # Fundo branco
        self.v1.draw(self.tela)
        self.v2.draw(self.tela)
        for inimigo in self.inimigos:
            inimigo.draw(self.tela)
        
        for powerup in self.powerups:
            powerup.draw(self.tela)
            if powerup.expirado():
                self.powerups.remove(powerup)
        
        # Exibe a integridade no topo
        self.v1.mostrar_integridade(self.tela, (20, 25))  # v1 no canto superior esquerdo
        self.v2.mostrar_integridade(self.tela, (self.largura_tela - 250, 25))  # v2 no canto superior direito
        
        pygame.display.flip()

if __name__ == '__main__':
    jogo = Gerenciador()
    jogo.run()