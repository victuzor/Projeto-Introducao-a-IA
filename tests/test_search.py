from src.dungeon import (
    AGENT,
    EMPTY,
    FRAGILE_WALL,
    GOLD,
    SLIME,
    WALL,
    create_default_dungeon,
)

from src.search import (
    busca_bfs,
    busca_ucs,
    calcular_custo_movimento,
    formatar_caminho,
    obter_proxima_posicao,
)

def criar_grid_teste_ucs():
    return [
        [AGENT, SLIME, GOLD, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, WALL, WALL, WALL, WALL, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    ]


def test_calcular_custo_movimento_celula_vazia():
    dungeon = criar_grid_teste_ucs()

    custo = calcular_custo_movimento(dungeon, (1, 0))

    assert custo == 1


def test_calcular_custo_movimento_slime():
    dungeon = criar_grid_teste_ucs()

    custo = calcular_custo_movimento(dungeon, (0, 1))

    assert custo == 31


def test_calcular_custo_movimento_parede_fragil():
    dungeon = [
        [AGENT, FRAGILE_WALL, GOLD, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    ]

    custo = calcular_custo_movimento(dungeon, (0, 1))

    assert custo == 6


def test_ucs_encontra_caminho_para_ferro_proximo():
    dungeon = create_default_dungeon()

    resultado = busca_ucs(
        dungeon,
        posicao_inicial=(0, 0),
        posicao_objetivo=(0, 2),
    )

    assert resultado.encontrou is True
    assert resultado.caminho == ((0, 0), (0, 1), (0, 2))
    assert resultado.custo == 2
    assert resultado.nos_expandidos > 0


def test_ucs_evitar_caminho_com_slime_quando_existe_caminho_mais_barato():
    dungeon = criar_grid_teste_ucs()

    resultado = busca_ucs(
        dungeon,
        posicao_inicial=(0, 0),
        posicao_objetivo=(0, 2),
    )

    assert resultado.encontrou is True
    assert (0, 1) not in resultado.caminho
    assert resultado.custo == 4


def test_ucs_nao_atravessa_parede_fragil_sem_picareta():
    dungeon = create_default_dungeon()

    resultado = busca_ucs(
        dungeon,
        posicao_inicial=(0, 2),
        posicao_objetivo=(0, 3),
        picareta_melhorada=False,
    )

    assert resultado.encontrou is False


def test_ucs_atravessa_parede_fragil_com_picareta():
    dungeon = create_default_dungeon()

    resultado = busca_ucs(
        dungeon,
        posicao_inicial=(0, 2),
        posicao_objetivo=(0, 3),
        picareta_melhorada=True,
    )

    assert resultado.encontrou is True
    assert resultado.caminho == ((0, 2), (0, 3))
    assert resultado.custo == 6