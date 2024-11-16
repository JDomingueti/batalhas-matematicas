import pygame
import math
import time

largura_tela = 800
altura_tela = 600
espaço_do_placar = 70
sprite_path_jogador_1 = "../assets/veiculos/foguete1.png"
sprite_path_jogador_2 = "../assets/veiculos/foguete2.png"
dano_tiro = 5

pygame.init()
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Jogar")

class Tiro:
    def __init__(self, x, y, angulo):
        self.x = x
        self.y = y
        self.velocidade = 1
        self.angulo = angulo
        self.raio = 5
        self.ativo = True
    
    def mover(self):
        self.x += math.cos(math.radians(self.angulo)) * self.velocidade
        self.y -= math.sin(math.radians(self.angulo)) * self.velocidade
        
    def desenhar(self, surface):
        pygame.draw.circle(surface, (255, 255, 0), (int(self.x), int(self.y)), self.raio)
    
    def colisao(self, objeto):
        """Verifica colisão com outro objeto (Tiro ou Jogador)."""
        if isinstance(objeto, Jogador):
            # Colisão do tiro com o jogador
            if objeto.x <= self.x <= objeto.x + objeto.largura \
                and objeto.y <= self.y <= objeto.y + objeto.altura:
                objeto.integridade -= dano_tiro  # Dano fixo por tiro
                self.ativo = False

class Jogador:
    def __init__(self, x, y, largura, altura, sprite, teclas, tiro_inverso=False, integridade_inicial=100):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.sprite = sprite
        self.velocidade = 0.5
        self.angulo = 0
        self.tiros = []
        self.ultimo_disparo = 0
        self.intervalo_tiro = 0.5
        self.teclas = teclas
        self.tiro_inverso = tiro_inverso
        self.integridade = integridade_inicial
    
    def mover(self):
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
        if(0 <= novo_x and novo_x <= largura_tela - largura_imagem): self.x = novo_x

        novo_y = self.y + dy
        if(espaço_do_placar <= novo_y and novo_y <= altura_tela - altura_imagem): self.y = novo_y

    def rotacionar(self):
        keys = pygame.key.get_pressed()

        if keys[self.teclas['rotacao_anti_horaria']]:
            self.angulo += 0.3
        if keys[self.teclas['rotacao_horaria']]:
            self.angulo -= 0.3

    def disparar(self):
        tempo_atual = time.time()
        if tempo_atual - self.ultimo_disparo >= self.intervalo_tiro:
            centro_x = self.x + self.largura / 2
            centro_y = self.y + self.altura / 2
            angulo_tiro  = self.angulo
            if self.tiro_inverso:
                angulo_tiro += 180
            novo_tiro = Tiro(centro_x, centro_y, angulo_tiro)
            self.tiros.append(novo_tiro)
            self.ultimo_disparo = tempo_atual
    
    def desenhar(self, surface):
        # Desenhar o jogador
        sprite_rotacionada = pygame.transform.rotate(self.sprite, self.angulo)
        novo_retangulo = sprite_rotacionada.get_rect(center=(self.x + self.largura / 2, self.y + self.altura / 2))
        surface.blit(sprite_rotacionada, novo_retangulo.topleft)
        
        # Desenhar os tiros
        for tiro in self.tiros:
            tiro.desenhar(surface)
        
    def atualizar_tiros(self):
        for tiro in self.tiros[:]:
            tiro.mover()
            if tiro.x < 0 or tiro.x > largura_tela or tiro.y < 0 or tiro.y > altura_tela:
                tiro.ativo = False
            if not tiro.ativo: self.tiros.remove(tiro)
    
    def mostrar_integridade(self, posicao_x, posicao_y):
        fonte = pygame.font.Font(None, 36)
        texto = fonte.render(f"Integridade: {self.integridade:,.2f}", True, (0, 0, 0))
        tela.blit(texto, (posicao_x, posicao_y))

    def esta_vivo(self):
        """Verifica se o jogador está vivo."""
        return self.integridade > 0



# Carregar a imagem da sprite
sprite_imagem_jogador_1 = pygame.image.load(sprite_path_jogador_1)
sprite_imagem_jogador_2 = pygame.image.load(sprite_path_jogador_2)

largura_imagem = 50
altura_imagem = 50
sprite_imagem_1 = pygame.transform.scale(sprite_imagem_jogador_1, (largura_imagem, altura_imagem))
sprite_imagem_2 = pygame.transform.scale(sprite_imagem_jogador_2, (largura_imagem, altura_imagem))

# Controles para cada jogador
controles_jogador_1 = {
    'esquerda': pygame.K_a,
    'direita': pygame.K_d,
    'cima': pygame.K_w,
    'baixo': pygame.K_s,
    'rotacao_anti_horaria': pygame.K_c,
    'rotacao_horaria': pygame.K_v,
    'disparo': pygame.K_b
}

controles_jogador_2 = {
    'esquerda': pygame.K_LEFT,
    'direita': pygame.K_RIGHT,
    'cima': pygame.K_UP,
    'baixo': pygame.K_DOWN,
    'rotacao_anti_horaria': pygame.K_COMMA,
    'rotacao_horaria': pygame.K_PERIOD,
    'disparo': pygame.K_SEMICOLON
}

# Iniciando os jogadores
x1_inicial = 50
y1_inicial = espaço_do_placar
x2_inicial = 700
y2_inicial = 500
jogador_1 = Jogador(x1_inicial, y1_inicial, largura_imagem, altura_imagem, sprite_imagem_1, controles_jogador_1, False)
jogador_2 = Jogador(x2_inicial, y2_inicial, largura_imagem, altura_imagem, sprite_imagem_2, controles_jogador_2, True)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Tecla de disparo de cada jogador
    keys = pygame.key.get_pressed()
    if keys[controles_jogador_1['disparo']]:
        jogador_1.disparar()
    if keys[controles_jogador_2['disparo']]:
        jogador_2.disparar()
    
    jogador_1.mover()
    jogador_1.rotacionar()
    jogador_1.atualizar_tiros()

    jogador_2.mover()
    jogador_2.rotacionar()
    jogador_2.atualizar_tiros()

    tela.fill((255, 255, 255))
    jogador_1.desenhar(tela)
    jogador_2.desenhar(tela)

    for tiro in jogador_1.tiros[:]:
        tiro.colisao(jogador_2) # Verifica colisão entre tiro do jogador 1 e jogador 2
    
    for tiro in jogador_2.tiros[:]:
        tiro.colisao(jogador_1) # Verifica colisão entre tiro do jogador 2 e jogador 1

    jogador_1.mostrar_integridade(20, 25)  # v1 no canto superior esquerdo
    jogador_2.mostrar_integridade(largura_tela - 250, 25)  # v2 no canto superior direito       
    pygame.display.flip()

    running = jogador_1.esta_vivo()
    if running: running = jogador_2.esta_vivo()
pygame.quit()