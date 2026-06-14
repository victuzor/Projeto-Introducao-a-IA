import pytest

from src.agent import (
    aplicar_efeitos_celula,
    aplicar_movimento,
    calcular_ferro_coletado,
    calcular_penalidade_celula,
    executar_caminho,
)

from src.dungeon import (
    EMPTY,
    FRAGILE_WALL,
    GOLD,
    IRON,
    SKELETON,
    SLIME,
    WALL,
    create_default_dungeon,
)

from src.state import EstadoAgente, criar_estado_inicial


def test_calcular_penalidade_celula_vazia():
    assert calcular_penalidade_celula(EMPTY) == 0


def test_calcular_penalidade_slime():
    assert calcular_penalidade_celula(SLIME) == 30


def test_calcular_penalidade_esqueleto():
    assert calcular_penalidade_celula(SKELETON) == 40


def test_calcular_ferro_coletado():
    assert calcular_ferro_coletado(IRON) == 1
    assert calcular_ferro_coletado(GOLD) == 0


def test_aplicar_movimento_incrementa_passos():
    dungeon = create_default_dungeon()
    estado = criar_estado_inicial((0, 0))

    novo_estado = aplicar_movimento(dungeon, estado, (0, 1))

    assert novo_estado.posicao == (0, 1)
    assert novo_estado.passos == 1
    assert novo_estado.caminho == ((0, 0), (0, 1))


def test_aplicar_movimento_coleta_ferro_sem_melhorar_picareta():
    dungeon = create_default_dungeon()
    estado = criar_estado_inicial((0, 1))

    novo_estado = aplicar_movimento(dungeon, estado, (0, 2))

    assert novo_estado.posicao == (0, 2)
    assert novo_estado.passos == 1
    assert novo_estado.dinheiro == 10
    assert novo_estado.ferro == 1
    assert novo_estado.picareta_melhorada is False
    assert novo_estado.minerios_coletados == ((0, 2),)


def test_aplicar_movimento_coleta_ouro():
    dungeon = create_default_dungeon()
    estado = criar_estado_inicial((0, 3))

    novo_estado = aplicar_movimento(dungeon, estado, (0, 4))

    assert novo_estado.posicao == (0, 4)
    assert novo_estado.dinheiro == 50
    assert novo_estado.ferro == 0
    assert novo_estado.minerios_coletados == ((0, 4),)


def test_aplicar_movimento_em_slime_adiciona_penalidade():
    dungeon = create_default_dungeon()
    estado = criar_estado_inicial((0, 5))

    novo_estado = aplicar_movimento(dungeon, estado, (0, 6))

    assert novo_estado.posicao == (0, 6)
    assert novo_estado.penalidades == 30


def test_aplicar_movimento_em_esqueleto_adiciona_penalidade():
    dungeon = create_default_dungeon()
    estado = criar_estado_inicial((3, 4))

    novo_estado = aplicar_movimento(dungeon, estado, (3, 5))

    assert novo_estado.posicao == (3, 5)
    assert novo_estado.penalidades == 40


def test_nao_coleta_mesmo_minerio_duas_vezes():
    dungeon = create_default_dungeon()
    estado = criar_estado_inicial((0, 2))

    estado = aplicar_efeitos_celula(dungeon, estado)
    estado = aplicar_efeitos_celula(dungeon, estado)

    assert estado.dinheiro == 10
    assert estado.ferro == 1
    assert estado.minerios_coletados == ((0, 2),)


def test_aplicar_movimento_em_parede_comum_gera_erro():
    dungeon = create_default_dungeon()
    estado = criar_estado_inicial((1, 0))

    with pytest.raises(ValueError):
        aplicar_movimento(dungeon, estado, (1, 1))


def test_aplicar_movimento_em_parede_fragil_sem_ferro_gera_erro():
    dungeon = create_default_dungeon()
    estado = criar_estado_inicial((0, 2))

    with pytest.raises(ValueError):
        aplicar_movimento(dungeon, estado, (0, 3))


def test_aplicar_movimento_em_parede_fragil_com_picareta_melhorada():
    dungeon = create_default_dungeon()

    estado = EstadoAgente(
        posicao=(0, 2),
        picareta_melhorada=True,
        caminho=((0, 2),),
    )

    novo_estado = aplicar_movimento(dungeon, estado, (0, 3))

    assert novo_estado.posicao == (0, 3)
    assert novo_estado.passos == 1
    assert novo_estado.picareta_melhorada is True


def test_parede_comum_nao_tem_penalidade():
    assert calcular_penalidade_celula(WALL) == 0


def test_parede_fragil_nao_tem_penalidade():
    assert calcular_penalidade_celula(FRAGILE_WALL) == 0


def test_executar_caminho_vazio_retorna_estado_inicial():
    dungeon = create_default_dungeon()
    estado = criar_estado_inicial((0, 0))

    estado_final = executar_caminho(dungeon, estado, ())

    assert estado_final == estado


def test_executar_caminho_com_apenas_posicao_inicial():
    dungeon = create_default_dungeon()
    estado = criar_estado_inicial((0, 0))

    estado_final = executar_caminho(dungeon, estado, ((0, 0),))

    assert estado_final == estado


def test_executar_caminho_coleta_ferro_sem_melhorar_picareta():
    dungeon = create_default_dungeon()
    estado = criar_estado_inicial((0, 0))

    caminho = ((0, 0), (0, 1), (0, 2))
    estado_final = executar_caminho(dungeon, estado, caminho)

    assert estado_final.posicao == (0, 2)
    assert estado_final.passos == 2
    assert estado_final.dinheiro == 10
    assert estado_final.ferro == 1
    assert estado_final.picareta_melhorada is False
    assert estado_final.minerios_coletados == ((0, 2),)
    assert estado_final.caminho == caminho


def test_executar_caminho_comeca_em_posicao_errada_gera_erro():
    dungeon = create_default_dungeon()
    estado = criar_estado_inicial((0, 0))

    caminho = ((1, 0), (2, 0))

    with pytest.raises(ValueError):
        executar_caminho(dungeon, estado, caminho)


def test_executar_caminho_bloqueado_gera_erro():
    dungeon = create_default_dungeon()
    estado = criar_estado_inicial((1, 0))

    caminho = ((1, 0), (1, 1))

    with pytest.raises(ValueError):
        executar_caminho(dungeon, estado, caminho)


def test_agente_so_melhora_picareta_ao_entrar_em_parede_fragil():
    dungeon = create_default_dungeon()
    estado = criar_estado_inicial((0, 0))

    estado = aplicar_movimento(dungeon, estado, (0, 1))
    estado = aplicar_movimento(dungeon, estado, (0, 2))

    assert estado.ferro == 1
    assert estado.picareta_melhorada is False

    estado = aplicar_movimento(dungeon, estado, (0, 3))

    assert estado.ferro == 0
    assert estado.picareta_melhorada is True
    assert estado.posicao == (0, 3)


def test_executar_caminho_coleta_ferro_e_atravessa_parede_fragil():
    dungeon = create_default_dungeon()
    estado = criar_estado_inicial((0, 0))

    caminho = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4))

    estado_final = executar_caminho(dungeon, estado, caminho)

    assert estado_final.posicao == (0, 4)
    assert estado_final.passos == 4
    assert estado_final.dinheiro == 60
    assert estado_final.ferro == 0
    assert estado_final.picareta_melhorada is True
    assert estado_final.minerios_coletados == ((0, 2), (0, 4))