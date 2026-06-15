from dataclasses import dataclass
from typing import Callable, Mapping, Optional, Tuple

from src.dungeon import Grid, Position, get_cell, get_ore_value, is_ore
from src.search import ResultadoBusca, busca_a_estrela, busca_bfs, busca_ucs


Minerios = Tuple[Position, ...]
CustosExtras = Optional[Mapping[Position, int]]


@dataclass(frozen=True)
class PlanoRota:
    """
    Representa uma rota planejada pelo agente até um minério.

    nos_expandidos_planejamento representa o total de nós expandidos
    para avaliar todos os minérios candidatos naquele momento.
    """

    alvo: Position
    valor_alvo: int
    resultado_busca: ResultadoBusca
    utilidade_estimada: int
    nos_expandidos_planejamento: int = 0


def localizar_minerios(grid: Grid) -> Minerios:
    """
    Localiza todos os minérios existentes no mapa.
    """
    minerios = []

    for linha_indice, linha in enumerate(grid):
        for coluna_indice, celula in enumerate(linha):
            if is_ore(celula):
                minerios.append((linha_indice, coluna_indice))

    return tuple(minerios)


def calcular_utilidade_rota(valor_alvo: int, custo_rota: int) -> int:
    """
    Calcula a utilidade estimada de uma rota.

    Quanto maior o valor do minério e menor o custo da rota,
    melhor será a utilidade.
    """
    return valor_alvo - custo_rota


def obter_algoritmo_busca(algoritmo: str) -> Callable:
    """
    Retorna a função de busca escolhida pelo nome.
    """
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
    ferro_disponivel: int = 0,
    algoritmo: str = "a_estrela",
    minerios_ignorados: Minerios = (),
    custos_extras: CustosExtras = None,
) -> Optional[PlanoRota]:
    """
    Escolhe o melhor minério para o agente buscar.

    O agente avalia todos os minérios conhecidos no mapa.
    Para cada minério, ele calcula uma rota usando o algoritmo escolhido.
    Depois, escolhe o minério com maior utilidade estimada.

    Minérios ignorados são aqueles que já foram coletados.
    """
    minerios = localizar_minerios(grid)
    minerios_ignorados_set = set(minerios_ignorados)
    funcao_busca = obter_algoritmo_busca(algoritmo)

    melhor_alvo = None
    melhor_valor = 0
    melhor_resultado = None
    melhor_utilidade = 0
    total_nos_expandidos = 0

    for posicao_minerio in minerios:
        if posicao_minerio in minerios_ignorados_set:
            continue

        celula = get_cell(grid, posicao_minerio)
        valor_minerio = get_ore_value(celula)

        resultado = funcao_busca(
            grid,
            posicao_inicial=posicao_inicial,
            posicao_objetivo=posicao_minerio,
            picareta_melhorada=picareta_melhorada,
            ferro_inicial=ferro_disponivel,
            custos_extras=custos_extras,
        )

        total_nos_expandidos += resultado.nos_expandidos

        if not resultado.encontrou:
            continue

        utilidade = calcular_utilidade_rota(
            valor_alvo=valor_minerio,
            custo_rota=resultado.custo,
        )

        if melhor_resultado is None or utilidade > melhor_utilidade:
            melhor_alvo = posicao_minerio
            melhor_valor = valor_minerio
            melhor_resultado = resultado
            melhor_utilidade = utilidade

    if melhor_resultado is None or melhor_alvo is None:
        return None

    return PlanoRota(
        alvo=melhor_alvo,
        valor_alvo=melhor_valor,
        resultado_busca=melhor_resultado,
        utilidade_estimada=melhor_utilidade,
        nos_expandidos_planejamento=total_nos_expandidos,
    )