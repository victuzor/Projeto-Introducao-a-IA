from typing import List, Tuple

from src.dungeon import Grid, Position, get_cell, get_neighbors, is_blocked

Action = Tuple[str, Position]


def get_valid_moves(
    grid: Grid,
    position: Position,
    picareta_melhorada: bool = False,
) -> List[Action]:
    """
    Retorna os movimentos válidos do agente a partir da posição atual.

    O agente pode se mover para cima, baixo, esquerda e direita,
    desde que a célula esteja dentro do mapa e não esteja bloqueada.

    Parede comum sempre bloqueia.
    Parede frágil só pode ser atravessada com picareta melhorada.
    """
    valid_moves = []

    neighbors = get_neighbors(position)

    for neighbor in neighbors:
        cell = get_cell(grid, neighbor)

        if not is_blocked(cell, picareta_melhorada):
            action_name = get_action_name(position, neighbor)
            valid_moves.append((action_name, neighbor))

    return valid_moves


def get_action_name(current_position: Position, next_position: Position) -> str:
    """
    Retorna o nome da ação com base na posição atual e na próxima posição.
    """
    current_row, current_col = current_position
    next_row, next_col = next_position

    if next_row < current_row:
        return "mover_cima"

    if next_row > current_row:
        return "mover_baixo"

    if next_col < current_col:
        return "mover_esquerda"

    if next_col > current_col:
        return "mover_direita"

    return "ficar_parado"