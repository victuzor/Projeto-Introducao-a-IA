from dataclasses import dataclass
from typing import Tuple

from src.agent import executar_caminho
from src.dungeon import Grid
from src.planner import PlanoRota, escolher_melhor_minerio
from src.score import ResultadoScore, calcular_score
from src.state import EstadoAgente


PlanosExecutados = Tuple[PlanoRota, ...]


@dataclass(frozen=True)
class ResultadoMissao:
    """
    Guarda o resultado da missão completa de coleta de minérios.
    """

    estado_final: EstadoAgente
    planos_executados: PlanosExecutados
    score: ResultadoScore
    motivo_parada: str


def executar_missao_coleta(
    grid: Grid,
    estado_inicial: EstadoAgente,
    algoritmo: str = "a_estrela",
    utilidade_minima: int = 1,
    max_coletas: int = 20,
) -> ResultadoMissao:
    """
    Executa uma missão de coleta de múltiplos minérios.

    Estratégia usada:
    - localizar minérios ainda não coletados;
    - escolher o minério com maior utilidade estimada;
    - executar a rota;
    - atualizar o estado do agente;
    - repetir enquanto a utilidade for positiva.

    utilidade = valor do minério - custo da rota
    """
    estado_atual = estado_inicial
    planos_executados = []

    for _ in range(max_coletas):
        plano = escolher_melhor_minerio(
            grid=grid,
            posicao_inicial=estado_atual.posicao,
            picareta_melhorada=estado_atual.picareta_melhorada,
            ferro_disponivel=estado_atual.ferro,
            algoritmo=algoritmo,
            minerios_ignorados=estado_atual.minerios_coletados,
        )

        if plano is None:
            return _criar_resultado(
                estado_atual,
                tuple(planos_executados),
                "Não há mais minérios acessíveis.",
            )

        if plano.utilidade_estimada < utilidade_minima:
            return _criar_resultado(
                estado_atual,
                tuple(planos_executados),
                "Próxima coleta não possui utilidade positiva.",
            )

        estado_atual = executar_caminho(
            grid=grid,
            estado_inicial=estado_atual,
            caminho=plano.resultado_busca.caminho,
        )

        planos_executados.append(plano)

    return _criar_resultado(
        estado_atual,
        tuple(planos_executados),
        "Limite máximo de coletas atingido.",
    )


def _criar_resultado(
    estado_final: EstadoAgente,
    planos_executados: PlanosExecutados,
    motivo_parada: str,
) -> ResultadoMissao:
    """
    Cria o resultado final da missão.
    """
    return ResultadoMissao(
        estado_final=estado_final,
        planos_executados=planos_executados,
        score=calcular_score(estado_final),
        motivo_parada=motivo_parada,
    )


def formatar_planos_executados(planos: PlanosExecutados) -> list[str]:
    """
    Formata os planos executados para exibição.
    """
    if not planos:
        return ["Nenhuma rota de coleta foi executada."]

    linhas = []

    for indice, plano in enumerate(planos, start=1):
        linhas.append(
            f"{indice}. Alvo {plano.alvo} | "
            f"Valor: {plano.valor_alvo} | "
            f"Custo: {plano.resultado_busca.custo} | "
            f"Utilidade: {plano.utilidade_estimada}"
        )

    return linhas