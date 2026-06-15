# uAI Dungeon Miner

Projeto desenvolvido para a disciplina de **Introdução à Inteligência Artificial**, com o objetivo de comparar algoritmos de busca em um ambiente parcialmente observável inspirado no **Mundo de Wumpus**.

O projeto simula um agente minerador dentro de uma dungeon 8x8. O agente precisa coletar minérios, evitar riscos, lidar com paredes e atualizar seu conhecimento conforme explora o ambiente.

---

## Objetivo do projeto

O objetivo é comparar o comportamento de três algoritmos de busca:

* **BFS** — Busca em Largura;
* **UCS** — Busca de Custo Uniforme;
* **A*** — Busca A Estrela.

Esses algoritmos são aplicados em um problema de navegação, coleta de recursos e tomada de decisão em ambiente com conhecimento parcial.

O agente não conhece todo o mapa desde o início. Ele possui apenas uma **bússola de minérios**, que informa onde estão os minérios, mas não revela paredes, slimes ou esqueletos.

---

## Ideia geral

O agente está em uma dungeon 8x8 e precisa coletar minérios para maximizar seu score.

Durante a exploração, ele encontra:

* minérios com valores diferentes;
* paredes comuns;
* paredes frágeis;
* slimes;
* esqueletos;
* percepções de risco, como gosma e crack.

O agente atualiza um **mapa mental** conforme anda pelo mundo. Esse mapa mental representa aquilo que o agente sabe ou suspeita sobre o ambiente.

---

## Representação do mundo

| Símbolo | Significado                          |
| ------- | ------------------------------------ |
| `A`     | Agente                               |
| `.`     | Célula livre                         |
| `?`     | Célula desconhecida no mapa mental   |
| `#`     | Parede comum                         |
| `X`     | Parede frágil                        |
| `Fe`    | Ferro                                |
| `Cu`    | Cobre                                |
| `Au`    | Ouro                                 |
| `S`     | Slime                                |
| `E`     | Esqueleto                            |
| `*`     | Caminho planejado ou percorrido      |
| `S?`    | Suspeita de slime no mapa mental     |
| `E?`    | Suspeita de esqueleto no mapa mental |
| `!?`    | Suspeita de slime ou esqueleto       |
| `G`     | Gosma próxima no mapa de percepções  |
| `C`     | Crack próximo no mapa de percepções  |
| `GC`    | Gosma e crack na mesma célula        |

---

## Minérios

Os minérios possuem valores diferentes:

| Minério | Valor |
| ------- | ----: |
| `Fe`    |    10 |
| `Cu`    |    20 |
| `Au`    |    50 |

Além de valer pontos, o ferro também pode ser usado para melhorar a picareta.

---

## Paredes e picareta

Existem dois tipos de paredes:

| Símbolo | Tipo          |
| ------- | ------------- |
| `#`     | Parede comum  |
| `X`     | Parede frágil |

A parede comum bloqueia o caminho.

A parede frágil pode ser atravessada se o agente tiver ferro suficiente para melhorar a picareta. O agente não melhora a picareta automaticamente ao coletar ferro. Ele guarda o ferro e só melhora a picareta quando realmente precisa atravessar uma parede frágil.

---

## Monstros e penalidades

O ambiente possui dois tipos de monstros:

| Monstro         | Penalidade |
| --------------- | ---------: |
| `S` — Slime     |         30 |
| `E` — Esqueleto |         40 |

Se o agente pisa em uma célula com monstro, ele sofre a penalidade correspondente. Depois disso, o monstro passa a ser conhecido no mapa mental e o agente evita passar por aquela célula novamente.

---

## Percepções

O agente não sabe inicialmente onde estão os monstros. Ele descobre riscos por meio de percepções.

| Percepção   | Significado                                  |
| ----------- | -------------------------------------------- |
| `G` — gosma | existe um slime em alguma célula vizinha     |
| `C` — crack | existe um esqueleto em alguma célula vizinha |

Essas percepções não indicam exatamente onde está o monstro. Elas apenas permitem criar hipóteses.

