import pytest

from src.dungeon import (
    AGENT,
    EMPTY,
    GOLD,
    WALL,
    create_default_dungeon,
)

from src.planner import (
    calcular_utilidade_rota,
    escolher_melhor_minerio,
    localizar_minerios,
    obter_algoritmo_busca,
)

from src.search import busca_a_estrela, busca_bfs, busca_ucs


def criar_grid_sem_minerios():
    return [
        [AGENT, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    ]


def test_localizar_minerios_no_mapa_padrao():
    dungeon = create_default_dungeon()

    minerios = localizar_minerios(dungeon)

    assert (0, 2) in minerios
    assert (0, 4) in minerios
    assert (1, 7) in minerios
    assert len(minerios) > 0


def test_localizar_minerios_em_grid_sem_minerios():
    dungeon = criar_grid_sem_minerios()

    minerios = localizar_minerios(dungeon)

    assert minerios == ()


def test_calcular_utilidade_rota():
    utilidade = calcular_utilidade_rota(valor_alvo=50, custo_rota=6)

    assert utilidade == 44


def test_obter_algoritmo_busca_bfs():
    algoritmo = obter_algoritmo_busca("bfs")

    assert algoritmo == busca_bfs


def test_obter_algoritmo_busca_ucs():
    algoritmo = obter_algoritmo_busca("ucs")

    assert algoritmo == busca_ucs


def test_obter_algoritmo_busca_a_estrela():
    algoritmo = obter_algoritmo_busca("a_estrela")

    assert algoritmo == busca_a_estrela


def test_obter_algoritmo_busca_invalido():
    with pytest.raises(ValueError):
        obter_algoritmo_busca("guloso")


def test_escolher_melhor_minerio_retorna_plano():
    dungeon = create_default_dungeon()

    plano = escolher_melhor_minerio(
        dungeon,
        posicao_inicial=(0, 0),
        algoritmo="a_estrela",
    )

    assert plano is not None
    assert plano.resultado_busca.encontrou is True
    assert plano.valor_alvo > 0
    assert plano.utilidade_estimada == plano.valor_alvo - plano.resultado_busca.custo


def test_escolher_melhor_minerio_no_mapa_padrao():
    dungeon = create_default_dungeon()

    plano = escolher_melhor_minerio(
        dungeon,
        posicao_inicial=(0, 0),
        algoritmo="a_estrela",
    )

    assert plano is not None
    assert plano.alvo == (0, 4)
    assert plano.valor_alvo == 50


def test_escolher_melhor_minerio_em_grid_sem_minerios():
    dungeon = criar_grid_sem_minerios()

    plano = escolher_melhor_minerio(
        dungeon,
        posicao_inicial=(0, 0),
        algoritmo="a_estrela",
    )

    assert plano is None


def test_escolher_melhor_minerio_ignora_minerio_inacessivel():
    dungeon = [
        [AGENT, WALL, GOLD, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [WALL, WALL, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    ]

    plano = escolher_melhor_minerio(
        dungeon,
        posicao_inicial=(0, 0),
        algoritmo="a_estrela",
    )

    assert plano is None