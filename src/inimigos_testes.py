import unittest
from unittest.mock import MagicMock
import pygame
from inimigos import Inimigo1, Inimigo2, Inimigo3, Inimigo4  # Importando as subclasses

class TestInimigo(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.largura_tela = 800
        self.altura_tela = 600
        self.tamanho = 50
        self.path_image = "../assets/inimigos/inimigo1_deserto.png"
        self.powerup_image = "../assets/poderes/dano.png"
        self.powerup_efeito = "dano"
        
        # Mock do veículo
        self.veiculo = MagicMock()
        self.veiculo.x = 400
        self.veiculo.y = 300
        self.veiculo.dano = 2

        self.veiculos = [self.veiculo]

        # Instância de Inimigo1
        self.inimigo = Inimigo1(
            self.path_image, 
            x=100, 
            largura_tela=self.largura_tela, 
            altura_tela=self.altura_tela, 
            tamanho=self.tamanho, 
            powerup_img=self.powerup_image, 
            powerup_efeito=self.powerup_efeito
        )

    def test_perseguir_veiculo(self):
        # Verifica se o inimigo se move na direção do veículo
        posicao_original = (self.inimigo.rect.x, self.inimigo.rect.y)
        self.inimigo.perseguir_veiculo(self.veiculos)
        posicao_nova = (self.inimigo.rect.x, self.inimigo.rect.y)
        self.assertNotEqual(posicao_original, posicao_nova)

    def test_disparar(self):
        # Testa se o inimigo adiciona tiros
        self.inimigo.disparar(self.veiculos)
        self.assertGreaterEqual(len(self.inimigo.tiros), 1)

    def test_atualizar_tiros(self):
        # Testa se os tiros fora da tela são removidos
        tiro_mock = MagicMock()
        tiro_mock.x = -10  # Fora da tela
        tiro_mock.y = 300
        self.inimigo.tiros = [tiro_mock]
        self.inimigo.atualizar_tiros()
        self.assertEqual(len(self.inimigo.tiros), 0)

    def test_colisao(self):
        # Testa se uma colisão reduz a integridade do inimigo
        powerups = []
        tiro_mock = MagicMock()
        tiro_mock.x = self.inimigo.rect.x
        tiro_mock.y = self.inimigo.rect.y
        tiro_mock.raio = 5

        resultado = self.inimigo.colisao(tiro_mock, self.veiculos[0], powerups)
        self.assertTrue(resultado)
        self.assertLess(self.inimigo.integridade, 10)

    def test_update(self):
        # Testa o método update chamando seus métodos internos
        powerups = []
        tiros = []
        self.inimigo.update(tiros, self.veiculos, powerups)

        # Verifica se os métodos foram chamados
        self.assertGreaterEqual(len(self.inimigo.tiros), 1)
        self.assertNotEqual((self.inimigo.rect.x, self.inimigo.rect.y), (100, 50))

if __name__ == "__main__":
    unittest.main()
