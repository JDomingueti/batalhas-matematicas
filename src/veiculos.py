import pygame
import random
from abc import ABC, abstractmethod
from typing import List
import math
import time

class Veiculo:
    def __init__(self, caminho_imagem, x, y, largura_tela, altura_tela, tamanho_veiculo, teclas, tiro_inverso=False):
        self.caminho_imagem = caminho_imagem
        self.tamanho_veiculo = tamanho_veiculo
        self.x = x
        self.y = y
        self.integridade = 100
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.velocidade = 10
        self.angulo = 0
        self.tiros = []
        self.dano = 1
        self.ultimo_disparo = 0 
        self.intervalo_tiro = 1
        self.velocidade_tiro = 10
        self.teclas = teclas
        self.tiro_inverso = tiro_inverso

    def processar_movimento(self, keys, is_v1=True):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        if keys[self.teclas['esquerda']]:
            dx = -self.velocidade
        if keys[self.teclas['direita']]:
            dx = self.velocidade
        if keys[self.teclas['cima']]:
            dy = -self.velocidade
        if keys[self.teclas['baixo']]:
            dy = self.velocidade
        
        novo_x = self.x + dx
        if(0 <= novo_x and novo_x <= self.largura_tela - self.tamanho_veiculo): self.x = novo_x

        novo_y = self.y + dy
        if(50 <= novo_y and novo_y <= self.altura_tela - self.tamanho_veiculo): self.y = novo_y

    def rotacionar(self):
        keys = pygame.key.get_pressed()

        if keys[self.teclas['rotacao_anti_horaria']]:
            self.angulo += 3
        if keys[self.teclas['rotacao_horaria']]:
            self.angulo -= 3
                
    def disparar(self, is_v1=True):
        tempo_atual = time.time()
        if tempo_atual - self.ultimo_disparo >= self.intervalo_tiro:
            centro_x = self.x + self.tamanho_veiculo / 2
            centro_y = self.y + self.tamanho_veiculo / 2
            angulo_tiro  = self.angulo
            if self.tiro_inverso:
                angulo_tiro += 180
            novo_tiro = Tiro(centro_x, centro_y, angulo_tiro, self.velocidade_tiro)
            self.tiros.append(novo_tiro)
            self.ultimo_disparo = tempo_atual

    def draw(self, surface):
        # Desenhar o jogador
        imagem = pygame.image.load(self.caminho_imagem)
        imagem = pygame.transform.scale(imagem, (self.tamanho_veiculo, self.tamanho_veiculo))
        imagem_rotacionada = pygame.transform.rotate(imagem, self.angulo)
        novo_retangulo = imagem_rotacionada.get_rect(center=(self.x + self.tamanho_veiculo / 2, self.y + self.tamanho_veiculo / 2))
        surface.blit(imagem_rotacionada, novo_retangulo.topleft)
        
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
    def __init__(self, x, y, angulo, velocidade, cor = (255, 255, 0), dano_tiro=5):
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.angulo = angulo
        self.raio = 5
        self.dano_tiro = dano_tiro
        self.cor = cor
        self.ativo = True
    
    def mover(self):
        # Calcula o movimento a partir do ângulo fornecido
        self.x += math.cos(math.radians(self.angulo)) * self.velocidade
        self.y -= math.sin(math.radians(self.angulo)) * self.velocidade  # Y diminui para cima na tela
        
    def draw(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)
    
    def colisao(self, objeto):
        """Verifica colisão com outro objeto (Tiro ou Jogador)."""
        if isinstance(objeto, Veiculo):
            # Colisão do tiro com o jogador
            if objeto.x <= self.x <= objeto.x + objeto.tamanho_veiculo \
                and objeto.y <= self.y <= objeto.y + objeto.tamanho_veiculo:
                objeto.integridade -= self.dano_tiro  # Dano fixo por tiro
                self.ativo = False
        
        if isinstance(objeto, Inimigo):
            #Colisão do tiro com o inimigo
            if objeto.rect.x <= self.x <= objeto.rect.x + objeto.tamanho_veiculo \
                and objeto.rect.y <= self.y <= objeto.rect.y + objeto.tamanho_veiculo:
                objeto.integridade -= self.dano_tiro  # Dano fixo por tiro
                self.ativo = False

class PowerUp:
    def __init__(self, path_image, x, y, efeito, tamanho_veiculo):
        self.x = x
        self.y = y
        self.tamanho_veiculo = tamanho_veiculo
        self.image = pygame.image.load(path_image)
        self.image = pygame.transform.scale(self.image, (self.tamanho_veiculo, self.tamanho_veiculo))
        self.rect = pygame.Rect(self.x, self.y, self.tamanho_veiculo, self.tamanho_veiculo)
        self.tempo_vida = 5  # dura 5 segundos
        self.criado_em = time.time()
        self.efeito = efeito

    def aplicar_efeito(self, veiculo):
        if self.efeito == "velocidade":
            veiculo.velocidade += 2
        elif self.efeito == "vida":
            veiculo.integridade = min(100, veiculo.integridade + 20)
        elif self.efeito == "tiro":
            veiculo.velocidade_tiro += 5
        elif self.efeito == "dano":
            veiculo.dano += 1

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def expirado(self):
        return time.time() - self.criado_em > self.tempo_vida

