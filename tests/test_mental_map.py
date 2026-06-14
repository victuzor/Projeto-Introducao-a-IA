from src.dungeon import AGENT, EMPTY, FRAGILE_WALL, GOLD, IRON, create_default_dungeon
from src.mental_map import (
    SUSPECT_SLIME,
    UNKNOWN,
    atualizar_mapa_mental,
    calcular_custos_risco_mapa_mental,
    contar_celulas_conhecidas,
    criar_grid_planejamento,
    criar_grid_visual_mapa_mental,
    criar_mapa_mental_inicial,
)


def test_mapa_mental_inicial_conhece_minerios_e_posicao_inicial():
    dungeon = create_default_dungeon()

    mapa = criar_mapa_mental_inicial(dungeon, (0, 0))

    assert mapa.celulas_conhecidas[0][0] == AGENT
    assert mapa.celulas_conhecidas[0][2] == IRON
    assert mapa.celulas_conhecidas[0][4] == GOLD


def test_mapa_mental_inicial_nao_revela_monstros_distantes():
    dungeon = create_default_dungeon()

    mapa = criar_mapa_mental_inicial(dungeon, (0, 0))

    assert mapa.celulas_conhecidas[0][6] == UNKNOWN


def test_atualizar_mapa_mental_revela_parede_adjacente():
    dungeon = create_default_dungeon()
    mapa = criar_mapa_mental_inicial(dungeon, (0, 0))

    mapa = atualizar_mapa_mental(mapa, dungeon, (0, 2))

    assert mapa.celulas_conhecidas[0][3] == FRAGILE_WALL
    assert mapa.celulas_conhecidas[1][2] == EMPTY


def test_criar_grid_planejamento_trata_desconhecido_como_livre():
    dungeon = create_default_dungeon()
    mapa = criar_mapa_mental_inicial(dungeon, (0, 0))

    grid_planejamento = criar_grid_planejamento(mapa)

    assert grid_planejamento[0][6] == EMPTY


def test_calcular_custos_risco_mapa_mental():
    dungeon = create_default_dungeon()
    mapa = criar_mapa_mental_inicial(dungeon, (0, 0))
    mapa = atualizar_mapa_mental(mapa, dungeon, (0, 5))

    custos = calcular_custos_risco_mapa_mental(mapa)

    assert len(custos) > 0


def test_criar_grid_visual_mapa_mental_exibe_suspeitas():
    dungeon = create_default_dungeon()
    mapa = criar_mapa_mental_inicial(dungeon, (0, 0))
    mapa = atualizar_mapa_mental(mapa, dungeon, (0, 5))

    grid_visual = criar_grid_visual_mapa_mental(
        mapa_mental=mapa,
        posicao_agente=(0, 5),
    )

    simbolos = {celula for linha in grid_visual for celula in linha}

    assert SUSPECT_SLIME in simbolos or "GC" in simbolos


def test_contar_celulas_conhecidas():
    dungeon = create_default_dungeon()
    mapa = criar_mapa_mental_inicial(dungeon, (0, 0))

    assert contar_celulas_conhecidas(mapa) > 0