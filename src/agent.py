from typing import Tuple

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


Caminho = Tuple[Position, ...]


PENALIDADES_CELULAS = {
    SLIME: 30,
    SKELETON: 40,
}


def calcular_penalidade_celula(celula: str) -> int:
    return PENALIDADES_CELULAS.get(celula, 0)


def calcular_ferro_coletado(celula: str) -> int:
    if celula == IRON:
        return 1

    return 0


def aplicar_efeitos_celula(grid: Grid, estado: EstadoAgente) -> EstadoAgente:
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
    celula_destino = get_cell(grid, nova_posicao)

    if is_blocked(celula_destino, estado.picareta_melhorada):
        raise ValueError("Movimento inválido: célula bloqueada.")

    estado_movido = estado.mover_para(nova_posicao)
    estado_atualizado = aplicar_efeitos_celula(grid, estado_movido)

    return estado_atualizado


def executar_caminho(
    grid: Grid,
    estado_inicial: EstadoAgente,
    caminho: Caminho,
) -> EstadoAgente:

    if not caminho:
        return estado_inicial

    if caminho[0] != estado_inicial.posicao:
        raise ValueError("O caminho não começa na posição atual do agente.")

    estado_atual = estado_inicial

    for proxima_posicao in caminho[1:]:
        estado_atual = aplicar_movimento(
            grid=grid,
            estado=estado_atual,
            nova_posicao=proxima_posicao,
        )

    return estado_atual