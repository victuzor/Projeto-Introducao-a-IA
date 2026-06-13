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

    encontrou: bool
    caminho: Caminho
    custo: int
    nos_expandidos: int


def calcular_custo_movimento(grid: Grid, posicao_destino: Position) -> int:
    celula = get_cell(grid, posicao_destino)

    custo = CUSTO_MOVIMENTO_PADRAO
    custo += calcular_penalidade_celula(celula)

    if celula == FRAGILE_WALL:
        custo += CUSTO_QUEBRAR_PAREDE_FRAGIL

    return custo


def calcular_heuristica_manhattan(
    posicao_atual: Position,
    posicao_objetivo: Position,
) -> int:
    linha_atual, coluna_atual = posicao_atual
    linha_objetivo, coluna_objetivo = posicao_objetivo

    distancia_linhas = abs(linha_atual - linha_objetivo)
    distancia_colunas = abs(coluna_atual - coluna_objetivo)

    return distancia_linhas + distancia_colunas


def busca_bfs(
    grid: Grid,
    posicao_inicial: Position,
    posicao_objetivo: Position,
    picareta_melhorada: bool = False,
) -> ResultadoBusca:
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


def busca_a_estrela(
    grid: Grid,
    posicao_inicial: Position,
    posicao_objetivo: Position,
    picareta_melhorada: bool = False,
) -> ResultadoBusca:
    fila_prioridade = []
    melhores_custos = {posicao_inicial: 0}

    contador = 0
    prioridade_inicial = calcular_heuristica_manhattan(
        posicao_inicial,
        posicao_objetivo,
    )

    heappush(
        fila_prioridade,
        (prioridade_inicial, contador, 0, posicao_inicial, (posicao_inicial,)),
    )

    nos_expandidos = 0

    while fila_prioridade:
        _, _, custo_atual, posicao_atual, caminho_atual = heappop(fila_prioridade)

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

                heuristica = calcular_heuristica_manhattan(
                    proxima_posicao,
                    posicao_objetivo,
                )
                prioridade = novo_custo + heuristica

                contador += 1
                heappush(
                    fila_prioridade,
                    (
                        prioridade,
                        contador,
                        novo_custo,
                        proxima_posicao,
                        novo_caminho,
                    ),
                )

    return ResultadoBusca(
        encontrou=False,
        caminho=(),
        custo=0,
        nos_expandidos=nos_expandidos,
    )


def formatar_caminho(caminho: Caminho) -> str:
    if not caminho:
        return "Nenhum caminho encontrado."

    return " -> ".join(str(posicao) for posicao in caminho)


def obter_proxima_posicao(caminho: Caminho) -> Optional[Position]:
    if len(caminho) < 2:
        return None

    return caminho[1]