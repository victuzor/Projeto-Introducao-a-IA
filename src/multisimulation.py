from dataclasses import dataclass
from time import perf_counter, sleep
from typing import Optional, Tuple

from rich.columns import Columns
from rich.console import Group
from rich.live import Live
from rich.panel import Panel

from src.agent import aplicar_movimento
from src.dungeon import Grid, get_perceptions
from src.mental_map import (
    MapaMental,
    calcular_custos_risco_mapa_mental,
    contar_celulas_conhecidas,
    criar_grid_planejamento,
    criar_grid_visual_mapa_mental,
    criar_mapa_mental_inicial,
    atualizar_mapa_mental,
)
from src.mission import ResultadoMissao
from src.planner import PlanoRota, escolher_melhor_minerio
from src.render import console, criar_tabela_grid
from src.score import calcular_score
from src.simulation import criar_grid_simulacao
from src.state import EstadoAgente


@dataclass(frozen=True)
class ResultadoSimulacaoAlgoritmo:
    algoritmo: str
    resultado_missao: ResultadoMissao
    total_nos_expandidos: int = 0
    total_tempo_planejamento: float = 0.0
    total_custo_planejado: int = 0
    quantidade_replanejamentos: int = 0


@dataclass
class EstadoSimulacaoAlgoritmo:
    """
    Guarda o estado de simulação de um algoritmo específico.
    """

    nome_exibicao: str
    algoritmo: str
    estado_atual: EstadoAgente
    mapa_mental: Optional[MapaMental] = None
    plano_atual: Optional[PlanoRota] = None
    indice_proximo_passo: int = 0
    planos_executados: list[PlanoRota] | None = None
    logs: list[str] | None = None
    finalizado: bool = False
    motivo_parada: str = ""
    total_nos_expandidos: int = 0
    total_tempo_planejamento: float = 0.0
    total_custo_planejado: int = 0
    quantidade_replanejamentos: int = 0

    def __post_init__(self):
        if self.planos_executados is None:
            self.planos_executados = []

        if self.logs is None:
            self.logs = ["Aguardando início."]


def criar_estado_simulacao_algoritmo(
    nome_exibicao: str,
    algoritmo: str,
    estado_inicial: EstadoAgente,
    mapa_mental: Optional[MapaMental] = None,
) -> EstadoSimulacaoAlgoritmo:
    """
    Cria o estado visual inicial de um algoritmo.
    """
    return EstadoSimulacaoAlgoritmo(
        nome_exibicao=nome_exibicao,
        algoritmo=algoritmo,
        estado_atual=estado_inicial,
        mapa_mental=mapa_mental,
    )


def _obter_grid_e_custos_planejamento(
    estado_simulacao: EstadoSimulacaoAlgoritmo,
    grid_real: Grid,
):
    """
    Retorna o grid e os custos que o algoritmo pode usar para planejar.

    Se houver mapa mental, o agente planeja sobre conhecimento parcial.
    Se não houver, mantém o comportamento antigo usando o mapa real.
    """
    if estado_simulacao.mapa_mental is None:
        return grid_real, None

    grid_planejamento = criar_grid_planejamento(estado_simulacao.mapa_mental)

    if estado_simulacao.algoritmo == "bfs":
        return grid_planejamento, None

    custos_extras = calcular_custos_risco_mapa_mental(
        estado_simulacao.mapa_mental
    )

    return grid_planejamento, custos_extras


def _registrar_metricas_planejamento(
    estado_simulacao: EstadoSimulacaoAlgoritmo,
    plano: PlanoRota,
    tempo_planejamento: float,
) -> None:
    """
    Acumula métricas computacionais do planejamento.
    """
    estado_simulacao.quantidade_replanejamentos += 1
    estado_simulacao.total_tempo_planejamento += tempo_planejamento
    estado_simulacao.total_custo_planejado += plano.resultado_busca.custo
    estado_simulacao.total_nos_expandidos += plano.nos_expandidos_planejamento