Por exemplo, se o agente sente gosma em uma posição, ele sabe que pode existir um slime em alguma das casas vizinhas. Então ele marca os vizinhos desconhecidos como `S?`.

Se depois o agente anda para outra posição e não sente gosma, ele pode eliminar algumas suspeitas.

---

## Mapa mental

O mapa mental representa o conhecimento parcial do agente.

Inicialmente, o agente sabe apenas:

* sua posição inicial;
* os limites do mapa;
* a posição dos minérios, por causa da bússola.

Inicialmente, o agente não sabe:

* onde estão as paredes;
* onde estão as paredes frágeis;
* onde estão os slimes;
* onde estão os esqueletos.

Conforme ele anda, o mapa mental é atualizado:

* paredes adjacentes são descobertas;
* percepções de gosma e crack geram suspeitas;
* ausência de percepção remove suspeitas;
* monstros pisados passam a ser conhecidos;
* células visitadas são marcadas como conhecidas.

Essa lógica torna o problema mais próximo de um ambiente parcialmente observável.

---

## Algoritmos implementados

### BFS — Busca em Largura

O BFS busca o caminho com menor quantidade de passos.

Características:

* ignora custos diferentes;
* não considera risco;
* não considera penalidade no planejamento;
* serve como algoritmo base de comparação.

Na prática, o BFS pode passar por áreas perigosas, porque seu objetivo principal é minimizar passos.

---

### UCS — Busca de Custo Uniforme

O UCS busca o caminho de menor custo acumulado.

Ele considera:

* custo de movimento;
* custo de paredes frágeis;
* custo de células desconhecidas;
* custo de suspeitas no mapa mental;
* penalidades quando já conhecidas no planejamento.

O UCS tende a evitar áreas suspeitas, mesmo que o caminho seja mais longo.

---

### A* — Busca A Estrela

O A* combina custo acumulado com uma heurística.

A função usada é:

```text
f(n) = g(n) + h(n)
```

Onde:

* `g(n)` é o custo acumulado até o estado atual;
* `h(n)` é a distância de Manhattan até o objetivo.

A heurística usada é a distância de Manhattan:

```text
h(n) = |linha_atual - linha_objetivo| + |coluna_atual - coluna_objetivo|
```

O A* tende a encontrar rotas boas com menor custo computacional, pois usa a heurística para direcionar a busca.

---

## Replanejamento

O agente não calcula uma rota completa e segue cegamente até o fim.

A lógica usada é:

1. escolhe um minério como alvo;
2. planeja uma rota com base no mapa mental atual;
3. anda um passo;
4. recebe novas percepções;
5. atualiza o mapa mental;
6. replana a rota;
7. repete o processo.

Isso permite que o agente reaja a novas informações, como paredes descobertas ou suspeitas de monstros.

---

## Score

O score final do agente é calculado considerando:

```text
score = dinheiro - custo_passos - penalidades - custo_risco
```

Onde:

* `dinheiro` é o valor total dos minérios coletados;
* `custo_passos` representa o custo de deslocamento;
* `penalidades` representam danos causados por monstros;
* `custo_risco` representa o custo de passar por regiões perigosas ou suspeitas.

---

## Métricas computacionais

Além do score da missão, o projeto também mede o custo computacional dos algoritmos.

As principais métricas são:

| Métrica               | Significado                                       |
| --------------------- | ------------------------------------------------- |
| Nós expandidos        | Quantidade de estados avaliados pelo algoritmo    |
| Replanejamentos       | Quantas vezes o agente precisou recalcular a rota |
| Tempo de planejamento | Tempo gasto planejando rotas                      |
| Custo planejado       | Soma dos custos das rotas planejadas              |
| Score final           | Resultado final da missão                         |

Essas métricas ajudam a comparar UCS e A*, mesmo quando os dois alcançam scores parecidos.

---

## Geração de mundos

O projeto possui geração de mundos por número.

Cada número de mundo funciona como uma seed. Isso significa que o mesmo número sempre gera o mesmo mapa.

O intervalo disponível é:

```text
1 até 42
```

Exemplos:

```bash
python main.py --mundo 1
python main.py --mundo 7
python main.py --mundo 42
```

