from src.dungeon import (
    Grid,
    Position,
    get_cell,
    get_ore_value,
    is_blocked,
    is_ore,
    IRON,
    SLIME,
    SKELETON,
)

from src.state import EstadoAgente


PENALIDADES_CELULAS = {
    SLIME: 30,
    SKELETON: 40,
}


def calcular_penalidade_celula(celula: str) -> int:
    """
    Retorna a penalidade associada a uma célula.

    Slimes e esqueletos causam penalidades.
    Células vazias, paredes e minérios não causam penalidade.
    """
    return PENALIDADES_CELULAS.get(celula, 0)


def calcular_ferro_coletado(celula: str) -> int:
    """
    Retorna a quantidade de ferro coletada.

    Por simplicidade, apenas o minério Fe aumenta o inventário de ferro.
    """
    if celula == IRON:
        return 1

    return 0


def aplicar_efeitos_celula(grid: Grid, estado: EstadoAgente) -> EstadoAgente:
    """
    Aplica os efeitos da célula atual no estado do agente.

    Possíveis efeitos:
    - coletar minério;
    - ganhar dinheiro;
    - ganhar ferro;
    - sofrer penalidade.
    """
    celula = get_cell(grid, estado.posicao)
    novo_estado = estado

    if is_ore(celula):
        valor_minerio = get_ore_value(celula)
        quantidade_ferro = calcular_ferro_coletado(celula)

        novo_estado = novo_estado.coletar_minerio(
            posicao_minerio=estado.posicao,
            valor_minerio=valor_minerio,
            quantidade_ferro=quantidade_ferro,
        )

    penalidade = calcular_penalidade_celula(celula)

    if penalidade > 0:
        novo_estado = novo_estado.adicionar_penalidade(penalidade)

    return novo_estado


def aplicar_movimento(
    grid: Grid,
    estado: EstadoAgente,
    nova_posicao: Position,
) -> EstadoAgente:
    """
    Move o agente para uma nova posição e aplica os efeitos da célula de destino.

    Caso a célula esteja bloqueada, o movimento não é permitido.
    """
    celula_destino = get_cell(grid, nova_posicao)

    if is_blocked(celula_destino, estado.picareta_melhorada):
        raise ValueError("Movimento inválido: célula bloqueada.")

    estado_movido = estado.mover_para(nova_posicao)
    estado_atualizado = aplicar_efeitos_celula(grid, estado_movido)

    return estado_atualizado