def avancar_simulacao_algoritmo(
    grid: Grid,
    estado_simulacao: EstadoSimulacaoAlgoritmo,
    utilidade_minima: int = 1,
) -> EstadoSimulacaoAlgoritmo:
    """
    Avança um único passo da simulação de um algoritmo.

    Quando há mapa mental, o agente replana após cada passo, pois pode
    descobrir novas paredes, paredes frágeis ou suspeitas de monstros.
    """
    if estado_simulacao.finalizado:
        return estado_simulacao

    estado_atual = estado_simulacao.estado_atual

    if estado_simulacao.plano_atual is None:
        grid_planejamento, custos_extras = _obter_grid_e_custos_planejamento(
            estado_simulacao,
            grid,
        )

        inicio_planejamento = perf_counter()

        plano = escolher_melhor_minerio(
            grid=grid_planejamento,
            posicao_inicial=estado_atual.posicao,
            picareta_melhorada=estado_atual.picareta_melhorada,
            ferro_disponivel=estado_atual.ferro,
            algoritmo=estado_simulacao.algoritmo,
            minerios_ignorados=estado_atual.minerios_coletados,
            custos_extras=custos_extras,
        )

        tempo_planejamento = perf_counter() - inicio_planejamento

        if plano is None:
            estado_simulacao.quantidade_replanejamentos += 1
            estado_simulacao.total_tempo_planejamento += tempo_planejamento
            estado_simulacao.finalizado = True
            estado_simulacao.motivo_parada = "Não há mais minérios acessíveis."
            estado_simulacao.logs.append(estado_simulacao.motivo_parada)
            return estado_simulacao

        _registrar_metricas_planejamento(
            estado_simulacao=estado_simulacao,
            plano=plano,
            tempo_planejamento=tempo_planejamento,
        )

        if plano.utilidade_estimada < utilidade_minima:
            estado_simulacao.finalizado = True
            estado_simulacao.motivo_parada = (
                "Próxima coleta não possui utilidade positiva."
            )
            estado_simulacao.logs.append(estado_simulacao.motivo_parada)
            return estado_simulacao

        estado_simulacao.plano_atual = plano
        estado_simulacao.indice_proximo_passo = 1
        estado_simulacao.planos_executados.append(plano)

        estado_simulacao.logs.append(
            f"Novo alvo {plano.alvo} | "
            f"custo={plano.resultado_busca.custo} | "
            f"nós={plano.nos_expandidos_planejamento} | "
            f"tempo={tempo_planejamento:.6f}s"
        )

        return estado_simulacao

    caminho = estado_simulacao.plano_atual.resultado_busca.caminho

    if estado_simulacao.indice_proximo_passo >= len(caminho):
        estado_simulacao.plano_atual = None
        estado_simulacao.indice_proximo_passo = 0
        return estado_simulacao

    proxima_posicao = caminho[estado_simulacao.indice_proximo_passo]

    novo_estado = aplicar_movimento(
        grid=grid,
        estado=estado_atual,
        nova_posicao=proxima_posicao,
    )

    estado_simulacao.estado_atual = novo_estado
    estado_simulacao.indice_proximo_passo += 1
    estado_simulacao.logs.append(f"Moveu para {proxima_posicao}")

    if estado_simulacao.mapa_mental is not None:
        estado_simulacao.mapa_mental = atualizar_mapa_mental(
            mapa_mental=estado_simulacao.mapa_mental,
            grid_real=grid,
            posicao_atual=novo_estado.posicao,
        )
        estado_simulacao.logs.append("Mapa mental atualizado.")
        estado_simulacao.plano_atual = None
        estado_simulacao.indice_proximo_passo = 0
        return estado_simulacao

    if estado_simulacao.indice_proximo_passo >= len(caminho):
        estado_simulacao.logs.append(f"Coleta concluída em {novo_estado.posicao}")
        estado_simulacao.plano_atual = None
        estado_simulacao.indice_proximo_passo = 0

    return estado_simulacao


def criar_linhas_estado_algoritmo(
    grid: Grid,
    estado_simulacao: EstadoSimulacaoAlgoritmo,
) -> list[str]:
    """
    Cria linhas de estado para um algoritmo.
    """
    estado = estado_simulacao.estado_atual
    score = calcular_score(estado)
    picareta = "melhorada" if estado.picareta_melhorada else "básica"
    percepcoes = get_perceptions(grid, estado.posicao)

    linhas = [
        f"Posição: {estado.posicao}",
        f"Percepções: {percepcoes}",
        f"Passos: {estado.passos}",
        f"Dinheiro: {estado.dinheiro}",
        f"Ferro: {estado.ferro}",
        f"Picareta: {picareta}",
        f"Penalidades: {estado.penalidades}",
        f"Custo risco: {estado.custo_risco}",
        f"Score: {score.score_final}",
        f"Coletas: {len(estado.minerios_coletados)}",
        f"Nós expandidos: {estado_simulacao.total_nos_expandidos}",
        f"Replanejamentos: {estado_simulacao.quantidade_replanejamentos}",
        f"Tempo plan.: {estado_simulacao.total_tempo_planejamento:.6f}s",
    ]

    if estado_simulacao.mapa_mental is not None:
        linhas.append(
            f"Células conhecidas: "
            f"{contar_celulas_conhecidas(estado_simulacao.mapa_mental)}"
        )

    if estado_simulacao.finalizado:
        linhas.append("Status: finalizado")
    else:
        linhas.append("Status: executando")

    return linhas


