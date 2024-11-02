import pygame
import sys
from botao import Botao
from typing import List

# TODO: Agrupar os botões em listas e tentar pensar numa
# maneira mais eficaz de manipulá-los

# TODO: Implementar a movimentação no menu pelo teclado

# TODO: Estilizar

def sair():
    pygame.quit()
    sys.exit()

class GameManager:
    def __init__(self, largura, altura, cor):
        pygame.init()
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.display = inicio(self.largura, self.altura, self.cor)
        self.musica = pygame.mixer.Sound("../assets/musica_menu.mp3")
        self.musica.set_volume(0.1)
        self.is_running = True
        self.clock = pygame.time.Clock()
    
    def run(self):
        pygame.mixer.Sound.play(self.musica, -1)
        while (self.is_running):
            events: List[pygame.event.Event] = pygame.event.get()
            for event in events:
                if (event.type == pygame.QUIT):
                    sair()
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    res = self.display.checar_eventos()
                    match res:
                        case 'jogar':
                            self.display = seletor_jogo(self.largura, self.altura, self.cor)
                        case 'opcoes':
                            self.display = opcoes(self.largura, self.altura, self.cor)
                        case 'voltar':
                            self.display = inicio(self.largura, self.altura, self.cor)
                        case 'musica':
                            if self.musica.get_volume() != 0:
                                self.musica.set_volume(0)
                            else:
                                self.musica.set_volume(0.1)
                        case 'efeitos':
                            self.display.mutar()
                        case _:
                            pass

            key_map = pygame.key.get_pressed()

            if key_map[pygame.K_ESCAPE]:
                sair()
            
            self.display.update()
            self.display.draw()
            
            self.clock.tick(60)
        pygame.quit()

class tela:
    def __init__(self, largura, altura, cor):
        self.largura = largura
        self.altura = altura
        self.tamanho = (self.largura, self.altura)
        self.display = pygame.display.set_mode(self.tamanho)
        self.display.fill(cor)
        self.is_running = True
    
    def update(self):
        pygame.display.flip()

class inicio(tela):
    def __init__(self, largura, altura, cor):
        super().__init__(largura, altura, cor)

        pygame.display.set_caption("Inicio")
        
        self.fonte = pygame.font.SysFont("Terminal", self.largura // 10)
        
        self.nome = self.fonte.render("Batalhas Matemáticas", False, "White")
        self.nome_rect = self.nome.get_rect(center = (self.largura//2, self.altura//5))
        
        self.jogar : Botao = Botao((self.largura//2, 2*self.altura//5), "Jogar", "Terminal", altura//10, "White", (120,0,0))
        self.opcoes : Botao = Botao((self.largura//2, 3*self.altura//5), "Opções", "Terminal", altura//10, "White", (120,0,0))
        self.sair : Botao = Botao((self.largura//2, 4*self.altura//5), "Sair", "Terminal", altura//10, "White", (120,0,0))
    
    def checar_eventos(self):
        if self.jogar.destacado:
            return("jogar")
        if self.opcoes.destacado:
            return("opcoes")
        if self.sair.destacado:
            sair()

    def draw(self):
        self.display.fill((0,0,0))
        self.display.blit(self.nome, self.nome_rect)
        
        self.jogar.display_botao(self.display)
        self.opcoes.display_botao(self.display)
        self.sair.display_botao(self.display)

    def update(self):
        self.jogar.atualizar(self.display)
        self.opcoes.atualizar(self.display)
        self.sair.atualizar(self.display)
        
        pygame.display.flip()

    def mutar(self):
        if self.jogar.som.get_volume() != 0:
            self.jogar.som.set_volume(0)
            self.sair.som.set_volume(0)
            self.opcoes.som.set_volume(0)
        else:
            self.jogar.som.set_volume(0.3)
            self.sair.som.set_volume(0.3)
            self.opcoes.som.set_volume(0.3) 

class opcoes(tela):
    def __init__(self, largura, altura, cor):
        super().__init__(largura, altura, cor)
        pygame.display.set_caption("Opções")
        
        self.fonte = pygame.font.SysFont("Terminal", self.largura//10)
        self.nome = self.fonte.render("Opcões", False, "White")
        self.nome_rect = self.nome.get_rect(center = (self.largura//2, self.altura//5))
        
        self.voltar : Botao = Botao((self.largura//2, self.altura - self.altura//5), "Voltar", "Terminal", self.altura//15, "White", (120,0,0))
        self.musica : Botao = Botao((self.largura//2, 2*self.altura//5), "Música", "Terminal", self.altura//15, "White", (120,0,0))
        self.efeitos : Botao = Botao((self.largura//2, 3*self.altura//5), "Efeitos", "Terminal", self.altura//15, "White", (120,0,0))
        
    def checar_eventos(self):
        if self.voltar.destacado:
            return("voltar")
        if self.musica.destacado:
            return("musica")
        if self.efeitos.destacado:
            return("efeitos")
    
    def draw(self):
        self.display.fill((0,0,0))
        self.display.blit(self.nome, self.nome_rect)
        
        self.voltar.display_botao(self.display)
        self.musica.display_botao(self.display)
        self.efeitos.display_botao(self.display)
        
    def update(self):
        self.voltar.atualizar(self.display)
        self.musica.atualizar(self.display)
        self.efeitos.atualizar(self.display)
        
        pygame.display.flip()

    
    def mutar(self):
        if self.voltar.som.get_volume() != 0:
            self.voltar.som.set_volume(0)
            self.musica.som.set_volume(0)
            self.efeitos.som.set_volume(0)
        else:
            self.voltar.som.set_volume(0.3)
            self.musica.som.set_volume(0.3)
            self.efeitos.som.set_volume(0.3)

class seletor_jogo(tela):
    def __init__(self, largura, altura, cor):
        super().__init__(largura, altura, cor)
        
        pygame.display.set_caption("Seleção")
        self.fonte = pygame.font.SysFont("Terminal", self.largura//10)
        self.nome = self.fonte.render("Selecione o mapa", False, "White")
        self.nome_rect = self.nome.get_rect(center = (self.largura//2, self.altura//5))
        
        self.voltar : Botao = Botao((self.largura//2, self.altura - self.altura//5), "Voltar", "Terminal", self.altura//15, "White", (120,0,0))
        
    def checar_eventos(self):
        if self.voltar.destacado:
            return("voltar")
    
    def draw(self):
        self.display.fill((0,0,0))
        self.display.blit(self.nome, self.nome_rect)
        
        self.voltar.display_botao(self.display)
    
    def update(self):
        self.voltar.atualizar(self.display)
        pygame.display.flip()

    
    def mutar(self):
        if self.voltar.som.get_volume() != 0:
            self.voltar.som.set_volume(0)
        else:
            self.voltar.som.set_volume(0.3)

if (__name__ == "__main__"):
    Jogo = GameManager(800, 600, (0,0,0))
    Jogo.run()
    pygame.quit()
    sys.exit()