from typing import Callable, Tuple

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.dungeon import (
    AGENT,
    COPPER,
    CRACK_PERCEPTION,
    EMPTY,
    FRAGILE_WALL,
    GOLD,
    GOO_PERCEPTION,
    Grid,
    IRON,
    Position,
    SKELETON,
    SLIME,
    WALL,
    get_perceptions,
)


console = Console()

Caminho = Tuple[Position, ...]
ROUTE = "*"


def formatar_simbolo(celula: str) -> str:
    """
    Aplica formatação visual aos símbolos do mapa.
    """
    if celula == AGENT:
        return "[bold cyan]A[/bold cyan]"

    if celula == EMPTY:
        return "[dim].[/dim]"

    if celula == WALL:
        return "[white]#[/white]"

    if celula == FRAGILE_WALL:
        return "[yellow]X[/yellow]"

    if celula == SLIME:
        return "[green]S[/green]"

    if celula == SKELETON:
        return "[red]E[/red]"

    if celula == IRON:
        return "[bright_white]Fe[/bright_white]"

    if celula == COPPER:
        return "[orange3]Cu[/orange3]"

    if celula == GOLD:
        return "[bold yellow]Au[/bold yellow]"

    if celula == ROUTE:
        return "[bold magenta]*[/bold magenta]"

    return celula


def criar_tabela_grid(grid: Grid, titulo: str) -> Table:
    """
    Cria uma tabela Rich para exibir o grid.
    """
    table = Table(
        title=titulo,
        box=box.ROUNDED,
        show_header=False,
        expand=False,
        padding=(0, 1),
    )

    for _ in range(len(grid[0])):
        table.add_column(justify="center", no_wrap=True)

    for row in grid:
        table.add_row(*[formatar_simbolo(cell) for cell in row])

    return table


def render_titulo() -> None:
    """
    Exibe o título principal do projeto.
    """
    console.print(
        Panel.fit(
            "[bold cyan]uAI Dungeon Miner[/bold cyan]\n"
            "Projeto de Introdução à Inteligência Artificial",
            border_style="cyan",
        )
    )


def render_grid(grid: Grid) -> None:
    """
    Exibe o mapa da dungeon no terminal usando Rich.
    """
    table = criar_tabela_grid(grid, "Dungeon 8x8")
    console.print(table)


def render_perception_grid(grid: Grid) -> None:
    """
    Exibe um mapa separado mostrando onde existem percepções.

    G = gosma próxima, indicando slime vizinho
    C = crack próximo, indicando esqueleto vizinho
    """
    perception_grid = []

    for row_index, row in enumerate(grid):
        perception_row = []

        for col_index, cell in enumerate(row):
            position = (row_index, col_index)

            if cell == SLIME:
                symbol = "S"
            elif cell == SKELETON:
                symbol = "E"
            else:
                perceptions = get_perceptions(grid, position)

                symbol_parts = []

                if GOO_PERCEPTION in perceptions:
                    symbol_parts.append("G")

                if CRACK_PERCEPTION in perceptions:
                    symbol_parts.append("C")

                if symbol_parts:
                    symbol = "".join(symbol_parts)
                else:
                    symbol = EMPTY

            perception_row.append(symbol)

        perception_grid.append(perception_row)

    table = criar_tabela_grid(perception_grid, "Mapa de Percepções")
    console.print(table)
    console.print("[dim]Legenda: G = gosma próxima | C = crack próximo[/dim]")


def criar_grid_com_caminho(grid: Grid, caminho: Caminho) -> Grid:
    """
    Cria uma cópia visual do mapa marcando o caminho planejado.

    O caminho é marcado com '*'.
    A posição inicial e a posição final são preservadas para não esconder
    o agente nem o minério alvo.
    """
    grid_visual = [linha.copy() for linha in grid]

    if not caminho:
        return grid_visual

    posicao_inicial = caminho[0]
    posicao_final = caminho[-1]

    for posicao in caminho:
        if posicao == posicao_inicial:
            continue

        if posicao == posicao_final:
            continue

        linha, coluna = posicao
        grid_visual[linha][coluna] = ROUTE

    return grid_visual


def render_route_grid(grid: Grid, caminho: Caminho) -> None:
    """
    Exibe o mapa com o caminho planejado pelo agente.
    """
    grid_com_caminho = criar_grid_com_caminho(grid, caminho)
    table = criar_tabela_grid(grid_com_caminho, "Rota Planejada")
    console.print(table)
    console.print("[dim]Legenda: * = caminho planejado[/dim]")


def render_painel(titulo: str, linhas: list[str]) -> None:
    """
    Exibe informações em formato de painel.
    """
    conteudo = "\n".join(linhas)
    console.print(Panel(conteudo, title=titulo, border_style="blue"))


def render_comparacao_algoritmos(
    resultados,
    formatar_caminho: Callable,
) -> None:
    """
    Exibe a comparação entre BFS, UCS e A* em formato de tabela.
    """
    table = Table(
        title="Comparação dos Algoritmos",
        box=box.ROUNDED,
        show_lines=True,
    )

    table.add_column("Algoritmo", justify="center")
    table.add_column("Encontrou", justify="center")
    table.add_column("Custo", justify="right")
    table.add_column("Nós", justify="right")
    table.add_column("Tempo", justify="right")
    table.add_column("Passos", justify="right")
    table.add_column("Dinheiro", justify="right")
    table.add_column("Penalidades", justify="right")
    table.add_column("Score", justify="right")
    table.add_column("Caminho", justify="left")

    for resultado in resultados:
        table.add_row(
            resultado.algoritmo,
            "Sim" if resultado.encontrou else "Não",
            str(resultado.custo_busca),
            str(resultado.nos_expandidos),
            f"{resultado.tempo_execucao:.6f}s",
            str(resultado.passos),
            str(resultado.dinheiro),
            str(resultado.penalidades),
            str(resultado.score_final),
            formatar_caminho(resultado.caminho),
        )

    console.print(table)


def render_score_final(texto_score: str) -> None:
    """
    Exibe o score final em um painel.
    """
    console.print(
        Panel(
            texto_score,
            title="Score Final",
            border_style="green",
        )
    )