import unittest
from unittest.mock import patch, MagicMock
from veiculos import Veiculo  # Supondo que o código do veículo está no arquivo `veiculo.py`
from tiro import Tiro  # Mockado nos testes

class TestVeiculo(unittest.TestCase):

    def test_disparar(self):
        # Configuração
        largura_tela, altura_tela = 800, 600
        veiculo = Veiculo(
            "caminho_fake.png", 100, 100, largura_tela, altura_tela, 50,
            {'esquerda': 0, 'direita': 0, 'cima': 0, 'baixo': 0}, False
        )
        veiculo.intervalo_tiro = 0  # Sem delay para facilitar o teste

        with patch('time.time', return_value=1000):
            veiculo.disparar()

        # Verificação
        self.assertEqual(len(veiculo.tiros), 1)
        tiro = veiculo.tiros[0]
        self.assertEqual(tiro.x, 125)  # Centro do veículo
        self.assertEqual(tiro.y, 125)
        self.assertEqual(tiro.angulo, 0)

    def test_atualizar_tiros(self):
        # Configuração
        largura_tela, altura_tela = 800, 600
        veiculo = Veiculo(
            "caminho_fake.png", 100, 100, largura_tela, altura_tela, 50,
            {'esquerda': 0, 'direita': 0, 'cima': 0, 'baixo': 0}, False
        )

        mock_tiro = MagicMock()
        mock_tiro.x = 900  # Fora da tela
        mock_tiro.y = 100
        veiculo.tiros = [mock_tiro]

        # Execução
        veiculo.atualizar_tiros()

        # Verificação
        self.assertEqual(len(veiculo.tiros), 0)

    @patch('pygame.key.get_pressed')
    def test_processar_movimento(self, mock_get_pressed):
        # Configuração
        largura_tela, altura_tela = 800, 600
        veiculo = Veiculo(
            "caminho_fake.png", 100, 100, largura_tela, altura_tela, 50,
            {'esquerda': 0, 'direita': 1, 'cima': 2, 'baixo': 3}, False
        )

        keys = [False] * 300
        keys[1] = True  # Simula tecla "direita" pressionada
        mock_get_pressed.return_value = keys

        # Execução
        veiculo.processar_movimento(keys)

        # Verificação
        self.assertEqual(veiculo.x, 110)  # 100 + 10 (velocidade)

    def test_rotacionar(self):
        # Configuração
        largura_tela, altura_tela = 800, 600
        veiculo = Veiculo(
            "caminho_fake.png", 100, 100, largura_tela, altura_tela, 50,
            {'rotacao_anti_horaria': 4, 'rotacao_horaria': 5}, False
        )

        keys = [False] * 300
        keys[4] = True  # Simula tecla "rotacao_anti_horaria" pressionada

        with patch('pygame.key.get_pressed', return_value=keys):
            veiculo.rotacionar()

        # Verificação
        self.assertEqual(veiculo.angulo, 3)

        # Simula tecla "rotacao_horaria" pressionada
        keys[4] = False
        keys[5] = True

        with patch('pygame.key.get_pressed', return_value=keys):
            veiculo.rotacionar()

        # Verificação
        self.assertEqual(veiculo.angulo, 0)  # 3 - 3

if __name__ == '__main__':
    unittest.main()
