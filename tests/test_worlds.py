import pytest

from src.dungeon import (
    AGENT,
    FRAGILE_WALL,
    GOLD,
    GRID_SIZE,
    IRON,
    find_agent_position,
)
from src.worlds import (
    MAX_WORLD_NUMBER,
    MIN_WORLD_NUMBER,
    criar_mundo,
    criar_mundo_com_metadados,
    escolher_numero_mundo_aleatorio,
    listar_mundos_disponiveis,
    validar_numero_mundo,
)


def contar_celula(grid, simbolo):
    total = 0

    for linha in grid:
        for celula in linha:
            if celula == simbolo:
                total += 1

    return total


def test_criar_mundo_tem_tamanho_8x8():
    grid = criar_mundo(1)

    assert len(grid) == GRID_SIZE

    for linha in grid:
        assert len(linha) == GRID_SIZE


def test_criar_mundo_tem_um_agente():
    grid = criar_mundo(1)

    assert contar_celula(grid, AGENT) == 1
    assert find_agent_position(grid) == (0, 0)


def test_criar_mundo_tem_ferro_parede_fragil_e_ouro():
    grid = criar_mundo(1)

    assert contar_celula(grid, IRON) >= 1
    assert contar_celula(grid, FRAGILE_WALL) >= 1
    assert contar_celula(grid, GOLD) >= 1


def test_criar_mundo_e_deterministico_para_mesmo_numero():
    mundo_a = criar_mundo(7)
    mundo_b = criar_mundo(7)

    assert mundo_a == mundo_b


def test_mundos_diferentes_tendem_a_ser_diferentes():
    mundo_1 = criar_mundo(1)
    mundo_2 = criar_mundo(2)

    assert mundo_1 != mundo_2


def test_criar_mundo_com_metadados():
    mundo = criar_mundo_com_metadados(3)

    assert mundo.numero == 3
    assert len(mundo.grid) == GRID_SIZE
    assert mundo.alvo_principal is not None


def test_validar_numero_mundo_aceita_limites():
    validar_numero_mundo(MIN_WORLD_NUMBER)
    validar_numero_mundo(MAX_WORLD_NUMBER)


def test_validar_numero_mundo_recusa_numero_abaixo_do_limite():
    with pytest.raises(ValueError):
        validar_numero_mundo(MIN_WORLD_NUMBER - 1)


def test_validar_numero_mundo_recusa_numero_acima_do_limite():
    with pytest.raises(ValueError):
        validar_numero_mundo(MAX_WORLD_NUMBER + 1)


def test_listar_mundos_disponiveis():
    mundos = listar_mundos_disponiveis()

    assert mundos[0] == MIN_WORLD_NUMBER
    assert mundos[-1] == MAX_WORLD_NUMBER
    assert len(mundos) == MAX_WORLD_NUMBER


def test_escolher_numero_mundo_aleatorio_retorna_numero_valido():
    for _ in range(100):
        numero = escolher_numero_mundo_aleatorio()

        assert MIN_WORLD_NUMBER <= numero <= MAX_WORLD_NUMBER


def test_todos_os_mundos_validos_sao_gerados():
    for numero in listar_mundos_disponiveis():
        grid = criar_mundo(numero)

        assert len(grid) == GRID_SIZE
        assert contar_celula(grid, AGENT) == 1
        assert contar_celula(grid, GOLD) >= 1