class Inimigo(pygame.sprite.Sprite, ABC):
    def __init__(self, path_image, x, largura_tela, altura_tela, tamanho_veiculo, powerup_image, powerup_efeito):
        super().__init__() 
        self.tamanho_veiculo = tamanho_veiculo
        self.image = pygame.image.load(path_image)
        self.image = pygame.transform.scale(self.image, (self.tamanho_veiculo, self.tamanho_veiculo))  
        self.rect = self.image.get_rect()  
        self.rect.x = x
        self.rect.y = 50
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.velocidade = 2
        self.velocidade_vertical = 2
        self.velocidade_horizontal = 3
        self.ultimo_tempo_colisao = pygame.time.get_ticks()
        self.angulo = 0
        self.tiros = []
        self.ultimo_disparo = 0
        self.intervalo_tiro = 5 # 5 segundos
        self.limite_distancia = 200
        self.integridade = 10
        self.powerup_image = powerup_image
        self.powerup_efeito = powerup_efeito
           
    def perseguir_veiculo(self, veiculos):
        veiculo_proximo = min(veiculos, key=lambda veiculo: pygame.Vector2(veiculo.x, veiculo.y).distance_to(self.rect.center))
        direcao = pygame.Vector2(veiculo_proximo.x - self.rect.x, veiculo_proximo.y - self.rect.y)
        distancia_ate_veiculo = direcao.length()

        if distancia_ate_veiculo > self.limite_distancia:
            movimento = direcao.normalize() * self.velocidade
            self.rect.x += movimento.x
            self.rect.y += movimento.y
            self.angulo = -math.degrees(math.atan2(direcao.y, direcao.x))

            self.rect.x = max(0, min(self.largura_tela - self.tamanho_veiculo, self.rect.x))
            self.rect.y = max(0, min(self.altura_tela - self.tamanho_veiculo, self.rect.y))

    def disparar(self, veiculos):
        veiculo_proximo = min(veiculos, key=lambda veiculo: pygame.Vector2(veiculo.x, veiculo.y).distance_to(self.rect.center))
        direcao_x = veiculo_proximo.x - self.rect.x
        direcao_y = veiculo_proximo.y - self.rect.y
        self.angulo = -math.degrees(math.atan2(direcao_y, direcao_x))

        tempo_atual = time.time()
        if tempo_atual - self.ultimo_disparo >= self.intervalo_tiro:
            centro_x = self.rect.centerx
            centro_y = self.rect.centery
            novo_tiro = Tiro(centro_x, centro_y, self.angulo, 3, (255, 0, 0))
            self.tiros.append(novo_tiro)
            self.ultimo_disparo = tempo_atual

    def draw(self, surface):
        image_rotacionada = pygame.transform.rotate(self.image, self.angulo+180)
        novo_retangulo = image_rotacionada.get_rect(topleft=(self.rect.x, self.rect.y))
        surface.blit(image_rotacionada, novo_retangulo)
        for tiro in self.tiros:
            tiro.draw(surface)

    def atualizar_tiros(self):
        for tiro in self.tiros[:]:
            tiro.mover()
            if tiro.x < 0 or tiro.x > self.largura_tela or tiro.y < 0 or tiro.y > self.altura_tela:
                self.tiros.remove(tiro)
    
    def colisao(self, tiro, veiculos, powerups):
        if tiro != None:
            if self.rect.colliderect(pygame.Rect(tiro.x - tiro.raio, tiro.y - tiro.raio, tiro.raio * 2, tiro.raio * 2)):
                self.integridade -= veiculos.dano

                if self.integridade <= 0:
                    powerup = PowerUp(self.powerup_image, self.rect.x, self.rect.y, self.powerup_efeito, self.tamanho_veiculo)
                    powerups.append(powerup)
                return True  # Remove o inimigo da lista
        return False

    @abstractmethod
    def update(self, tiros, veiculos, powerups):
        self.perseguir_veiculo(veiculos)
        self.disparar(veiculos) 
        self.atualizar_tiros()

class Inimigo1(Inimigo):       
    def __init__(self, path_image, x, largura_tela, altura_tela, tamanho_veiculo, powerup_img, powerup_efeito):
        super().__init__(path_image, x, largura_tela, altura_tela, tamanho_veiculo, powerup_img, powerup_efeito)

    def update(self, tiros, veiculos, powerups):  
        return super().update(tiros, veiculos, powerups)

class Inimigo2(Inimigo):       
    def __init__(self, path_image, x, largura_tela, altura_tela, tamanho_veiculo, powerup_img, powerup_efeito):
        super().__init__(path_image, x, largura_tela, altura_tela, tamanho_veiculo, powerup_img, powerup_efeito)

    def update(self, tiros, veiculos, powerups):  
        return super().update(tiros, veiculos, powerups)

class Inimigo3(Inimigo):       
    def __init__(self, path_image, x, largura_tela, altura_tela, tamanho_veiculo, powerup_img, powerup_efeito):
        super().__init__(path_image, x, largura_tela, altura_tela, tamanho_veiculo, powerup_img, powerup_efeito)

    def update(self, tiros, veiculos, powerups):  
        return super().update(tiros, veiculos, powerups)

class Inimigo4(Inimigo):       
    def __init__(self, path_image, x, largura_tela, altura_tela, tamanho_veiculo, powerup_img, powerup_efeito):
        super().__init__(path_image, x, largura_tela, altura_tela, tamanho_veiculo, powerup_img, powerup_efeito)

    def update(self, tiros, veiculos, powerups):  
        return super().update(tiros, veiculos, powerups)

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
                tiro.colisao(self.v1)
                tiro.colisao(self.v2)
                if not tiro.ativo:
                    inimigo.tiros.remove(tiro)

        
        for tiro in self.v1.tiros[:]:
            tiro.colisao(self.v2)
            for inimigo in self.inimigos:
                tiro.colisao(inimigo)
            if not tiro.ativo:
                self.v1.tiros.remove(tiro)
        
        for tiro in self.v2.tiros[:]:
            tiro.colisao(self.v1)
            for inimigo in self.inimigos:
                tiro.colisao(inimigo)
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