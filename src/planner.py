from dataclasses import dataclass
from typing import Callable, Optional, Tuple

from src.dungeon import Grid, Position, get_cell, get_ore_value, is_ore
from src.search import ResultadoBusca, busca_a_estrela, busca_bfs, busca_ucs


Minerios = Tuple[Position, ...]


@dataclass(frozen=True)
class PlanoRota:

    alvo: Position
    valor_alvo: int
    resultado_busca: ResultadoBusca
    utilidade_estimada: int


def localizar_minerios(grid: Grid) -> Minerios:
    minerios = []

    for linha_indice, linha in enumerate(grid):
        for coluna_indice, celula in enumerate(linha):
            if is_ore(celula):
                minerios.append((linha_indice, coluna_indice))

    return tuple(minerios)


def calcular_utilidade_rota(valor_alvo: int, custo_rota: int) -> int:
    return valor_alvo - custo_rota


def obter_algoritmo_busca(algoritmo: str) -> Callable:
    if algoritmo == "bfs":
        return busca_bfs

    if algoritmo == "ucs":
        return busca_ucs

    if algoritmo == "a_estrela":
        return busca_a_estrela

    raise ValueError("Algoritmo inválido. Use: bfs, ucs ou a_estrela.")


def escolher_melhor_minerio(
    grid: Grid,
    posicao_inicial: Position,
    picareta_melhorada: bool = False,
    algoritmo: str = "a_estrela",
) -> Optional[PlanoRota]:
    minerios = localizar_minerios(grid)
    funcao_busca = obter_algoritmo_busca(algoritmo)

    melhor_plano = None

    for posicao_minerio in minerios:
        celula = get_cell(grid, posicao_minerio)
        valor_minerio = get_ore_value(celula)

        resultado = funcao_busca(
            grid,
            posicao_inicial=posicao_inicial,
            posicao_objetivo=posicao_minerio,
            picareta_melhorada=picareta_melhorada,
        )

        if not resultado.encontrou:
            continue

        utilidade = calcular_utilidade_rota(
            valor_alvo=valor_minerio,
            custo_rota=resultado.custo,
        )

        plano = PlanoRota(
            alvo=posicao_minerio,
            valor_alvo=valor_minerio,
            resultado_busca=resultado,
            utilidade_estimada=utilidade,
        )

        if melhor_plano is None:
            melhor_plano = plano
            continue

        if plano.utilidade_estimada > melhor_plano.utilidade_estimada:
            melhor_plano = plano

    return melhor_plano