import pygame
import sys
import botao
from typing import List

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
        self.is_running = True
        self.clock = pygame.time.Clock()
    
    def run(self):
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
        self.botoes: List[botao.botao] = []
    
    def update(self):
        pygame.display.flip()

class inicio(tela):
    def __init__(self, largura, altura, cor):
        super().__init__(largura, altura, cor)
        pygame.display.set_caption("Inicio")
        self.fonte = pygame.font.SysFont("Terminal", 80)
        nome = self.fonte.render("Batalhas Matemáticas", False, "White")
        nome_rect = nome.get_rect(center = (self.largura//2, 50))
        self.display.blit(nome, nome_rect)
        self.jogar : botao.botao = botao.botao((self.largura//2, 250), "Jogar", "Terminal", 60, "White")
        self.opcoes : botao.botao = botao.botao((self.largura//2, 350), "Opções", "Terminal", 60, "White")
        self.sair : botao.botao = botao.botao((self.largura//2, 450), "Sair", "Terminal", 60, "White")
    
    def checar_eventos(self):
        if self.jogar.verificar_clique(pygame.mouse.get_pos()):
            return("jogar")
        if self.opcoes.verificar_clique(pygame.mouse.get_pos()):
            return("opcoes")
        if self.sair.verificar_clique(pygame.mouse.get_pos()):
            sair()

    def draw(self):
        self.jogar.display_botao(self.display)
        self.opcoes.display_botao(self.display)
        self.sair.display_botao(self.display)

class opcoes(tela):
    def __init__(self, largura, altura, cor):
        super().__init__(largura, altura, cor)
        pygame.display.set_caption("Opções")
        self.fonte = pygame.font.SysFont("Terminal", 80)
        nome = self.fonte.render("Opcoes", False, "White")
        nome_rect = nome.get_rect(center = (self.largura//2, 50))
        self.display.blit(nome, nome_rect)
        self.voltar : botao.botao = botao.botao((self.largura//2, 550), "Voltar", "Terminal", 40, "White")
        
    def checar_eventos(self):
        if self.voltar.verificar_clique(pygame.mouse.get_pos()):
            return("voltar")
    
    def draw(self):
        self.voltar.display_botao(self.display)

class seletor_jogo(tela):
    def __init__(self, largura, altura, cor):
        super().__init__(largura, altura, cor)
        pygame.display.set_caption("Seleção")
        self.fonte = pygame.font.SysFont("Terminal", 80)
        nome = self.fonte.render("Selecione o mapa", False, "White")
        nome_rect = nome.get_rect(center = (self.largura//2, 50))
        self.display.blit(nome, nome_rect)
        self.voltar : botao.botao = botao.botao((self.largura//2, 550), "Voltar", "Terminal", 40, "White")
        
    def checar_eventos(self):
        if self.voltar.verificar_clique(pygame.mouse.get_pos()):
            return("voltar")
    
    def draw(self):
        self.voltar.display_botao(self.display)


if (__name__ == "__main__"):
    Jogo = GameManager(800, 600, (0,0,0))
    Jogo.run()
    pygame.quit()
    sys.exit()