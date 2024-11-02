import pygame, sys, botoes

class tela:
    def __init__(self, largura, altura, cor):
        self.largura = largura
        self.altura = altura
        self.tamanho = (self.largura, self.altura)
        self.display = pygame.display.set_mode(self.tamanho)
        self.display.fill(cor)
        self.is_running = True
        self.botoes = []
        self.pos_botao = 0
    
    def draw(self):
        self.display.fill((0,0,0))
        for botao in self.botoes:
            botao.display_botao(self.display)

    def update(self):
        for pos, botao in enumerate(self.botoes):
            if botao.mouse and not botao.focado:
                for botao_ in self.botoes:
                    botao_.focado = False
                self.pos_botao = pos
            botao.atualizar(self.display)
        pygame.display.flip()

    def mover_no_teclado(self, movimento: pygame.event.EventType):
        res = None
        if len(self.botoes) > 0:
            if movimento == pygame.K_UP:
                self.pos_botao = (self.pos_botao - 1)
                self.pos_botao %= len(self.botoes)
                for botao in self.botoes:
                    botao.focado = False
                self.botoes[self.pos_botao].focado = True
            elif movimento == pygame.K_DOWN:
                self.pos_botao = (self.pos_botao + 1)
                self.pos_botao %= len(self.botoes)
                for botao in self.botoes:
                    botao.focado = False
                self.botoes[self.pos_botao].focado = True
            elif movimento == pygame.K_LEFT:
                if isinstance(self.botoes[self.pos_botao], botoes.Controle_desl):
                    self.botoes[self.pos_botao].percent -= 0.1
            elif movimento == pygame.K_RIGHT:
                if isinstance(self.botoes[self.pos_botao], botoes.Controle_desl):
                    self.botoes[self.pos_botao].percent += 0.1
            else:
                pass
        if movimento == pygame.K_RETURN:
            res = self.checar_eventos(movimento)
        return res
    
    def checar_eventos(self, evento = None):
        pass

class inicio(tela):
    def __init__(self, largura, altura, cor, efeitos):
        super().__init__(largura, altura, cor)

        pygame.display.set_caption("Inicio")
        
        self.fonte = pygame.font.SysFont("Terminal", self.largura // 10)
        
        self.nome = self.fonte.render("Batalhas Matemáticas", False, "White")
        self.nome_rect = self.nome.get_rect(center = (self.largura//2, self.altura//5))

        self.jogar : botoes.Botao = botoes.Botao((self.largura//2, 2*self.altura//5), "Jogar", "Terminal", altura//10, "White", (120,0,0), efeitos = efeitos, focado = True)
        self.opcoes : botoes.Botao = botoes.Botao((self.largura//2, 3*self.altura//5), "Opções", "Terminal", altura//10, "White", (120,0,0), efeitos = efeitos)
        self.sair : botoes.Botao = botoes.Botao((self.largura//2, 4*self.altura//5), "Sair", "Terminal", altura//10, "White", (120,0,0), efeitos = efeitos)
        self.botoes = [self.jogar, self.opcoes, self.sair]

    def checar_eventos(self, evento = None):
        if evento == pygame.K_RETURN:
            match self.pos_botao:
                case 0:
                    return("jogar")
                case 1:
                    return("opcoes")
                case 2:
                    pygame.quit()
                    sys.exit()
                case _:
                    pass
        if self.jogar.destacado and pygame.mouse.get_pressed()[0]:
            return("jogar")
        if self.opcoes.destacado and pygame.mouse.get_pressed()[0]:
            return("opcoes")
        if self.sair.destacado and pygame.mouse.get_pressed()[0]:        
            pygame.quit()
            sys.exit()

    def draw(self):
        super().draw()
        self.display.blit(self.nome, self.nome_rect)

    def volume_efeitos(self, novo_volume):
        for botao in self.botoes:
            botao.som.set_volume(novo_volume)

class opcoes(tela):
    def __init__(self, largura, altura, cor, musica, efeitos):
        super().__init__(largura, altura, cor)
        pygame.display.set_caption("Opções")
        
        self.fonte = pygame.font.SysFont("Terminal", self.largura//10)
        self.nome = self.fonte.render("Opcões", False, "White")
        self.nome_rect = self.nome.get_rect(center = (self.largura//2, self.altura//5))
        
        self.voltar : botoes.Botao = botoes.Botao((self.largura//2, self.altura - self.altura//5), "Voltar", "Terminal", self.altura//15, "White", (120,0,0), efeitos = efeitos, focado = True)
        self.musica : botoes.Controle_desl = botoes.Controle_desl((3*self.largura//7, 2*self.altura//5), "Musica","Terminal", 40, (self.largura//3, 10), musica, (250, 250, 250))
        self.efeitos : botoes.Controle_desl = botoes.Controle_desl((3*self.largura//7, 3*self.altura//5), "Efeitos","Terminal", 40, (self.largura//3, 10), efeitos, (250, 250, 250))
        self.botoes = [self.voltar, self.musica, self.efeitos]

    def checar_eventos(self, evento = None):
        if evento == pygame.K_RETURN:
            match self.pos_botao:
                case 0:
                    return("voltar")
                case 1:
                    return("musica")
                case 2:
                    return("efeitos")
                case _:
                    pass
        if (self.voltar.destacado and pygame.mouse.get_pressed()[0]):
            return("voltar")
        if self.efeitos.destacado or self.efeitos.focado:
            return("efeitos")
        if self.musica.destacado or self.musica.focado:
            return("musica")
    
    def draw(self):
        super().draw()
        self.display.blit(self.nome, self.nome_rect)

    def atualizar_musica(self):
        return(self.musica.ler_posicao())

    def atualizar_efeitos(self):
        return(self.efeitos.ler_posicao())
    
    def volume_efeitos(self, novo_volume):
        self.voltar.som.set_volume(novo_volume)
    
class seletor_jogo(tela):
    def __init__(self, largura, altura, cor, efeitos):
        super().__init__(largura, altura, cor)
        
        pygame.display.set_caption("Seleção")
        self.fonte = pygame.font.SysFont("Terminal", self.largura//10)
        self.nome = self.fonte.render("Selecione o mapa", False, "White")
        self.nome_rect = self.nome.get_rect(center = (self.largura//2, self.altura//5))
        
        self.voltar : botoes.Botao = botoes.Botao((self.largura//2, self.altura - self.altura//5), "Voltar", "Terminal", self.altura//15, "White", (120,0,0), efeitos = efeitos, focado = True)
        self.botoes = [self.voltar]

    def checar_eventos(self, evento = None):
        if evento == pygame.K_RETURN:
            match self.pos_botao:
                case 0:
                    return("voltar")
                case _:
                    pass
        if self.voltar.destacado and pygame.mouse.get_pressed()[0]:
            return("voltar")
    
    def draw(self):
        super().draw()
        self.display.blit(self.nome, self.nome_rect)

    def volume_efeitos(self, novo_volume):
        for botao in self.botoes:
            botao.som.set_volume(novo_volume)
