from typing import List, Tuple

Position = Tuple[int, int]
Grid = List[List[str]]

GRID_SIZE = 8

EMPTY = "."
AGENT = "A"

WALL = "#"
FRAGILE_WALL = "X"
SLIME = "S"
SKELETON = "E"

IRON = "Fe"
COPPER = "Cu"
GOLD = "Au"

GOO_PERCEPTION = "gosma"
CRACK_PERCEPTION = "crack"

ORE_VALUES = {
    IRON: 10,
    COPPER: 20,
    GOLD: 50,
}


def create_default_dungeon() -> Grid:
    """
    Cria um mapa fixo 8x8 para facilitar os testes e a comparação dos algoritmos.

    Símbolos:
    A  = agente
    .  = célula vazia
    Fe = ferro
    Cu = cobre
    Au = ouro
    #  = parede comum
    X  = parede frágil
    S  = slime
    E  = esqueleto

    Percepções:
    gosma = existe slime em uma célula vizinha
    crack = existe esqueleto em uma célula vizinha
    """
    return [
        [AGENT, EMPTY, IRON, FRAGILE_WALL, GOLD, EMPTY, SLIME, EMPTY],
        [EMPTY, WALL, EMPTY, EMPTY, EMPTY, WALL, EMPTY, COPPER],
        [IRON, EMPTY, SLIME, EMPTY, FRAGILE_WALL, WALL, EMPTY, EMPTY],
        [EMPTY, WALL, WALL, GOLD, EMPTY, SKELETON, EMPTY, WALL],
        [WALL, EMPTY, EMPTY, EMPTY, WALL, EMPTY, IRON, EMPTY],
        [EMPTY, EMPTY, FRAGILE_WALL, WALL, SLIME, EMPTY, COPPER, EMPTY],
        [GOLD, WALL, EMPTY, SKELETON, EMPTY, WALL, EMPTY, EMPTY],
        [EMPTY, EMPTY, COPPER, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    ]


def find_agent_position(grid: Grid) -> Position:
    """
    Encontra a posição inicial do agente no mapa.
    """
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if cell == AGENT:
                return row_index, col_index

    raise ValueError("Agente não encontrado no mapa.")


def is_inside_grid(position: Position) -> bool:
    """
    Verifica se uma posição está dentro dos limites da dungeon.
    """
    row, col = position
    return 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE


def get_cell(grid: Grid, position: Position) -> str:
    """
    Retorna o conteúdo de uma célula do mapa.
    """
    row, col = position
    return grid[row][col]


def get_neighbors(position: Position) -> List[Position]:
    """
    Retorna as posições vizinhas válidas.

    Consideramos apenas cima, baixo, esquerda e direita.
    Não consideramos diagonais.
    """
    row, col = position

    possible_neighbors = [
        (row - 1, col),
        (row + 1, col),
        (row, col - 1),
        (row, col + 1),
    ]

    valid_neighbors = []

    for neighbor in possible_neighbors:
        if is_inside_grid(neighbor):
            valid_neighbors.append(neighbor)

    return valid_neighbors


def get_perceptions(grid: Grid, position: Position) -> List[str]:
    """
    Retorna as percepções da posição atual.

    Se houver slime em uma célula vizinha, retorna 'gosma'.
    Se houver esqueleto em uma célula vizinha, retorna 'crack'.
    """
    perceptions = []

    neighbors = get_neighbors(position)

    for neighbor in neighbors:
        cell = get_cell(grid, neighbor)

        if cell == SLIME and GOO_PERCEPTION not in perceptions:
            perceptions.append(GOO_PERCEPTION)

        if cell == SKELETON and CRACK_PERCEPTION not in perceptions:
            perceptions.append(CRACK_PERCEPTION)

    return perceptions


def is_blocked(cell: str, picareta_melhorada: bool = False) -> bool:
    """
    Verifica se uma célula bloqueia o caminho do agente.

    Parede comum sempre bloqueia.
    Parede frágil bloqueia apenas se o agente ainda não tiver picareta melhorada.
    """
    if cell == WALL:
        return True

    if cell == FRAGILE_WALL and not picareta_melhorada:
        return True

    return False


def is_ore(cell: str) -> bool:
    """
    Verifica se uma célula contém minério.
    """
    return cell in ORE_VALUES


def get_ore_value(cell: str) -> int:
    """
    Retorna o valor de um minério.
    Caso a célula não seja minério, retorna 0.
    """
    return ORE_VALUES.get(cell, 0)