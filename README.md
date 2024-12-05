# Batalhas Matemáticas


## Fundação Getúlio Vargas - Matemática Aplicada  

**Autores:**  

- Jean Gabriel Domingueti  

- Rodrigo da Cruz Ribeiro  

- Eliane da Silva Moreira  


---


## Introdução


Este projeto descreve o desenvolvimento do jogo **Batalhas Matemáticas**, inspirado em
*Space Invaders*, um clássico jogo de tiro no qual o jogador controla um veículo e deve destruir inimigos enquanto desvia de seus ataques.



Ao longo do desenvolvimento, o jogo se distanciou da inspiração inicialf por conter dois jogadores que lutam um contra o outro, diferentes paisagens, inimigos e veículos, diversos obstáculos e muitos outros detalhes. Este documento descreve os principais aspectos
do desenvolvimento, incluindo a lógica do jogo, o design e a implementação.


---


## Processo de Desenvolvimento do Jogo


O desenvolvimento do jogo foi feito em **Python** utilizando a biblioteca 
*Pygame*, aplicando conceitos de orientação a objetos. O projeto contou com a abordagem de diferentes elementos, funções e implementações. Segue um breve resumo de cada tópico trabalhado.


### Design


Inicialmente, três cenários foram projetados: deserto, oceano e espaço. Cada cenário possui sprites específicos, como veículos e inimigos, além de power-ups gerados após a destruição dos inimigos. Ao todo, há 4 tipos de power-ups: vida, velocidade, dano e tiro.
Tente coletá-los antes que expirem!


Os sons do Tubarão que aparece de vez em quando na tela do oceano é um trecho da trilha do filme Tubarão, o som do Verme da Areia que aprece no deserto foi retirado do jogo Terraria e as músicas de fundo foram retiradas do jogo Stardew Valley. Os links para
outros sons utilizados serão citados no final.


### Implementações Principais


O jogo foi desenvolvido com diversos módulos, cada um abordando uma parte do jogo, como veículos, inimigos, power-ups, tiros, telas e botões. As funções principais incluem:


- **Veículos:** podem ser melhorados com os power-ups;

- **Inimigos:** possuem uma IA simples para perseguir os veículos;

- **Tela:** apresenta obstáculos ao longo do jogo;

- **Unittests:** verificam se os módulos principais funcionam corretamente.


### Controles dos Jogadores


Os dois jogadores podem se mover, rotacionar e disparar contra os inimigos (cuidado, os inimigos também podem atacar você!). As teclas de controle são:


#### Jogador 1:

- **a**: Mover para a esquerda

- **d**: Mover para a direita

- **w**: Mover para cima

- **s**: Mover para baixo

- **c**: Rotação anti-horária

- **v**: Rotação horária

- **b**: Disparo


#### Jogador 2:

- **LEFT**: Mover para a esquerda

- **RIGHT**: Mover para a direita

- **UP**: Mover para cima

- **DOWN**: Mover para baixo

- **COMMA**: Rotação anti-horária

- **PERIOD**: Rotação horária

- **SEMICOLON**: Disparo


### Divisão de Tarefas


O desenvolvimento foi dividido entre os membros da equipe da seguinte maneira:

- **Eliane Moreira:** Funcionalidades básicas dos veículos, inimigos e power-ups.

- **Rodrigo Ribeiro:** Rotação, disparo e melhorias das funcionalidades básicas.

- **Jean Domingueti:** Design, obstáculos, colisão e estruturação principal do jogo.


### Dificuldades Enfrentadas


Algumas dificuldades enfrentadas durante o desenvolvimento foram:

- **Implementação dos limites:** Ajustes nas colisões para garantir que veículos e inimigos não saiam dos limites da tela.

- **Implementação da rotação e dos tiros:** Realizar os cálculos matemáticas para garantir que o ângulo em que a nave está apontando é correto, disparo do tiro a partir desta direção se certificando que o módulo do seu vetor velocidade se mantém constante
e fazer com que ao um inimigo morrer os seus tiros já disparados continuem na tela. Para resolver os desafios foram utilizadas as funções
*cos* e *sin* da biblioteca **math** e a criação de uma lista geral que guarda todos os tiros dos inimigos.



### Como Rodar o Projeto

Clone esse repositório, navegue até o diretório do jogo e execute os passos a seguir.


- Crie um ambiente virtual utilizando o comando:

```

python -m venv venv

```


- Ative o ambiente virtual


No Windows:

```

venv\Scripts\activate

```

No Unix ou MacOS:

```

source venv/bin/activate

```


- Para instalar os pacotes necessários execute:

```

pip install -r requirements.txt

```


- Para verificar os unittests execute:

```

cd src/tests.py

```


- Para iniciar o jogo execute:

```

cd src/main.py

```


Divirta-se!


---


## Conclusão


O desenvolvimento do jogo **Batalhas Matemáticas** foi desafiador e enriquecedor, proporcionando uma excelente oportunidade para melhorar o conhecimento na área de planejamento e criação de jogos.


**Data:** Dezembro de 2024


## Links


- Som explosão - (0:21): [YouTube - Som Explosão](https://www.youtube.com/watch?v=jajIP4m6HfU)

- Crab rave - (1:10): [YouTube - Crab Rave](https://www.youtube.com/watch?v=cE0wfjsybIQ)

- Águas vivas: [Pixabay - Águas Vivas](https://pixabay.com/pt/sound-effects/funny-bubbles-96203/)

- Bola de vento: [Pixabay - Bola de Vento](https://pixabay.com/pt/sound-effects/wind-91882/)

- Gafanhotos: [Pixabay - Gafanhotos](https://pixabay.com/pt/sound-effects/criquet-2-72941/)

- Space: [YouTube - Space](https://www.youtube.com/watch?v=TQ-Fv7bbJgM)

- Cometa: [Pixabay - Cometa](https://pixabay.com/sound-effects/fireball-whoosh-7-201453/)

- Laser inimigos: [Pixabay - Laser Inimigos](https://pixabay.com/pt/sound-effects/laser-14792/)

- Laser player: [Pixabay - Laser Player](https://pixabay.com/pt/sound-effects/laser-104024/)
