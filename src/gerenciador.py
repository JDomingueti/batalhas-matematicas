import pygame
import random
from typing import List
from veiculos import Veiculo
from inimigos import *

class Gerenciador:
    def __init__(self, largura, altura, display: pygame.SurfaceType, configs = None, cenario = None, vol_efeitos = 1) -> None:
        """
        Inicializa a classe Gerenciador, configurando os principais elementos do jogo.

        Este método define os atributos básicos necessários para o funcionamento do jogo,
        incluindo as dimensões da tela, veículos dos jogadores, inimigos, power-ups, e
        os controles atribuídos para cada veículo.

        Atributos
        ----------
        largura_tela : int
            Largura da janela do jogo (padrão: 800).
        altura_tela : int
            Altura da janela do jogo (padrão: 600).
        tamanho_veiculo : int
            Dimensão (em pixels) do lado de cada veículo (padrão: 70).
        limite_superior : int
            Distância mínima (em pixels) do topo da tela (padrão: 50).
        tela : pygame.Surface
            Superfície que representa a janela principal do jogo.
        clock : pygame.time.Clock
            Gerenciador do tempo de atualização (frames por segundo).
        is_running : bool
            Estado do jogo (True se está ativo; False caso contrário).
        v1_img, v2_img, in1_img, ... : str
            Caminhos para os arquivos de imagem de veículos, inimigos e power-ups.
        v1, v2 : Veiculo
            Instâncias dos veículos controlados pelos jogadores.
        inimigos : list[Inimigo]
            Lista de inimigos presentes no jogo.
        powerups : list[Powerup]
            Lista de power-ups ativos no jogo.
        max_inimigos : int
            Número máximo de inimigos simultâneos (padrão: 4).
        timer_inimigos : int
            Contador para controlar a criação de novos inimigos.
        controles_v1, controles_v2 : dict
            Mapeamento de teclas para os controles de cada jogador.
        """
        pygame.init()

        # Dimensões
        self.largura_tela = largura
        self.altura_tela = altura
        self.tamanho_veiculo = self.largura_tela/10
        self.limite_superior = self.altura_tela/12
        self.tela = display
        self.volume_efeitos = vol_efeitos
        pygame.display.set_caption("Batalhas Matemáticas")

        # Caminhos das imagens !
        if configs == None:
            v1_img = "../assets/veiculos/foguete1.png"
            v2_img = "../assets/veiculos/foguete2.png"
            self.in1_img = "../assets/inimigos/inimigo1_deserto.png"
            self.in2_img = "../assets/inimigos/inimigo2_deserto.png"
            self.in3_img = "../assets/inimigos/inimigo3_deserto.png"
            self.in4_img = "../assets/inimigos/inimigo4_deserto.png"
        else:
            v1_img = configs["cenarios"][cenario]["pl_1"]["img"]
            v2_img = configs["cenarios"][cenario]["pl_2"]["img"]
            self.in1_img = configs["cenarios"][cenario]["in_1"]
            self.in2_img = configs["cenarios"][cenario]["in_2"]
            self.in3_img = configs["cenarios"][cenario]["in_3"]
            self.in4_img = configs["cenarios"][cenario]["in_4"]
        
        # Caminhos das imagens dos powerups
        self.powerup1_img = "../assets/poderes/vida.png"
        self.powerup2_img = "../assets/poderes/velocidade.png"
        self.powerup3_img = "../assets/poderes/bala.png"
        self.powerup4_img = "../assets/poderes/dano.png"

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
        
        self.v1 = Veiculo(v1_img, 20, (self.altura_tela - self.tamanho_veiculo) // 2, self.largura_tela, self.altura_tela, self.tamanho_veiculo, controles_v1, volume_tiro=vol_efeitos)  
        self.v2 = Veiculo(v2_img, self.largura_tela - self.tamanho_veiculo - 20, (self.altura_tela - self.tamanho_veiculo) // 2, self.largura_tela, self.altura_tela, self.tamanho_veiculo, controles_v2, True, vol_efeitos)
        self.veiculos = [
            self.v1,
            self.v2,
        ]

        self.clock = pygame.time.Clock()
        self.tempo_respawn = 5000
        self.tempos_respawn = [0, 0]
        self.is_running = False

    def criar_inimigos(self, tipo, x, largura_tela, altura_tela, tamanho_veiculo):
        """
        Cria inimigos de acordo com o tipo especificado.

        Parâmetros
        ----------
        tipo : int
            Tipo de inimigo a ser criado.
        x : int
            Posição inicial no eixo X.
        largura_tela : int
            Largura da tela para os limites de movimento.
        altura_tela : int
            Altura da tela para os limites de movimento.
        tamanho_veiculo : int
            Tamanho dos inimigos.
        """

        match tipo: 
            case 1:
                inimigo = Inimigo1(self.in1_img, x, largura_tela, altura_tela, tamanho_veiculo, self.powerup1_img, "vida", self.volume_efeitos)
            case 2: 
                inimigo = Inimigo2(self.in2_img, x, largura_tela, altura_tela, tamanho_veiculo, self.powerup2_img, "velocidade", self.volume_efeitos)
            case 3:
                inimigo = Inimigo3(self.in3_img, x, largura_tela, altura_tela, tamanho_veiculo, self.powerup3_img, "tiro", self.volume_efeitos)
            case 4:
                inimigo = Inimigo4(self.in4_img, x, largura_tela, altura_tela, tamanho_veiculo, self.powerup4_img, "dano", self.volume_efeitos)
            case _: 
                return
        self.inimigos.append(inimigo)

    def criar_powerups(self, tipo, x, largura_tela, altura_tela, tamanho_veiculo):
        """
        Cria power-ups no jogo.

        Este método adiciona power-ups após a morte de inimigos com tipos correspondentes.

        Atualiza
        --------
        powerups : list[Powerup]
            Adiciona um novo objeto Powerup à lista de power-ups.

        """
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
        '''
        Verifica colisão com outro objeto (Inimigo ou Jogador).
        '''
        if isinstance(objeto, Veiculo):
            # Colisão do tiro com o jogador
            if objeto.x <= tiro.x <= objeto.x + objeto.tamanho \
                and objeto.y <= tiro.y <= objeto.y + objeto.tamanho:
                objeto.levar_dano(tiro.dano)
                tiro.ativo = False
        
        if isinstance(objeto, Inimigo):
            #Colisão do tiro com o inimigo
            if objeto.rect.x <= tiro.x <= objeto.rect.x + objeto.tamanho \
                and objeto.rect.y <= tiro.y <= objeto.rect.y + objeto.tamanho:
                objeto.levar_dano(tiro.dano)
                tiro.ativo = False

    def verificar_colisoes_powerups(self):
        """
        Verifica colisões entre veículos e power-ups.

        Se um veículo colidir com um power-up, aplica o efeito do power-up e remove-o da lista.
        """
        for powerup in self.powerups[:]:
            for veiculo in self.veiculos:
                if powerup.rect.colliderect(veiculo.rect):
                    powerup.aplicar_efeito(veiculo) 
                    self.powerups.remove(powerup)

    def verificar_colisoes_entre_inimigos(self):
        '''
        Verifica colisões entre os inimigos e resolve o impacto,
         ajustando suas posições e diminuindo integridade.
        '''
        for i, inimigo1 in enumerate(self.inimigos):
            for inimigo2 in self.inimigos[i + 1:]:
                if inimigo1.rect.colliderect(inimigo2.rect):
                    # Movimenta inimigos para longe um do outro
                    inimigo1.rect.x -= 5
                    inimigo1.rect.y -= 2  
                    inimigo2.rect.x += 5
                    inimigo2.rect.y += 2
                    inimigo1.velocidade = inimigo2.velocidade = 0

                    # Limita os inimigos aos limites da tela
                    inimigo1.rect.x = max(0, min(self.largura_tela - self.tamanho_veiculo, inimigo1.rect.x))
                    inimigo1.rect.y = max(0, min(self.altura_tela - self.tamanho_veiculo, inimigo1.rect.y))
                    inimigo2.rect.x = max(0, min(self.largura_tela - self.tamanho_veiculo, inimigo2.rect.x))
                    inimigo2.rect.y = max(0, min(self.altura_tela - self.tamanho_veiculo, inimigo2.rect.y))

    def verificar_colisoes_entre_veiculos_e_inimigos(self):
        '''
        Verifica colisões entre os veículos e inimigos e 
        resolve o impacto, ajustando suas posições e diminuindo integridade.
        '''
        tempo_atual = pygame.time.get_ticks()
        for inimigo in self.inimigos:
            for veiculo in self.veiculos:
                if inimigo.rect.colliderect(veiculo.rect):
                    if tempo_atual - inimigo.ultimo_tempo_colisao > 10:
                        veiculo.levar_dano(1)
                        inimigo.ultimo_tempo_colisao = tempo_atual

                        # Ajusta a posição do inimigo para longe do veiculo
                        if inimigo.rect.x < veiculo.rect.x:
                            inimigo.rect.x -= 10  # Move para a esquerda
                            veiculo.rect.x = min(self.largura_tela - veiculo.tamanho, veiculo.rect.x + 5)
                        elif inimigo.rect.x > veiculo.rect.x:
                            inimigo.rect.x += 10  # Move para a direita
                            veiculo.rect.x = max(0, veiculo.rect.x - 5)

                        if inimigo.rect.y < veiculo.rect.y:
                            inimigo.rect.y -= 10  # Move para cima
                            veiculo.rect.y = min(self.altura_tela - veiculo.tamanho, veiculo.rect.y + 5)
                        elif inimigo.rect.y > veiculo.rect.y:
                            inimigo.rect.y += 10  # Move para baixo
                            veiculo.rect.y = max(self.limite_superior, veiculo.rect.y - 5)

                        # Anula a velocidade temporariamente
                        inimigo.velocidade = 0

                        # Limita o inimigo aos limites da tela
                        inimigo.rect.x = max(0, min(self.largura_tela - inimigo.tamanho, inimigo.rect.x))
                        inimigo.rect.y = max(self.limite_superior, min(self.altura_tela - inimigo.tamanho, inimigo.rect.y))
                        veiculo.rect.x = max(0, min(self.largura_tela - veiculo.tamanho, veiculo.rect.x))
                        veiculo.rect.y = max(self.limite_superior, min(self.altura_tela - veiculo.tamanho, veiculo.rect.y))

    def verificar_colisoes_entre_veiculos(self):
        '''
        Verifica colisões entre os veículos e resolve o impacto, ajustando suas posições e diminuindo integridade.
        '''
        if self.v1.rect.colliderect(self.v2.rect):
            self.v1.levar_dano(1) 
            self.v2.levar_dano(1)

            if self.v1.rect.x < self.v2.rect.x:
                self.v1.rect.x = max(0, self.v1.rect.x - 5)
                self.v2.rect.x = min(self.largura_tela - self.v2.tamanho, self.v2.rect.x + 5)
            else:
                self.v1.rect.x = min(self.largura_tela - self.v1.tamanho, self.v1.rect.x + 5)
                self.v2.rect.x = max(0, self.v2.rect.x - 5)
            if self.v1.rect.y < self.v2.rect.y:
                self.v1.rect.y = max(self.limite_superior, self.v1.rect.y - 5)
                self.v2.rect.y = min(self.altura_tela - self.v2.tamanho, self.v2.rect.y + 5)
            else:
                self.v1.rect.y = min(self.altura_tela - self.v1.tamanho, self.v1.rect.y + 5)
                self.v2.rect.y = max(self.limite_superior, self.v2.rect.y - 5)

    def colisoes_dos_tiros(self, placar):
        """
        Verifica colisões dos tiros com veículos e inimigos.

        Ao colidir, o tiro aplica dano no veículo ou inimigo que sofreu o impacto
         e remove o tiro da lista.
        """
        for inimigo in self.inimigos:
            for tiro in inimigo.tiros[:]:
                self.colisao_tiro(tiro, self.v1)
                self.colisao_tiro(tiro, self.v2)
                if not tiro.ativo:
                    inimigo.tiros.remove(tiro)
        
        for tiro in self.v1.tiros[:]:
            self.colisao_tiro(tiro, self.v2)
            if self.v2.integridade <= 0 and self.v2.ativo:
                placar[0] += self.v2.pontos
            if not tiro.ativo:
                self.v1.tiros.remove(tiro)
        
        for tiro in self.v2.tiros[:]:
            self.colisao_tiro(tiro, self.v1)
            if self.v1.integridade <= 0 and self.v1.ativo:
                placar[1] += self.v1.pontos
            if not tiro.ativo:
                self.v2.tiros.remove(tiro)

    def run(self):
        """
        Método principal para iniciar o loop do jogo e fazer
         aparecer um inimigo por vez.
        """
        self.is_running = True
        inimigos = [1, 2, 3, 4]
        while self.is_running:
            if len(self.inimigos) < self.max_inimigos and pygame.time.get_ticks() - self.timer_inimigos > 20000:
                if inimigos:
                    idx = random.choice(inimigos)
                    self.criar_inimigos(idx, self.largura_tela // 2, self.largura_tela, self.altura_tela, self.tamanho_veiculo)
                    self.criar_inimigos(idx, self.largura_tela // 2, self.largura_tela, self.altura_tela, self.tamanho_veiculo)
                    inimigos.remove(idx)
                    self.timer_inimigos = pygame.time.get_ticks()

            if len(inimigos) == 0:
                inimigos = [1, 2, 3, 4]

            self.v1.atualizar_tiros()
            self.v2.atualizar_tiros()

            self.eventos()
            self.draw()
            
            # Checar movimentos e disparo
            keys = pygame.key.get_pressed()
            tmp = self.update(keys)
            self.clock.tick(30)

        pygame.quit()

    def eventos(self):
        """
        Gerencia os eventos do jogo, como entrada do teclado e fechamento da janela.

        Este método verifica eventos do Pygame, como o pressionamento de teclas
        e o encerramento da janela. É utilizado para determinar se o jogo
        deve continuar rodando.

        Atualiza
        --------
        is_running : bool
            Define como False caso o evento de fechamento seja detectado.
        """
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.is_running = False

    def update(self, keys, placar):
        '''
        Atualiza o estado do jogo, movendo os veículos, verificando colisões, criando novos inimigos, bem como geração e power-ups, 
        e apresentando estes na tela.
        '''
        # Atualiza a posição dos veículos e inimigos, bem como geração
        # de powerups e destruição das naves
        self.v1.processar_movimento(keys)
        self.v2.processar_movimento(keys)
        # Caso inimigo ou players sejam destruídos retorna os seus retângulos
        rect_destruido = []
        for inimigo in self.inimigos[:]:
            if len(self.v1.tiros) > 0 or len(self.v2.tiros) > 0:
                for tiro in self.v1.tiros:
                    if inimigo.colisao(tiro, self.veiculos[0], self.powerups):
                        self.v1.tiros.remove(tiro)
                        if inimigo.integridade <= 0: placar[0] += inimigo.pontos
                for tiro in self.v2.tiros:
                    if inimigo.colisao(tiro, self.veiculos[1], self.powerups):
                        self.v2.tiros.remove(tiro)
                        if inimigo.integridade <= 0: placar[1] += inimigo.pontos 
            if inimigo.integridade <= 0:
                rect_destruido.append(inimigo.rect)
                self.inimigos.remove(inimigo)
                continue
            inimigo.update(None, self.veiculos, self.powerups)
        for pos, player in enumerate(self.veiculos):
            if (player.integridade <= 0) and player.ativo:
                player.ativo = False
                rect_destruido.append(player.rect)
                self.tempos_respawn[pos] = pygame.time.get_ticks()
            elif not player.ativo and (pygame.time.get_ticks() - self.tempos_respawn[pos]) > self.tempo_respawn:
                player.integridade = 100
                player.ativo = True
                player.rect.x = 20 if pos == 0 else self.largura_tela - self.tamanho_veiculo - 20
                player.rect.y = (self.altura_tela - self.tamanho_veiculo) // 2
        
        self.verificar_colisoes_powerups()
        self.verificar_colisoes_entre_inimigos()
        self.verificar_colisoes_entre_veiculos_e_inimigos()
        self.verificar_colisoes_entre_veiculos()
        self.colisoes_dos_tiros(placar)

        return rect_destruido

    def draw(self):
        '''
        Desenha os elementos do jogo na tela.

        Este método é responsável por exibir os elementos visuais do jogo,
        como o plano de fundo, jogador, inimigos e power-ups, na janela do Pygame.

        Observações
        -----------
        A ordem de desenho é importante para garantir que os elementos
        sejam exibidos corretamente, com o jogador e os inimigos sobre o plano de fundo.

        Atualiza
        --------
        tela : pygame.Surface
            Atualiza a superfície da tela com os elementos do jogo.
        '''
        if __name__ == '__main__':
            self.tela.fill((255,255,255))
        if self.v1.ativo:
            self.v1.draw(self.tela)
        if self.v2.ativo:
            self.v2.draw(self.tela)
        for inimigo in self.inimigos:
            inimigo.draw(self.tela)
        for powerup in self.powerups:
            powerup.draw(self.tela)
            if powerup.expirado():
                self.powerups.remove(powerup)
        
        # Exibe a integridade no topo
        self.v1.mostrar_integridade(self.tela, (20, 25))  # v1 no canto superior esquerdo
        self.v2.mostrar_integridade(self.tela, (self.largura_tela - 250 * (self.largura_tela/800), 25))  # v2 no canto superior direito
        if __name__ == '__main__':
            print("main")
            pygame.display.flip()

    def atualizar_efeitos(self, novo_volume):
        self.volume_efeitos = novo_volume
        for veiculo in self.veiculos:
            veiculo.volume_tiro = novo_volume
        for inimigo in self.inimigos:
            inimigo.volume_tiro = novo_volume
        
if __name__ == '__main__':
    display = pygame.display.set_mode((800, 600))
    jogo = Gerenciador(800, 600, display)
    jogo.run()