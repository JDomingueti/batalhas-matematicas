import unittest
from unittest.mock import Mock, patch
import time
from powerups import PowerUp

class TestPowerUp(unittest.TestCase):

    @patch('pygame.image.load')  # Mock para evitar dependências de gráficos
    @patch('pygame.transform.scale')  # Mock para evitar problemas com `pygame.transform`
    def test_init(self, mock_scale, mock_load):
        # Simula a inicialização e testa os atributos básicos
        mock_load.return_value = Mock()  # Retorna um mock de imagem
        mock_scale.return_value = Mock()  # Retorna um mock para a escala

        powerup = PowerUp("path/to/image.png", 100, 200, "velocidade", 50)
        self.assertEqual(powerup.x, 100)
        self.assertEqual(powerup.y, 200)
        self.assertEqual(powerup.tamanho, 50)
        self.assertEqual(powerup.efeito, "velocidade")
        self.assertEqual(powerup.tempo_vida, 5)
        self.assertTrue(time.time() - powerup.criado_em < 1)  # Criado recentemente
        self.assertIsNotNone(powerup.rect)

    def test_aplicar_efeito_velocidade(self):
        # Testa o efeito "velocidade"
        veiculo = Mock()
        veiculo.velocidade = 10
        powerup = PowerUp("path/to/image.png", 0, 0, "velocidade", 50)
        powerup.aplicar_efeito(veiculo)
        self.assertEqual(veiculo.velocidade, 12)

    def test_aplicar_efeito_vida(self):
        # Testa o efeito "vida"
        veiculo = Mock()
        veiculo.integridade = 80
        powerup = PowerUp("path/to/image.png", 0, 0, "vida", 50)
        powerup.aplicar_efeito(veiculo)
        self.assertEqual(veiculo.integridade, 100)

        veiculo.integridade = 50
        powerup.aplicar_efeito(veiculo)
        self.assertEqual(veiculo.integridade, 70)

    def test_aplicar_efeito_tiro(self):
        # Testa o efeito "tiro"
        veiculo = Mock()
        veiculo.velocidade_tiro = 15
        powerup = PowerUp("path/to/image.png", 0, 0, "tiro", 50)
        powerup.aplicar_efeito(veiculo)
        self.assertEqual(veiculo.velocidade_tiro, 20)

    def test_aplicar_efeito_dano(self):
        # Testa o efeito "dano"
        veiculo = Mock()
        veiculo.dano = 3
        powerup = PowerUp("path/to/image.png", 0, 0, "dano", 50)
        powerup.aplicar_efeito(veiculo)
        self.assertEqual(veiculo.dano, 4)

    def test_expirado(self):
        # Testa o comportamento de expiração
        powerup = PowerUp("path/to/image.png", 0, 0, "velocidade", 50)
        powerup.criado_em = time.time() - 6  # Simula criação há 6 segundos
        self.assertTrue(powerup.expirado())

        powerup.criado_em = time.time()  # Criado agora
        self.assertFalse(powerup.expirado())

if __name__ == '__main__':
    unittest.main()
