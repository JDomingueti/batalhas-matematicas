import unittest
from unittest.mock import MagicMock, patch
from inimigos import Inimigo, Inimigo1, Inimigo2, Inimigo3, Inimigo4
from tiro import Tiro
from powerups import PowerUp

class TestInimigo(unittest.TestCase):

    @patch("pygame.image.load")
    @patch("pygame.Surface")
    def setUp(self, mock_surface, mock_load):
        mock_load.return_value = mock_surface
        self.mock_powerup_image = "mock_powerup.png"
        self.mock_effect = "vida"
        self.inimigo = Inimigo1(
            path_image="mock_path.png", 
            x=100, 
            largura_tela=800, 
            altura_tela=600, 
            tamanho=50, 
            powerup_img=self.mock_powerup_image, 
            powerup_efeito=self.mock_effect
        )

    def test_initialization(self):
        self.assertEqual(self.inimigo.rect.x, 100)
        self.assertEqual(self.inimigo.rect.y, 50)
        self.assertEqual(self.inimigo.integridade, 10)
        self.assertEqual(self.inimigo.powerup_efeito, "vida")

    @patch("pygame.Vector2")
    def test_perseguir_veiculo(self, mock_vector):
        veiculo_mock = MagicMock(x=200, y=300)
        mock_vector.return_value.distance_to.return_value = 300
        self.inimigo.perseguir_veiculo([veiculo_mock])

        mock_vector.assert_called_with(200 - self.inimigo.rect.x, 300 - self.inimigo.rect.y)

    @patch("time.time", return_value=10)
    def test_disparar(self, mock_time):
        veiculo_mock = MagicMock(x=200, y=300)
        self.inimigo.disparar([veiculo_mock])

        self.assertEqual(len(self.inimigo.tiros), 1)
        tiro = self.inimigo.tiros[0]
        self.assertIsInstance(tiro, Tiro)

    @patch("pygame.Rect.colliderect", return_value=True)
    def test_colisao(self, mock_colliderect):
        tiro_mock = MagicMock(x=100, y=100, raio=5)
        powerups = []

        self.inimigo.colisao(tiro_mock, MagicMock(dano=5), powerups)
        self.assertEqual(self.inimigo.integridade, 5)
        self.assertEqual(len(powerups), 0)

        # Simula destruição do inimigo
        self.inimigo.integridade = 0
        self.inimigo.colisao(tiro_mock, MagicMock(dano=5), powerups)
        self.assertEqual(len(powerups), 1)
        self.assertIsInstance(powerups[0], PowerUp)

    def test_atualizar_tiros(self):
        tiro_mock = MagicMock(x=400, y=300)
        self.inimigo.tiros.append(tiro_mock)
        self.inimigo.atualizar_tiros()

        tiro_mock.mover.assert_called_once()

    def test_update_calls_methods(self):
        self.inimigo.perseguir_veiculo = MagicMock()
        self.inimigo.disparar = MagicMock()
        self.inimigo.atualizar_tiros = MagicMock()

        self.inimigo.update([], [], [])
        self.inimigo.perseguir_veiculo.assert_called_once()
        self.inimigo.disparar.assert_called_once()
        self.inimigo.atualizar_tiros.assert_called_once()

    def test_subclasses(self):
        inimigo2 = Inimigo2("mock_path.png", 100, 800, 600, 50, self.mock_powerup_image, "velocidade")
        inimigo3 = Inimigo3("mock_path.png", 100, 800, 600, 50, self.mock_powerup_image, "tiro")
        inimigo4 = Inimigo4("mock_path.png", 100, 800, 600, 50, self.mock_powerup_image, "dano")

        self.assertEqual(inimigo2.powerup_efeito, "velocidade")
        self.assertEqual(inimigo3.powerup_efeito, "tiro")
        self.assertEqual(inimigo4.powerup_efeito, "dano")

if __name__ == "__main__":
    unittest.main()