Também é possível executar sem escolher um mundo específico:

```bash
python main.py
```

Nesse caso, o programa escolhe aleatoriamente um mundo entre 1 e 42.

---

## Como executar

### 1. Criar ambiente virtual

No Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

No Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

---

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 3. Executar a simulação

Executar com mundo aleatório:

```bash
python main.py
```

Executar com mundo específico:

```bash
python main.py --mundo 42
```

Executar mais rápido:

```bash
python main.py --mundo 42 --delay 0.2
```

Limitar a quantidade de iterações:

```bash
python main.py --mundo 42 --max-iteracoes 100
```

---

## Como executar os testes

```bash
pytest
```

Os testes verificam:

* criação da dungeon;
* ações válidas;
* estado do agente;
* cálculo de score;
* algoritmos de busca;
* planejamento de rotas;
* mapa mental;
* geração de mundos;
* simulação comparativa.

---

## Estrutura do projeto

```text
.
├── main.py
├── requirements.txt
├── pytest.ini
├── README.md
├── src
│   ├── actions.py
│   ├── agent.py
│   ├── comparison.py
│   ├── dungeon.py
│   ├── mental_map.py
│   ├── mission.py
│   ├── multisimulation.py
│   ├── planner.py
│   ├── render.py
│   ├── risk.py
│   ├── score.py
│   ├── search.py
│   ├── simulation.py
│   └── worlds.py
└── tests
    ├── test_actions.py
    ├── test_agent.py
    ├── test_comparison.py
    ├── test_dungeon.py
    ├── test_mental_map.py
    ├── test_mission.py
    ├── test_multisimulation.py
    ├── test_planner.py
    ├── test_render.py
    ├── test_score.py
    ├── test_search.py
    ├── test_simulation.py
    ├── test_state.py
    └── test_worlds.py
```

---

## Diferença esperada entre os algoritmos

### BFS

O BFS tende a encontrar caminhos curtos, mas pode ignorar riscos.

Resultado esperado:

* pode andar menos;
* pode cair mais em monstros;
* pode ter score menor;
* expande estados de forma simples.

---

### UCS

O UCS tende a evitar riscos porque considera custos.

Resultado esperado:

* evita células suspeitas;
* pode andar mais para fugir de perigo;
* pode obter score melhor que o BFS;
* pode expandir muitos nós.

---

### A*

O A* também considera custos, mas usa uma heurística para se orientar.

Resultado esperado:

* evita riscos como o UCS;
* tende a ser mais eficiente computacionalmente;
* pode alcançar score parecido com UCS;
* normalmente expande menos nós que UCS.

---

## Exemplo de explicação para apresentação

O projeto simula um agente minerador em uma dungeon 8x8. O agente possui uma bússola que revela a posição dos minérios, mas ele não conhece o ambiente completo. Ele precisa explorar o mapa, descobrir paredes e lidar com sinais de perigo.

As percepções são inspiradas no Mundo de Wumpus. Quando o agente sente gosma, ele sabe que pode haver um slime em alguma célula vizinha. Quando sente crack, ele sabe que pode haver um esqueleto por perto. Com essas informações, o agente atualiza seu mapa mental.

A cada passo, o agente replana sua rota usando BFS, UCS ou A*. O BFS busca o menor caminho em passos, enquanto o UCS busca o menor custo. Já o A* combina custo acumulado com uma heurística de distância até o alvo.

A comparação entre os algoritmos é feita usando score, penalidades, passos, nós expandidos, tempo de planejamento e número de replanejamentos.

---

## Conclusão

O projeto demonstra como algoritmos clássicos de busca podem ser aplicados em um ambiente parcialmente observável.

A principal diferença entre os algoritmos aparece na forma como eles lidam com custo, risco e eficiência computacional.

O BFS funciona como uma estratégia simples baseada em menor caminho. O UCS melhora a tomada de decisão ao considerar custos. O A* usa uma heurística para buscar soluções de forma mais direcionada.

Com o mapa mental, o agente deixa de ter conhecimento completo do ambiente e passa a tomar decisões com base em percepções, hipóteses e replanejamento.
