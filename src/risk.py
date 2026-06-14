from src.dungeon import (
    CRACK_PERCEPTION,
    GOO_PERCEPTION,
    Grid,
    Position,
    get_perceptions,
)


CUSTO_PERCEPCAO_GOSMA = 3
CUSTO_PERCEPCAO_CRACK = 4


def calcular_custo_percepcao(grid: Grid, posicao: Position) -> int:
    """
    Calcula o custo extra causado pelas percepções de risco.

    A ideia é representar a cautela do agente:

    - gosma: o chão está escorregadio ou suspeito;
    - crack: o agente ouve sinais de esqueleto e anda mais devagar.

    Esse custo é diferente da penalidade direta de cair em um monstro.
    Ele representa lentidão/cautela ao passar por áreas suspeitas.
    """
    percepcoes = get_perceptions(grid, posicao)

    custo = 0

    if GOO_PERCEPTION in percepcoes:
        custo += CUSTO_PERCEPCAO_GOSMA

    if CRACK_PERCEPTION in percepcoes:
        custo += CUSTO_PERCEPCAO_CRACK

    return custo