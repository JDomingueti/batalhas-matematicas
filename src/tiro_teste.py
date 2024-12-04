import unittest
from tiro import Tiro
import math

class TestTiro(unittest.TestCase):

    def test_init(self):
        # Testa a inicialização do objeto
        tiro = Tiro(100, 200, 45, 10, (255, 0, 0), 10)
        self.assertEqual(tiro.x, 100)
        self.assertEqual(tiro.y, 200)
        self.assertEqual(tiro.angulo, 45)
        self.assertEqual(tiro.velocidade, 10)
        self.assertEqual(tiro.cor, (255, 0, 0))
        self.assertEqual(tiro.dano_tiro, 10)
        self.assertTrue(tiro.ativo)

    def test_mover(self):
        # Testa o movimento com base no ângulo e na velocidade
        tiro = Tiro(0, 0, 0, 10)  # Movimento na direção horizontal positiva
        tiro.mover()
        self.assertAlmostEqual(tiro.x, 10)
        self.assertAlmostEqual(tiro.y, 0)

        tiro = Tiro(0, 0, 90, 10)  # Movimento na direção vertical negativa (para cima)
        tiro.mover()
        self.assertAlmostEqual(tiro.x, 0)
        self.assertAlmostEqual(tiro.y, -10)

        tiro = Tiro(0, 0, 45, math.sqrt(2) * 10)  # Movimento diagonal
        tiro.mover()
        self.assertAlmostEqual(tiro.x, 10, places=5)
        self.assertAlmostEqual(tiro.y, -10, places=5)

    def test_mover_variacoes(self):
        # Testa o movimento em ângulos variados
        tiro = Tiro(100, 100, 180, 10)  # Movimento horizontal negativo (para a esquerda)
        tiro.mover()
        self.assertAlmostEqual(tiro.x, 90)
        self.assertAlmostEqual(tiro.y, 100)

        tiro = Tiro(100, 100, 270, 10)  # Movimento vertical positivo (para baixo)
        tiro.mover()
        self.assertAlmostEqual(tiro.x, 100)
        self.assertAlmostEqual(tiro.y, 110)

if __name__ == '__main__':
    unittest.main()
