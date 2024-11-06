import pygame, sys, telas
from typing import List
# import jogo, veiculos

# TODO: Estilizar

class GerenciadorTelas:
    def __init__(self, largura, altura, cor):
        pygame.init()
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.volume_efeitos = 0.1
        self.display = telas.inicio(self.largura, self.altura, self.cor, self.volume_efeitos, "fundo_inicio.png")
        self.musica = pygame.mixer.Sound("../assets/musica_menu.mp3")
        self.musica.set_volume(0.2)
        self.rodando = True
        self.estado = 'Menu'
        self.relogio = pygame.time.Clock()
    
    def run(self):
        pygame.mixer.Sound.play(self.musica, -1)
        tempo_press = pygame.time.get_ticks()
        while (self.rodando):
            if (self.estado == 'Menu'):
                events: List[pygame.event.Event] = pygame.event.get()
                for event in events:
                    res = self.display.checar_eventos()
                    self.interagir(res)
                    if (event.type == pygame.QUIT):
                        pygame.quit()
                        sys.exit()
                            
                teclas_pressionadas = pygame.key.get_pressed()

                if teclas_pressionadas[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
                teclado = [pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN]
                for item in teclado:
                    if (pygame.time.get_ticks() - tempo_press) > 300:
                        if teclas_pressionadas[item]:
                            tempo_press = pygame.time.get_ticks()
                            res = self.display.mover_no_teclado(item)
                            self.interagir(res)
                
                self.display.atualizar()
                self.display.draw()
            
            # elif (self.estado == 'jogando'):
            #     events: List[pygame.event.Event] = pygame.event.get()
            #     for event in events:
            #         if (event.type == pygame.QUIT):
            #             pygame.quit()
            #             sys.exit()
            #     teclas_pressionadas = pygame.key.get_pressed()
            #     if teclas_pressionadas[pygame.K_ESCAPE]:
            #         pygame.quit()
            #         sys.exit()
            #     self.display.draw()
            #     self.veiculo1.processar_movimento(teclas_pressionadas)
            #     self.veiculo1.draw(self.display.display)
            #     self.veiculo1.mostrar_integridade(self.display.display, (50, 50))
            #     self.display.atualizar()
                
            self.relogio.tick(60)
        pygame.quit()

    def interagir(self, res):
        match res:
            case 'selecao':
                self.display = telas.seletor_jogo(self.largura, self.altura, self.cor, self.volume_efeitos)
            # case 'jogar':
            # case 'selecao':
            #     self.display = jogo.espaco(self.largura, self.altura, self.cor, self.musica.get_volume(), self.volume_efeitos)
            #     self.estado = "jogando"
            case 'opcoes':
                self.display = telas.opcoes(self.largura, self.altura, self.cor, self.musica.get_volume(), self.volume_efeitos)
            case 'voltar':
                self.display = telas.inicio(self.largura, self.altura, self.cor, self.volume_efeitos, "fundo_inicio.png")
            case 'efeitos':
                self.display.volume_efeitos(self.display.atualizar_efeitos())
                self.volume_efeitos = self.display.atualizar_efeitos()
            case 'musica':
                self.musica.set_volume(self.display.atualizar_musica())
            case _:
                pass
         
if (__name__ == "__main__"):
    Jogo = GerenciadorTelas(800, 600, (0,0,0))
    Jogo.run()
    pygame.quit()
    sys.exit()