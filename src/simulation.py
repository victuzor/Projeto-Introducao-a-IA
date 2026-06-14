from time import sleep
from typing import Tuple

from rich.console import Group
from rich.live import Live
from rich.panel import Panel

from src.agent import aplicar_movimento
from src.dungeon import AGENT, EMPTY, Grid, Position
from src.mission import ResultadoMissao
from src.planner import PlanoRota, escolher_melhor_minerio
from src.render import ROUTE, console, criar_tabela_grid
from src.score import calcular_score
from src.state import EstadoAgente


Caminho = Tuple[Position, ...]


def criar_grid_simulacao(
    grid: Grid,
    posicao_agente: Position,
    caminho_percorrido: Caminho = (),
    caminho_planejado: Caminho = (),
) -> Grid:
    """
    Cria uma versão visual do mapa para a simulação.
    """
    grid_visual = [linha.copy() for linha in grid]

    for linha_indice, linha in enumerate(grid_visual):
        for coluna_indice, celula in enumerate(linha):
            if celula == AGENT:
                grid_visual[linha_indice][coluna_indice] = EMPTY

    posicao_final_planejada = caminho_planejado[-1] if caminho_planejado else None

    for posicao in caminho_planejado:
        if posicao == posicao_agente:
            continue

        if posicao == posicao_final_planejada:
            continue

        linha, coluna = posicao
        grid_visual[linha][coluna] = ROUTE

    for posicao in caminho_percorrido:
        if posicao == posicao_agente:
            continue

        linha, coluna = posicao
        grid_visual[linha][coluna] = ROUTE

    linha_agente, coluna_agente = posicao_agente
    grid_visual[linha_agente][coluna_agente] = AGENT

    return grid_visual


def criar_linhas_estado(estado: EstadoAgente) -> list[str]:
    """
    Cria linhas de texto com o estado atual do agente.
    """
    score = calcular_score(estado)
    picareta = "melhorada" if estado.picareta_melhorada else "básica"

    return [
        f"Posição: {estado.posicao}",
        f"Passos: {estado.passos}",
        f"Dinheiro: {estado.dinheiro}",
        f"Ferro: {estado.ferro}",
        f"Picareta: {picareta}",
        f"Penalidades: {estado.penalidades}",
        f"Custo risco: {estado.custo_risco}",
        f"Score parcial: {score.score_final}",
        f"Minérios coletados: {len(estado.minerios_coletados)}",
    ]


def criar_tela_simulacao(
    grid: Grid,
    estado: EstadoAgente,
    caminho_planejado: Caminho = (),
    logs: list[str] | None = None,
) -> Group:
    """
    Monta a tela visual da simulação.
    """
    if logs is None:
        logs = []

    grid_visual = criar_grid_simulacao(
        grid=grid,
        posicao_agente=estado.posicao,
        caminho_percorrido=estado.caminho,
        caminho_planejado=caminho_planejado,
    )

    tabela_grid = criar_tabela_grid(grid_visual, "Simulação da Missão")

    painel_estado = Panel(
        "\n".join(criar_linhas_estado(estado)),
        title="Estado do Agente",
        border_style="green",
    )

    texto_logs = "\n".join(logs[-8:]) if logs else "Aguardando início da missão."

    painel_logs = Panel(
        texto_logs,
        title="Log da Missão",
        border_style="blue",
    )

    return Group(tabela_grid, painel_estado, painel_logs)


def simular_missao_visual(
    grid: Grid,
    estado_inicial: EstadoAgente,
    algoritmo: str = "a_estrela",
    utilidade_minima: int = 1,
    max_coletas: int = 20,
    delay: float = 0.8,
) -> ResultadoMissao:
    """
    Executa visualmente a missão de coleta de múltiplos minérios.
    """
    estado_atual = estado_inicial
    planos_executados: list[PlanoRota] = []
    logs: list[str] = ["Missão iniciada."]

    motivo_parada = "Limite máximo de coletas atingido."

    with Live(
        criar_tela_simulacao(grid, estado_atual, logs=logs),
        console=console,
        refresh_per_second=4,
        transient=False,
    ) as live:
        sleep(delay)

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
                motivo_parada = "Não há mais minérios acessíveis."
                logs.append(motivo_parada)
                live.update(
                    criar_tela_simulacao(grid, estado_atual, logs=logs),
                    refresh=True,
                )
                break

            if plano.utilidade_estimada < utilidade_minima:
                motivo_parada = "Próxima coleta não possui utilidade positiva."
                logs.append(motivo_parada)
                live.update(
                    criar_tela_simulacao(grid, estado_atual, logs=logs),
                    refresh=True,
                )
                break

            planos_executados.append(plano)

            logs.append(
                f"Novo alvo: {plano.alvo} | "
                f"valor={plano.valor_alvo} | "
                f"custo={plano.resultado_busca.custo} | "
                f"utilidade={plano.utilidade_estimada}"
            )

            live.update(
                criar_tela_simulacao(
                    grid,
                    estado_atual,
                    caminho_planejado=plano.resultado_busca.caminho,
                    logs=logs,
                ),
                refresh=True,
            )

            sleep(delay)

            for proxima_posicao in plano.resultado_busca.caminho[1:]:
                estado_atual = aplicar_movimento(
                    grid=grid,
                    estado=estado_atual,
                    nova_posicao=proxima_posicao,
                )

                logs.append(f"Agente moveu para {proxima_posicao}")

                live.update(
                    criar_tela_simulacao(
                        grid,
                        estado_atual,
                        caminho_planejado=plano.resultado_busca.caminho,
                        logs=logs,
                    ),
                    refresh=True,
                )

                sleep(delay)

        else:
            logs.append(motivo_parada)
            live.update(
                criar_tela_simulacao(grid, estado_atual, logs=logs),
                refresh=True,
            )

    return ResultadoMissao(
        estado_final=estado_atual,
        planos_executados=tuple(planos_executados),
        score=calcular_score(estado_atual),
        motivo_parada=motivo_parada,
    )