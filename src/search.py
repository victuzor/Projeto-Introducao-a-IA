from collections import deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional, Tuple

from src.actions import get_valid_moves
from src.agent import calcular_penalidade_celula
from src.dungeon import FRAGILE_WALL, Grid, Position, get_cell


Caminho = Tuple[Position, ...]

CUSTO_MOVIMENTO_PADRAO = 1
CUSTO_QUEBRAR_PAREDE_FRAGIL = 5


@dataclass(frozen=True)
class ResultadoBusca:
    """
    Guarda o resultado de um algoritmo de busca.
    """

    encontrou: bool
    caminho: Caminho
    custo: int
    nos_expandidos: int


def calcular_custo_movimento(grid: Grid, posicao_destino: Position) -> int:
    """
    Calcula o custo de entrar em uma célula.

    Custo básico:
    - Todo movimento custa 1.

    Custos extras:
    - Entrar em slime ou esqueleto adiciona penalidade.
    - Entrar em parede frágil adiciona custo extra, simulando o esforço de quebrá-la.
    """
    celula = get_cell(grid, posicao_destino)

    custo = CUSTO_MOVIMENTO_PADRAO
    custo += calcular_penalidade_celula(celula)

    if celula == FRAGILE_WALL:
        custo += CUSTO_QUEBRAR_PAREDE_FRAGIL

    return custo


def busca_bfs(
    grid: Grid,
    posicao_inicial: Position,
    posicao_objetivo: Position,
    picareta_melhorada: bool = False,
) -> ResultadoBusca:
    """
    Executa BFS para encontrar o menor caminho em quantidade de passos.

    O BFS ignora diferenças de custo entre células.
    Ele considera apenas a quantidade de movimentos necessários.
    """
    fila = deque()
    visitados = set()

    fila.append((posicao_inicial, (posicao_inicial,)))
    visitados.add(posicao_inicial)

    nos_expandidos = 0

    while fila:
        posicao_atual, caminho_atual = fila.popleft()
        nos_expandidos += 1

        if posicao_atual == posicao_objetivo:
            custo = len(caminho_atual) - 1

            return ResultadoBusca(
                encontrou=True,
                caminho=caminho_atual,
                custo=custo,
                nos_expandidos=nos_expandidos,
            )

        acoes_validas = get_valid_moves(
            grid,
            posicao_atual,
            picareta_melhorada=picareta_melhorada,
        )

        for _, proxima_posicao in acoes_validas:
            if proxima_posicao not in visitados:
                visitados.add(proxima_posicao)
                novo_caminho = caminho_atual + (proxima_posicao,)
                fila.append((proxima_posicao, novo_caminho))

    return ResultadoBusca(
        encontrou=False,
        caminho=(),
        custo=0,
        nos_expandidos=nos_expandidos,
    )


def busca_ucs(
    grid: Grid,
    posicao_inicial: Position,
    posicao_objetivo: Position,
    picareta_melhorada: bool = False,
) -> ResultadoBusca:
    """
    Executa UCS para encontrar o caminho de menor custo acumulado.

    Diferente do BFS, o UCS considera que algumas células são mais caras:
    slime, esqueleto e parede frágil.
    """
    fila_prioridade = []
    melhores_custos = {posicao_inicial: 0}

    contador = 0
    heappush(fila_prioridade, (0, contador, posicao_inicial, (posicao_inicial,)))

    nos_expandidos = 0

    while fila_prioridade:
        custo_atual, _, posicao_atual, caminho_atual = heappop(fila_prioridade)

        if custo_atual > melhores_custos.get(posicao_atual, float("inf")):
            continue

        nos_expandidos += 1

        if posicao_atual == posicao_objetivo:
            return ResultadoBusca(
                encontrou=True,
                caminho=caminho_atual,
                custo=custo_atual,
                nos_expandidos=nos_expandidos,
            )

        acoes_validas = get_valid_moves(
            grid,
            posicao_atual,
            picareta_melhorada=picareta_melhorada,
        )

        for _, proxima_posicao in acoes_validas:
            custo_movimento = calcular_custo_movimento(grid, proxima_posicao)
            novo_custo = custo_atual + custo_movimento

            if novo_custo < melhores_custos.get(proxima_posicao, float("inf")):
                melhores_custos[proxima_posicao] = novo_custo
                novo_caminho = caminho_atual + (proxima_posicao,)

                contador += 1
                heappush(
                    fila_prioridade,
                    (novo_custo, contador, proxima_posicao, novo_caminho),
                )

    return ResultadoBusca(
        encontrou=False,
        caminho=(),
        custo=0,
        nos_expandidos=nos_expandidos,
    )


def formatar_caminho(caminho: Caminho) -> str:
    """
    Formata um caminho para exibição no terminal.
    """
    if not caminho:
        return "Nenhum caminho encontrado."

    return " -> ".join(str(posicao) for posicao in caminho)


def obter_proxima_posicao(caminho: Caminho) -> Optional[Position]:
    """
    Retorna a próxima posição após a posição inicial.

    Se o caminho tiver apenas uma posição ou estiver vazio, retorna None.
    """
    if len(caminho) < 2:
        return None

    return caminho[1]