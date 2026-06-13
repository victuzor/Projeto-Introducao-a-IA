from collections import deque
from dataclasses import dataclass
from typing import Optional, Tuple

from src.actions import get_valid_moves
from src.dungeon import Grid, Position


Caminho = Tuple[Position, ...]


@dataclass(frozen=True)
class ResultadoBusca:
    """
    Guarda o resultado de um algoritmo de busca.
    """

    encontrou: bool
    caminho: Caminho
    custo: int
    nos_expandidos: int


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