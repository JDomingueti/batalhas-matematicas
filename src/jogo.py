import pygame, random , json
from typing import List
from abc import ABC, abstractmethod
from eventos import evento, eventos_oceano, eventos_deserto, eventos_espaco
import gerenciador

class jogo(ABC):
    '''
    Classe padrão dos cenários de jogo.
    Essa classe é definida com AbstractMethod, portanto possui métodos
    que devem ser implementados na definição de uma nova classe que a 
    herdem.

    Atributos
    ---------
    largura: int

        Comprimento em x do display atual
    
    altura: int

        Comprimento em y do display atual
        
    cor: ColorValue

        Valor de cor do fundo da tela. Em RGB ou texto
        (Ex: (0,0,0) ou ('Black'))

    display: pygame.display

        Janela utilizada pelo pygame

    fundo: pygame.Rect | pygame.Surface

        Fundo a ser utilizado no jogo.

    volume_musica: float

        Volume da música utilizada no jogo

    volume_efeitos: float

        Volume dos efeitos utilizados no jogo
        
    eventos: List[evento.evento]

        Lista dos eventos que estão sendo executados

    frame_atual: int

        Frame da execução atual. Aumentado no método `atualizar`.

    contador_eventos: int

        Valor que indica o tempo na qual o evento foi atualizado

    separador_eventos: int

        Valor mínimo para gerar um novo evento

    Métodos
    -------
    Métodos da classe:
        - __init__(largura, altura, cor, musica, efeitos, display)
        - atualizar()
        - desenhar()
        - checar_colisoes()
        - criar_obstaculos(vida, cor, nome, alcance)
        - gerar_eventos()
        - explodir(pygame.Rect)
    '''
    @abstractmethod
    def __init__(self, largura, altura, cor, volume_musica, volume_efeitos, display):
        '''
        Inicia a classe jogo. É def

        Parâmetros
        ----------
        largura: int
            
            Comprimento em x da tela

        altura: int

            Comprimento em y da tela

        cor: ColorValue

            Cor padrão do fundo da tela

        volume_musica: float

            Volume da música

        volume_efeitos: float

            Volume dos efeitos

        display: pygame.display         

            Janela sendo executada
        '''
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.display = display
        # O modo do display é atualizado para não permitir redimensionamento
        # enquanto estiver em jogo.
        if pygame.display.is_fullscreen():
            self.display = pygame.display.set_mode((largura, altura), pygame.FULLSCREEN)
        else:
            self.display = pygame.display.set_mode((largura, altura))
        self.fundo = pygame.rect.Rect(0, 0, largura, altura)
        self.display.fill(self.cor)
        self.volume_musica = volume_musica
        self.volume_efeitos = volume_efeitos
        self.eventos : List[evento.evento]= []
        self.obstaculos : List[obstaculo] = pygame.sprite.Group()
        self.contador_eventos = 0
        self.separador_eventos = 20000
        self.separador_inimigos = 10000
        self.frame_atual = 0
        # CADA CENARIO DEVE INICIALIZAR O GERENCIADOR
        # self.gerenciador = gerenciador.Gerenciador(...)
        self.idx_inimigos = [1, 2, 3, 4]
        self.fonte = pygame.font.SysFont("Terminal", self.largura//17)
        self.placar = [0, 0]
        self.tempo_jogo = 120000
        self.tempo_fim_jogo = pygame.time.get_ticks() + self.tempo_jogo
        self.tempo_em_pause = 0
        self.tick_atual = pygame.time.get_ticks()
        self.encerrar = False
        with open("configuracoes.json", "r", encoding="utf-8") as config_file:
            self.configuracoes = json.load(config_file)

    def mostrar_tempo(self):
        pos = [self.largura//2, self.altura//16]
        tempo_atual = (self.tempo_fim_jogo - self.tick_atual)//1000
        minutos = tempo_atual//60
        segundos = tempo_atual % 60
        str_tempo = self.fonte.render(f"{minutos:02.0f}:{segundos:02.0f}", False, (0,0,0))
        rect = str_tempo.get_rect()
        sfc = pygame.Surface((rect.width, rect.height))
        pos[0] -= rect.width//2
        pos[1] -= rect.height//2
        sfc.set_alpha(150)
        sfc.fill((255,255,255))
        self.display.blit(sfc, pos)
        self.display.blit(str_tempo, pos)
        
    def mostrar_placar(self):
        pos = [self.largura//2, 2*self.altura//15]
        str_placar = self.fonte.render(f"{self.placar[0]:04.0f}:{self.placar[1]:04.0f}", False, (0,0,0))
        rect = str_placar.get_rect()
        sfc = pygame.Surface((rect.width, rect.height))
        pos[0] -= rect.width//2
        pos[1] -= rect.height//2
        sfc.set_alpha(150)
        sfc.fill((255,255,255))
        self.display.blit(sfc, pos)
        self.display.blit(str_placar, pos)

    def gerenciador_naves(self):
        if len(self.gerenciador.inimigos) < self.gerenciador.max_inimigos and pygame.time.get_ticks() - self.gerenciador.timer_inimigos > self.separador_inimigos:
            if len(self.idx_inimigos) != 0:
                idx = random.choice(self.idx_inimigos)
                self.gerenciador.criar_inimigos(idx, self.gerenciador.largura_tela // 2, self.gerenciador.largura_tela, self.gerenciador.altura_tela, self.gerenciador.tamanho_veiculo)
                self.idx_inimigos.remove(idx)
                self.gerenciador.timer_inimigos = pygame.time.get_ticks()
            else:
                self.idx_inimigos = [1, 2, 3, 4]

        self.gerenciador.v1.atualizar_tiros()
        self.gerenciador.v2.atualizar_tiros()

        keys = pygame.key.get_pressed()
        rect = self.gerenciador.update(keys, self.placar)
        if rect != None:
            self.explodir(rect)

    def ultima_imagem(self):
        imagem = pygame.Surface((self.largura, self.altura))


    def atualizar(self):
        '''
        Método que atualiza as informações do jogo.
        '''
        if self.tick_atual >= self.tempo_fim_jogo:
            self.encerrar = True
            return
        if len(self.eventos) > 0:
            for evento in self.eventos:
                evento.aviso_direcao()
                evento.atualizar()
                if evento.matar(self.explodir):
                    self.eventos.remove(evento)
                    self.contador_eventos = pygame.time.get_ticks()
        else:
            self.gerar_eventos()
        self.checar_colisoes()
        self.gerenciador_naves()
        self.tick_atual = pygame.time.get_ticks()
        pygame.display.flip()
        self.frame_atual += 1

    def desenhar(self):
        '''
        Método que desenha todos as imagens do jogo no atributo 
        self.display
        '''
        self.display.blit(self.fundo, (0, 0))
        self.obstaculos.draw(self.display)
        self.gerenciador.draw()
        self.mostrar_placar()
        self.mostrar_tempo()
        if len(self.eventos) > 0:
            for evento in self.eventos:
                evento.desenhar()

    def checar_colisoes(self):
        '''
        Método que checa todas as colisões que podem ocorrer
        '''
        for bloco in self.obstaculos:
            for evento in self.eventos:
                colidiu = bloco.verificar_colisao(evento, 1)
                if colidiu:
                    self.obstaculos.remove(bloco)
        self.colisoes_tiros()
        self.colisoes_inimigos()
        self.colisoes_players()
        
    def colisoes_tiros(self):
        '''
        Com os blocos e eventos
        '''
        tiros = list()
        for inimigo in self.gerenciador.inimigos:
            tiros += inimigo.tiros
        for tiro in tiros:
            tiro_rect = pygame.Rect(tiro.x - tiro.raio, tiro.y - tiro.raio, 2 * tiro.raio, 2 * tiro.raio)
            colidiu = False
            for bloco in self.obstaculos:
                if tiro_rect.colliderect(bloco):
                    tiro.ativo = False
                    self.obstaculos.remove(bloco)
                    colidiu = True
                    break
            for evento in self.eventos:
                pontos = 0
                if evento.verificar_colisao(tiro_rect, tiro.dano)[0]:
                    tiro.ativo = False
        for pos, player  in enumerate([self.gerenciador.v1, self.gerenciador.v2]):
            for tiro in player.tiros:
                tiro_rect = pygame.Rect(tiro.x - tiro.raio, tiro.y - tiro.raio, 2 * tiro.raio, 2 * tiro.raio)
                colidiu = False
                for bloco in self.obstaculos:
                    if tiro_rect.colliderect(bloco):
                        tiro.ativo = False
                        self.obstaculos.remove(bloco)
                        colidiu = True
                        break
                for evento in self.eventos:
                    pontos = 0
                    colidiu, pontos = evento.verificar_colisao(tiro_rect, tiro.dano)
                    self.placar[pos] += pontos
                    if colidiu:
                        tiro.ativo = False

    def colisoes_inimigos(self):
        '''
        Com os blocos e eventos
        '''
        for inimigo in self.gerenciador.inimigos:
            for bloco in self.obstaculos:
                colidiu = bloco.verificar_colisao(inimigo, inimigo.dano)
                if colidiu:
                    inimigo.levar_dano(bloco.dano)
                if bloco.vida <= 0:
                    self.obstaculos.remove(bloco)
            for evento in self.eventos:
                if evento.verificar_colisao(inimigo.rect, inimigo.dano)[0]:
                    inimigo.levar_dano(evento.dano)
    
    def colisoes_players(self):
        '''
        Com os blocos e eventos
        '''
        for player in [self.gerenciador.v1, self.gerenciador.v2]:
            for bloco in self.obstaculos:
                colidiu = bloco.verificar_colisao(player, player.dano)
                if colidiu:
                    player.levar_dano(bloco.dano)
                if bloco.vida <= 0:
                    self.obstaculos.remove(bloco)
            for evento in self.eventos:
                if evento.verificar_colisao(player.rect, player.dano)[0]:
                    player.levar_dano(evento.dano)
    
    def criar_obstaculos(self, vida, cor = (0, 0, 0), nome = None, alcance = 0):
        '''
        Método destinado a geração dos obstáculos. Para isso deve ser
        incluido na classe o atributo self.mapa, que é uma matriz com 
        valores 'x' na posição onde deve ser desenhado o obstáculo.

        Parâmetros
        ----------

        vida: int

            Valor da vida de cada obstáculo
        
        cor: ColorValue

            Cor do bloco a ser gerado, caso não haja sprites

        nome: str

            Nome do arquivo na pasta `../assets/sprites/` a ser
            utilizado como sprite
        
        alcance: int

            Caso não inserido, o nome do arquivo a ser utilizado é o 
            passado comp argumento `nome`. Caso o valor alcance seja 
            diferente de 0, os nomes dos arquivos a serem utilizados 
            deverão estar no formato: '...{i}...' onde {i} é um valor 
            aleatório entre 1 e o valor `alcance`.
        '''
        for num_linha, linha in enumerate(self.mapa):
            for num_coluna, coluna in enumerate(linha):
                if coluna == 'x':
                    esquerda = num_coluna * self.largura_blocos
                    topo = num_linha * self.altura_blocos
                    if (alcance != 0):
                        escolha = random.randint(1, alcance)
                        bloco = obstaculo(esquerda, topo, self.largura_blocos, self.altura_blocos, vida, nome = nome.format(escolha))    
                        self.obstaculos.add(bloco)
                    else:
                        bloco = obstaculo(esquerda, topo, self.largura_blocos, self.altura_blocos, vida, cor, nome)
                        self.obstaculos.add(bloco)

    @abstractmethod
    def gerar_eventos(self):
        '''
        Método que varia na definição da classe e deve ser implementado
        que é responsável pela geração de eventos.
        '''
        pass
    
    def explodir(self, rect):
        '''
        Método que cria o evento `evento.explosao` em um retângulo passado
        como parâmetro.

        Parâmetro
        ---------
        rect: pygame.Rect
            Retângulo na qual deve ser gerado o evento
        '''
        if isinstance(rect, pygame.Rect):
            self.eventos.append(evento.explosao(rect, self.display, self.volume_efeitos))
        if isinstance(rect, List):
            for rects in rect:
                self.eventos.append(evento.explosao(rects, self.display, self.volume_efeitos))

class oceano(jogo):
    '''
    Subclasse de jogo que define o cenário `Oceano`.
    '''
    def __init__(self, largura, altura, cor, musica, efeitos, display):
        '''
        Atributos adicionais
        --------------------
        self.mapa: List[ List[ str ] ]

            Matriz contendo valores 'x' nas posições onde devem ser 
            criados os obstáculos e valores '' nas posições que devem
            ser ignoradas.
        
        self.tamanho_mapa: tuple[ int, int ]

            Tupla que possui o tamanho do mapa passado (número de colunas
            na primeira posição e de linhas na segunda posição)
        
        self.largura_blocos: int

            Valor que indica o tamanho em x dos blocos, com base na
            largura da tela e da quantidade de colunas do mapa

        self.altura_blocos: int

            Valor que indica o tamanho em y dos blocos, com base na
            altura da tela e da quantidade de linhas do mapa

        self.obstaculos: pygame.sprite.Group()

            Classe que contém todos os obstáculos gerados

        self.fundos: List[ pygame.Surface ]

            Lista com todas as imagens de fundo a serem utilizadas

        self.fundo_atual: int

            Valor que indica a posição do fundo em self.fundos que
            deve ser utilizado
        
        self.chances: dict{str: float}
        
            Dicionário que contem as chances de spawn de cada um dos 
            eventos (chances entre 0 e 1)
        '''
        super().__init__(largura, altura, cor, musica, efeitos, display)
        pygame.display.set_caption("Mapa oceano")
        self.gerenciador = gerenciador.Gerenciador(self.largura, self.altura, self.display, self.configuracoes, 'oceano', self.volume_efeitos)
        self.fundos = []
        for i in [1, 2]:
            fundo_i = pygame.image.load(f"../assets/fundos/oceano_{i}.png")
            fundo_i = pygame.transform.scale(fundo_i, (self.largura, self.altura))
            self.fundos.append(fundo_i)
        self.fundo_atual = 0
        self.fundo = self.fundos[self.fundo_atual]
        self.mapa = mapa_oceano
        self.tamanho_mapa = (len(self.mapa[0]), len(self.mapa))
        self.largura_blocos = self.largura // self.tamanho_mapa[0]
        self.altura_blocos = self.altura // self.tamanho_mapa[1]
        nome_obstaculo = "../assets/sprites/bloco_oceano_{0}.png"
        self.criar_obstaculos(10, nome = nome_obstaculo, alcance = 4)
        self.fundo_atual = 1
        self.chances = {
            'tubarao': 0.2,
            'caranguejo': 0.2,
            'bando_aguas_vivas': 0.3
        }

    def atualizar(self):
        super().atualizar()
        if self.frame_atual >= 30:
            self.frame_atual %= 30
            self.fundo_atual = (self.fundo_atual + 1) % 2
            self.fundo = self.fundos[self.fundo_atual]

    def gerar_eventos(self):
        # Caso não hajam eventos acontecendo, gera novos eventos.
        # Podem ser gerados mais de um evento em uma execução.
        if len(self.eventos) == 0:
            if (pygame.time.get_ticks() - self.contador_eventos) >= self.separador_eventos:
                chance_tubarao = random.random()
                if chance_tubarao <= self.chances['tubarao']:
                    self.eventos.append(eventos_oceano.tubarao(self.display, self.volume_efeitos))
                chance_caranguejo = random.random()
                if chance_caranguejo <= self.chances['caranguejo']:
                    self.eventos.append(eventos_oceano.caranguejo(self.display, self.volume_efeitos))
                chance_bando_aguas_vivas = random.random()
                if chance_bando_aguas_vivas <= self.chances['bando_aguas_vivas']:
                    self.eventos.append(eventos_oceano.bando_aguas_vivas(self.display, self.volume_efeitos))
                self.contador_eventos = pygame.time.get_ticks()

class deserto(jogo):
    '''
    Subclasse de jogo que define o cenário `Deserto`.
    '''
    def __init__(self, largura, altura, cor, musica, efeitos, display):
        '''
        Atributos adicionais
        --------------------
        self.mapa: List[ List[ str ] ]

            Matriz contendo valores 'x' nas posições onde devem ser 
            criados os obstáculos e valores '' nas posições que devem
            ser ignoradas.
        
        self.tamanho_mapa: tuple[ int, int ]

            Tupla que possui o tamanho do mapa passado (número de colunas
            na primeira posição e de linhas na segunda posição)
        
        self.largura_blocos: int

            Valor que indica o tamanho em x dos blocos, com base na
            largura da tela e da quantidade de colunas do mapa

        self.altura_blocos: int

            Valor que indica o tamanho em y dos blocos, com base na
            altura da tela e da quantidade de linhas do mapa

        self.obstaculos: pygame.sprite.Group()

            Classe que contém todos os obstáculos gerados

        self.fundos: List[ pygame.Surface ]

            Lista com todas as imagens de fundo a serem utilizadas

        self.fundo_atual: int

            Valor que indica a posição do fundo em self.fundos que
            deve ser utilizado
        
        self.chances: dict{str: float}
        
            Dicionário que contem as chances de spawn de cada um dos 
            eventos (chances entre 0 e 1)
        '''
        super().__init__(largura, altura, cor, musica, efeitos, display)
        self.gerenciador = gerenciador.Gerenciador(self.largura, self.altura, self.display, self.configuracoes, 'deserto', self.volume_efeitos)
        pygame.display.set_caption("Mapa deserto")
        self.fundos = []
        for i in [1,2]:
            fundo_i = pygame.image.load(f"../assets/fundos/deserto_{i}.png")
            fundo_i = pygame.transform.scale(fundo_i, (largura, altura))
            self.fundos.append(fundo_i)
        self.fundo_atual = 0
        self.fundo = self.fundos[self.fundo_atual]
        self.mapa = mapa_deserto
        self.tamanho_mapa = (len(self.mapa[0]), len(self.mapa))
        self.largura_blocos = largura // self.tamanho_mapa[0]
        self.altura_blocos = altura // self.tamanho_mapa[1]
        self.obstaculos = pygame.sprite.Group()
        nome_obstaculo = "../assets/sprites/bloco_deserto_{0}.png"
        self.criar_obstaculos(10, nome = nome_obstaculo, alcance = 4)
        self.fundo_atual = 1
        self.chances = {
            "bola_de_feno" : 0.3,
            "verme_da_areia" : 0.2,
            "nuvem_gafanhotos" : 0.3
        }
    
    def atualizar(self):
        super().atualizar()
        if self.frame_atual >= 90:
            self.frame_atual %= 90
            self.fundo_atual = (self.fundo_atual + 1) % 2
            self.fundo = self.fundos[self.fundo_atual]

    def gerar_eventos(self):
        if len(self.eventos) == 0:
            if (pygame.time.get_ticks() - self.contador_eventos) >= self.separador_eventos:
                chance_bola_de_feno = random.random()
                if chance_bola_de_feno <= self.chances['bola_de_feno']:
                    self.eventos.append(eventos_deserto.bola_de_feno(self.display, self.volume_efeitos))
                chance_verme_da_areia = random.random()
                if chance_verme_da_areia <= self.chances['verme_da_areia']:
                    self.eventos.append(eventos_deserto.verme_da_areia(self.display, self.volume_efeitos))
                chance_nuvem_gafanhotos = random.random()
                if chance_nuvem_gafanhotos <= self.chances['nuvem_gafanhotos']:
                    self.eventos.append(eventos_deserto.nuvem_gafanhotos(self.display, self.volume_efeitos))
                self.contador_eventos = pygame.time.get_ticks()

class espaco(jogo):
    '''
    Subclasse de jogo que define o cenário `Espaco`.
    '''
    def __init__(self, largura, altura, cor, musica, efeitos, display):
        '''
        Atributos adicionais
        --------------------
        self.mapa: List[ List[ str ] ]

            Matriz contendo valores 'x' nas posições onde devem ser 
            criados os obstáculos e valores '' nas posições que devem
            ser ignoradas.
        
        self.tamanho_mapa: tuple[ int, int ]

            Tupla que possui o tamanho do mapa passado (número de colunas
            na primeira posição e de linhas na segunda posição)
        
        self.largura_blocos: int

            Valor que indica o tamanho em x dos blocos, com base na
            largura da tela e da quantidade de colunas do mapa

        self.altura_blocos: int

            Valor que indica o tamanho em y dos blocos, com base na
            altura da tela e da quantidade de linhas do mapa

        self.obstaculos: pygame.sprite.Group()

            Classe que contém todos os obstáculos gerados

        self.fundos: List[ pygame.Surface ]

            Lista com todas as imagens de fundo a serem utilizadas

        self.fundo_atual: int

            Valor que indica a posição do fundo em self.fundos que
            deve ser utilizado
        
        self.chances: dict{str: float}
        
            Dicionário que contem as chances de spawn de cada um dos 
            eventos (chances entre 0 e 1)
        '''
        super().__init__(largura, altura, cor, musica, efeitos, display)
        self.gerenciador = gerenciador.Gerenciador(self.largura, self.altura, self.display, self.configuracoes, 'espaco', self.volume_efeitos)
        pygame.display.set_caption("Mapa espaco")
        self.fundos = []
        for i in [1,2]:
            fundo_i = pygame.image.load(f"../assets/fundos/espaco_{i}.png")
            fundo_i = pygame.transform.scale(fundo_i, (largura, altura))
            self.fundos.append(fundo_i)
        self.fundo_atual = 0
        self.fundo = self.fundos[self.fundo_atual]
        self.mapa = mapa_espaco
        self.tamanho_mapa = (len(self.mapa[0]), len(self.mapa))
        self.largura_blocos = largura // self.tamanho_mapa[0]
        self.altura_blocos = altura // self.tamanho_mapa[1]
        self.obstaculos = pygame.sprite.Group()
        nome_obstaculo = "../assets/sprites/bloco_espaco_{0}.png"
        self.criar_obstaculos(10, nome = nome_obstaculo, alcance = 4)
        self.fundo_atual = 1
        self.chances = {
            "cometa" : 0.2,
            "space" : 0.3
        }

    def atualizar(self):
        super().atualizar()
        if self.frame_atual >= 30:
            self.frame_atual %= 30
            self.fundo_atual = (self.fundo_atual + 1) % 2
            self.fundo = self.fundos[self.fundo_atual]

    def gerar_eventos(self):
        if len(self.eventos) == 0:
            if (pygame.time.get_ticks() - self.contador_eventos) >= self.separador_eventos:
                chance_cometa = random.random()
                if chance_cometa <= self.chances['cometa']:
                    self.eventos.append(eventos_espaco.cometa(self.display, self.volume_efeitos))
                chance_space = random.random()
                if chance_space <= self.chances['space']:
                    self.eventos.append(eventos_espaco.invasores_do_espaco(self.display, self.volume_efeitos))
                self.contador_eventos = pygame.time.get_ticks()

class obstaculo(pygame.sprite.Sprite):
    '''
    Subclasse que herda a classe pygame.sprite.Sprite destinada aos 
    obstáculos de cada mapa

    Atributos
    ---------
    image: pygame.SurfaceType
        
        Caso seja passado o parâmetro `nome`, é carregado o arquivo da 
        pasta `../assets/sprites/` com o respectivo nome.
        Caso não seja passado esse parâmetro, é gerada uma superfície
        com dimensões `largura` e `altura`, com fundo na cor passada 
        como parâmetro
         
    self.rect = pygame.Rect

        Retângulo referente a imagem carregada/gerada

    self.vida: int

        Valor que indica a vida do obstáculo
    '''
    def __init__(self, x, y, largura, altura, vida, cor = (150,150,150), nome = None, transparente: bool = False):
        '''
        Método de inicialização dos obstáculos

        Parâmetros
        ----------
        x: int
            
            Valor em x do lado esquerdo do obstáculo

        y: int
            
            Valor em y do topo do obstáculo

        largura: int

            Valor do comprimento em x do obstáculo

        altura: int

            Valor do comprimento em y do obstáculo

        vida: int

            Valor que indica a vida do obstáculo a ser criado

        cor: ColorValue

            Cor que será criado o bloco (Utilizado somente sem o 
            parâmetro `nome`)

        nome: str | None

            Nome do arquivo a ser carregado para utilizar de sprite.

        transparente: bool

            Caso queira criar um obstáculo transparente, deve ser passado
            esse parâmetro como true, sem passar o parâmetro `nome`
        '''
        super().__init__()
        if nome == None:
            self.image = pygame.Surface((largura, altura))
            if not transparente:
                self.image.fill(cor)
            self.rect = self.image.get_rect(topleft = (x, y))
        else:
            self.image = pygame.image.load(nome)
            self.image = pygame.transform.scale(self.image, (largura, altura))
            self.rect = self.image.get_rect(topleft = (x, y))
        self.largura_tela = pygame.display.get_surface().get_width()
        self.altura_tela = pygame.display.get_surface().get_height()
        self.largura = largura
        self.altura = altura
        self.vida = vida
        self.dano = 1
        self.contador_dano = 0
        self.separador_dano = 500

    def verificar_colisao(self, objeto, dano : int = 0):
        if isinstance(objeto, evento.evento):
            return objeto.verificar_colisao(self.rect, 1/2)[0]
        else:
            if self.rect.colliderect(objeto.rect):
                if objeto.rect.x < self.rect.x:
                    objeto.rect.x -= 10
                elif objeto.rect.x > self.rect.x:
                    objeto.rect.x += 10
                    
                if objeto.rect.y < self.rect.y:
                    objeto.rect.y -= 10
                elif objeto.rect.y > self.rect.y:
                    objeto.rect.y += 10
                objeto.velocidade = 0
                self.vida -= dano

                objeto.rect.y = max(0, min(objeto.rect.y, self.altura_tela - objeto.tamanho))
                objeto.rect.x = max(0, min(objeto.rect.x, self.largura_tela - objeto.tamanho))
                return True
        return False
            
mapa_oceano = [
    [" "," "," "," "," "," "," "," "," "," "," ","x","x","x","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," ","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x"," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x"," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," ","x"," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," ","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," ",],
    [" "," "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," ",],
    [" "," "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," ",],
    [" "," "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "," ",],
    [" "," "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "," ",],
    [" "," "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "," ",],
    [" "," "," "," "," ","x","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x","x"," "," "," "," "," ",],
    [" "," "," "," "," ","x","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x","x"," "," "," "," "," ",],
    [" "," "," "," "," ","x","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x","x"," "," "," "," "," ",],
    [" "," "," "," "," ","x","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x","x"," "," "," "," "," ",]
]

mapa_deserto = [
    [" "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," ","x"," "," "," "," ","x"," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," ","x","x","x","x","x","x"," "," "," "," "," "," "," "," "," "," ","x","x","x","x","x","x"," "," "," "," "," ",],
    [" "," "," "," "," "," ","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x"," "," "," "," "," "," ",],
    [" "," "," "," "," "," ","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x"," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," ",],
    [" "," "," "," "," "," ","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x"," "," "," "," "," "," ",],
    [" "," "," "," "," "," ","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x"," "," "," "," "," "," ",],
    [" "," "," "," "," ","x","x","x","x","x","x"," "," "," "," "," "," "," "," "," "," ","x","x","x","x","x","x"," "," "," "," "," ",]
]

mapa_espaco = [
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," "," ","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x"," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," ","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x"," "," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "],
    [" "," "," "," "," ","x","x","x"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","x","x","x"," "," "," "," "," "]
]
