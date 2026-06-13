from dataclasses import dataclass
from time import perf_counter
from typing import Callable, Tuple

from src.agent import executar_caminho
from src.dungeon import Grid, Position
from src.score import calcular_score
from src.search import (
    ResultadoBusca,
    busca_a_estrela,
    busca_bfs,
    busca_ucs,
)


@dataclass(frozen=True)
class ResultadoComparacao:

    algoritmo: str
    encontrou: bool
    caminho: Tuple[Position, ...]
    custo_busca: int
    nos_expandidos: int
    tempo_execucao: float
    passos: int
    dinheiro: int
    penalidades: int
    score_final: int


def avaliar_algoritmo(
    nome_algoritmo: str,
    funcao_busca: Callable[..., ResultadoBusca],
    grid: Grid,
    posicao_inicial: Position,
    posicao_objetivo: Position,
    picareta_melhorada: bool = False,
) -> ResultadoComparacao:
    inicio = perf_counter()

    resultado_busca = funcao_busca(
        grid,
        posicao_inicial=posicao_inicial,
        posicao_objetivo=posicao_objetivo,
        picareta_melhorada=picareta_melhorada,
    )

    fim = perf_counter()
    tempo_execucao = fim - inicio

    if not resultado_busca.encontrou:
        return ResultadoComparacao(
            algoritmo=nome_algoritmo,
            encontrou=False,
            caminho=(),
            custo_busca=0,
            nos_expandidos=resultado_busca.nos_expandidos,
            tempo_execucao=tempo_execucao,
            passos=0,
            dinheiro=0,
            penalidades=0,
            score_final=0,
        )

    from src.state import criar_estado_inicial

    estado_inicial = criar_estado_inicial(posicao_inicial)

    if picareta_melhorada:
        estado_inicial = estado_inicial.coletar_minerio(
            posicao_minerio=posicao_inicial,
            valor_minerio=0,
            quantidade_ferro=1,
        )
        estado_inicial = estado_inicial.melhorar_picareta()

    estado_final = executar_caminho(
        grid=grid,
        estado_inicial=estado_inicial,
        caminho=resultado_busca.caminho,
    )

    resultado_score = calcular_score(estado_final)

    return ResultadoComparacao(
        algoritmo=nome_algoritmo,
        encontrou=True,
        caminho=resultado_busca.caminho,
        custo_busca=resultado_busca.custo,
        nos_expandidos=resultado_busca.nos_expandidos,
        tempo_execucao=tempo_execucao,
        passos=estado_final.passos,
        dinheiro=estado_final.dinheiro,
        penalidades=estado_final.penalidades,
        score_final=resultado_score.score_final,
    )


def comparar_algoritmos(
    grid: Grid,
    posicao_inicial: Position,
    posicao_objetivo: Position,
    picareta_melhorada: bool = False,
) -> Tuple[ResultadoComparacao, ...]:
    """
    Compara BFS, UCS e A* para o mesmo objetivo.
    """
    resultados = [
        avaliar_algoritmo(
            nome_algoritmo="BFS",
            funcao_busca=busca_bfs,
            grid=grid,
            posicao_inicial=posicao_inicial,
            posicao_objetivo=posicao_objetivo,
            picareta_melhorada=picareta_melhorada,
        ),
        avaliar_algoritmo(
            nome_algoritmo="UCS",
            funcao_busca=busca_ucs,
            grid=grid,
            posicao_inicial=posicao_inicial,
            posicao_objetivo=posicao_objetivo,
            picareta_melhorada=picareta_melhorada,
        ),
        avaliar_algoritmo(
            nome_algoritmo="A*",
            funcao_busca=busca_a_estrela,
            grid=grid,
            posicao_inicial=posicao_inicial,
            posicao_objetivo=posicao_objetivo,
            picareta_melhorada=picareta_melhorada,
        ),
    ]

    return tuple(resultados)


def formatar_resultado_comparacao(resultado: ResultadoComparacao) -> str:
    """
    Formata uma comparação para exibição no terminal.
    """
    return (
        f"Algoritmo: {resultado.algoritmo}\n"
        f"Encontrou caminho: {resultado.encontrou}\n"
        f"Custo da busca: {resultado.custo_busca}\n"
        f"Nós expandidos: {resultado.nos_expandidos}\n"
        f"Tempo de execução: {resultado.tempo_execucao:.6f}s\n"
        f"Passos finais: {resultado.passos}\n"
        f"Dinheiro coletado: {resultado.dinheiro}\n"
        f"Penalidades: {resultado.penalidades}\n"
        f"Score final: {resultado.score_final}"
    )