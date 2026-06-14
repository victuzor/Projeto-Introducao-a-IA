from typing import Tuple

from src.dungeon import (
    FRAGILE_WALL,
    Grid,
    IRON,
    Position,
    SKELETON,
    SLIME,
    get_cell,
    get_ore_value,
    is_blocked,
    is_ore,
)

from src.risk import calcular_custo_percepcao
from src.state import EstadoAgente


Caminho = Tuple[Position, ...]


PENALIDADES_CELULAS = {
    SLIME: 30,
    SKELETON: 40,
}


def calcular_penalidade_celula(celula: str) -> int:
    """
    Retorna a penalidade associada a uma célula.

    Slimes e esqueletos causam penalidades diretas.
    Células vazias, paredes e minérios não causam penalidade direta.
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
    - sofrer penalidade direta;
    - acumular custo de risco por gosma/crack.

    O agente não melhora a picareta automaticamente ao coletar ferro.
    Ele guarda o ferro e só usa quando precisar atravessar parede frágil.
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

    custo_risco = calcular_custo_percepcao(grid, estado.posicao)

    if custo_risco > 0:
        novo_estado = novo_estado.adicionar_custo_risco(custo_risco)

    return novo_estado


def preparar_para_entrar_na_celula(
    grid: Grid,
    estado: EstadoAgente,
    nova_posicao: Position,
) -> EstadoAgente:
    """
    Prepara o agente antes de entrar em uma célula.

    Se a célula for uma parede frágil e o agente ainda não tiver picareta
    melhorada, ele só melhora a picareta nesse momento, usando 1 ferro.
    """
    celula_destino = get_cell(grid, nova_posicao)

    if celula_destino == FRAGILE_WALL and not estado.picareta_melhorada:
        if estado.ferro < 1:
            raise ValueError("Movimento inválido: parede frágil exige ferro.")

        return estado.melhorar_picareta()

    return estado


def aplicar_movimento(
    grid: Grid,
    estado: EstadoAgente,
    nova_posicao: Position,
) -> EstadoAgente:
    """
    Move o agente para uma nova posição e aplica os efeitos da célula de destino.

    Caso a célula seja parede frágil, o agente só melhora a picareta
    se realmente precisar atravessá-la.
    """
    estado_preparado = preparar_para_entrar_na_celula(
        grid=grid,
        estado=estado,
        nova_posicao=nova_posicao,
    )

    celula_destino = get_cell(grid, nova_posicao)

    if is_blocked(
        celula_destino,
        estado_preparado.picareta_melhorada,
        estado_preparado.ferro,
    ):
        raise ValueError("Movimento inválido: célula bloqueada.")

    estado_movido = estado_preparado.mover_para(nova_posicao)
    estado_atualizado = aplicar_efeitos_celula(grid, estado_movido)

    return estado_atualizado


def executar_caminho(
    grid: Grid,
    estado_inicial: EstadoAgente,
    caminho: Caminho,
) -> EstadoAgente:
    """
    Executa um caminho completo, posição por posição.

    O caminho deve começar na posição atual do agente.
    Exemplo:
    ((0, 0), (0, 1), (0, 2))
    """
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