def criar_painel_algoritmo(
    grid: Grid,
    estado_simulacao: EstadoSimulacaoAlgoritmo,
) -> Panel:
    """
    Cria um painel visual para um algoritmo.
    """
    caminho_planejado = ()

    if estado_simulacao.plano_atual is not None:
        caminho_planejado = estado_simulacao.plano_atual.resultado_busca.caminho

    if estado_simulacao.mapa_mental is not None:
        grid_visual = criar_grid_visual_mapa_mental(
            mapa_mental=estado_simulacao.mapa_mental,
            posicao_agente=estado_simulacao.estado_atual.posicao,
            caminho_percorrido=estado_simulacao.estado_atual.caminho,
            caminho_planejado=caminho_planejado,
        )
    else:
        grid_visual = criar_grid_simulacao(
            grid=grid,
            posicao_agente=estado_simulacao.estado_atual.posicao,
            caminho_percorrido=estado_simulacao.estado_atual.caminho,
            caminho_planejado=caminho_planejado,
        )

    tabela = criar_tabela_grid(grid_visual, estado_simulacao.nome_exibicao)

    painel_estado = Panel(
        "\n".join(criar_linhas_estado_algoritmo(grid, estado_simulacao)),
        title="Estado",
        border_style="green",
    )

    logs = estado_simulacao.logs[-5:] if estado_simulacao.logs else []
    texto_logs = "\n".join(logs) if logs else "Sem logs."

    painel_logs = Panel(
        texto_logs,
        title="Log",
        border_style="blue",
    )

    return Panel(
        Group(tabela, painel_estado, painel_logs),
        title=estado_simulacao.nome_exibicao,
        border_style="cyan",
    )


def criar_tela_comparativa(
    grid: Grid,
    estados_simulacao: Tuple[EstadoSimulacaoAlgoritmo, ...],
) -> Group:
    """
    Cria a tela com os três algoritmos lado a lado.
    """
    paineis = [
        criar_painel_algoritmo(grid, estado_simulacao)
        for estado_simulacao in estados_simulacao
    ]

    return Group(
        Panel.fit(
            "[bold cyan]Simulação Comparativa[/bold cyan]\n"
            "BFS, UCS e A* usando mapa mental, replanejamento e métricas.",
            border_style="cyan",
        ),
        Columns(paineis, equal=True, expand=True),
    )


def todos_finalizados(
    estados_simulacao: Tuple[EstadoSimulacaoAlgoritmo, ...],
) -> bool:
    """
    Verifica se todos os algoritmos finalizaram.
    """
    return all(estado.finalizado for estado in estados_simulacao)


def simular_algoritmos_visual(
    grid: Grid,
    estado_inicial: EstadoAgente,
    utilidade_minima: int = 1,
    max_iteracoes: int = 200,
    delay: float = 0.8,
) -> Tuple[ResultadoSimulacaoAlgoritmo, ...]:
    """
    Executa BFS, UCS e A* lado a lado em tempo real.

    Cada algoritmo recebe seu próprio mapa mental, começando apenas com a
    bússola dos minérios e atualizando o conhecimento conforme anda.
    """
    estados_simulacao = (
        criar_estado_simulacao_algoritmo(
            "BFS",
            "bfs",
            estado_inicial,
            criar_mapa_mental_inicial(grid, estado_inicial.posicao),
        ),
        criar_estado_simulacao_algoritmo(
            "UCS",
            "ucs",
            estado_inicial,
            criar_mapa_mental_inicial(grid, estado_inicial.posicao),
        ),
        criar_estado_simulacao_algoritmo(
            "A*",
            "a_estrela",
            estado_inicial,
            criar_mapa_mental_inicial(grid, estado_inicial.posicao),
        ),
    )

    with Live(
        criar_tela_comparativa(grid, estados_simulacao),
        console=console,
        refresh_per_second=4,
        transient=False,
    ) as live:
        sleep(delay)

        for _ in range(max_iteracoes):
            if todos_finalizados(estados_simulacao):
                break

            for estado_simulacao in estados_simulacao:
                avancar_simulacao_algoritmo(
                    grid=grid,
                    estado_simulacao=estado_simulacao,
                    utilidade_minima=utilidade_minima,
                )

            live.update(
                criar_tela_comparativa(grid, estados_simulacao),
                refresh=True,
            )

            sleep(delay)

    resultados = []

    for estado_simulacao in estados_simulacao:
        estado_final = estado_simulacao.estado_atual
        score = calcular_score(estado_final)

        resultado_missao = ResultadoMissao(
            estado_final=estado_final,
            planos_executados=tuple(estado_simulacao.planos_executados),
            score=score,
            motivo_parada=estado_simulacao.motivo_parada,
        )

        resultados.append(
            ResultadoSimulacaoAlgoritmo(
                algoritmo=estado_simulacao.nome_exibicao,
                resultado_missao=resultado_missao,
                total_nos_expandidos=estado_simulacao.total_nos_expandidos,
                total_tempo_planejamento=estado_simulacao.total_tempo_planejamento,
                total_custo_planejado=estado_simulacao.total_custo_planejado,
                quantidade_replanejamentos=estado_simulacao.quantidade_replanejamentos,
            )
        )

    return tuple(resultados)