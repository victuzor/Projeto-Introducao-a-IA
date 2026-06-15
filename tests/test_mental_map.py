from src.dungeon import (
    AGENT,
    EMPTY,
    FRAGILE_WALL,
    GOLD,
    GRID_SIZE,
    IRON,
    SKELETON,
    SLIME,
    WALL,
    create_default_dungeon,
)
from src.mental_map import (
    CUSTO_CELULA_DESCONHECIDA,
    CUSTO_SUSPEITA_SLIME,
    SUSPECT_SLIME,
    UNKNOWN,
    atualizar_mapa_mental,
    calcular_custos_risco_mapa_mental,
    contar_celulas_conhecidas,
    criar_grid_planejamento,
    criar_grid_visual_mapa_mental,
    criar_mapa_mental_inicial,
)


def criar_grid_vazio():
    return [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


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


def test_atualizar_mapa_mental_nao_revela_casas_vazias_quando_ha_risco():
    dungeon = criar_grid_vazio()
    dungeon[3][3] = AGENT
    dungeon[3][4] = SLIME

    mapa = criar_mapa_mental_inicial(dungeon, (3, 3))

    assert mapa.celulas_conhecidas[2][3] == UNKNOWN
    assert mapa.celulas_conhecidas[4][3] == UNKNOWN
    assert mapa.celulas_conhecidas[3][2] == UNKNOWN
    assert mapa.celulas_conhecidas[3][4] == UNKNOWN


def test_atualizar_mapa_mental_marca_todos_vizinhos_desconhecidos_como_suspeitos():
    dungeon = criar_grid_vazio()
    dungeon[3][3] = AGENT
    dungeon[3][4] = SLIME

    mapa = criar_mapa_mental_inicial(dungeon, (3, 3))

    assert (2, 3) in mapa.suspeita_slime
    assert (4, 3) in mapa.suspeita_slime
    assert (3, 2) in mapa.suspeita_slime
    assert (3, 4) in mapa.suspeita_slime


def test_atualizar_mapa_mental_revela_slime_quando_agente_pisa_nele():
    dungeon = create_default_dungeon()
    mapa = criar_mapa_mental_inicial(dungeon, (0, 0))

    mapa = atualizar_mapa_mental(mapa, dungeon, (0, 6))

    assert mapa.celulas_conhecidas[0][6] == SLIME


def test_atualizar_mapa_mental_revela_esqueleto_quando_agente_pisa_nele():
    dungeon = create_default_dungeon()
    mapa = criar_mapa_mental_inicial(dungeon, (0, 0))

    mapa = atualizar_mapa_mental(mapa, dungeon, (3, 5))

    assert mapa.celulas_conhecidas[3][5] == SKELETON


def test_criar_grid_planejamento_trata_desconhecido_como_livre():
    dungeon = create_default_dungeon()
    mapa = criar_mapa_mental_inicial(dungeon, (0, 0))

    grid_planejamento = criar_grid_planejamento(mapa)

    assert grid_planejamento[0][6] == EMPTY


def test_criar_grid_planejamento_bloqueia_slime_conhecido():
    dungeon = create_default_dungeon()
    mapa = criar_mapa_mental_inicial(dungeon, (0, 0))
    mapa = atualizar_mapa_mental(mapa, dungeon, (0, 6))

    grid_planejamento = criar_grid_planejamento(mapa)

    assert grid_planejamento[0][6] == WALL


def test_criar_grid_planejamento_bloqueia_esqueleto_conhecido():
    dungeon = create_default_dungeon()
    mapa = criar_mapa_mental_inicial(dungeon, (0, 0))
    mapa = atualizar_mapa_mental(mapa, dungeon, (3, 5))

    grid_planejamento = criar_grid_planejamento(mapa)

    assert grid_planejamento[3][5] == WALL


def test_calcular_custos_risco_mapa_mental_tem_custo_para_desconhecido():
    dungeon = create_default_dungeon()
    mapa = criar_mapa_mental_inicial(dungeon, (0, 0))

    custos = calcular_custos_risco_mapa_mental(mapa)

    assert custos[(0, 6)] == CUSTO_CELULA_DESCONHECIDA


def test_calcular_custos_risco_mapa_mental_acumula_incerteza_e_suspeita():
    dungeon = create_default_dungeon()
    mapa = criar_mapa_mental_inicial(dungeon, (0, 0))
    mapa = atualizar_mapa_mental(mapa, dungeon, (0, 5))

    custos = calcular_custos_risco_mapa_mental(mapa)

    assert custos[(0, 6)] == CUSTO_CELULA_DESCONHECIDA + CUSTO_SUSPEITA_SLIME


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

    assert SUSPECT_SLIME in simbolos or "!?" in simbolos


def test_contar_celulas_conhecidas():
    dungeon = create_default_dungeon()
    mapa = criar_mapa_mental_inicial(dungeon, (0, 0))

    assert contar_celulas_conhecidas(mapa) > 0