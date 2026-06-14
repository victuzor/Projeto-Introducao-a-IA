from src.dungeon import AGENT, COPPER, EMPTY, GOLD, IRON
from src.mission import executar_missao_coleta, formatar_planos_executados
from src.state import criar_estado_inicial


def criar_grid_coleta_simples():
    return [
        [AGENT, IRON, COPPER, GOLD, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    ]


def criar_grid_minerio_longe_sem_utilidade():
    return [
        [AGENT, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, IRON],
    ]


def test_executar_missao_coleta_minerios_enquanto_utilidade_positiva():
    dungeon = criar_grid_coleta_simples()
    estado = criar_estado_inicial((0, 0))

    resultado = executar_missao_coleta(
        grid=dungeon,
        estado_inicial=estado,
        algoritmo="a_estrela",
        utilidade_minima=1,
    )

    assert resultado.estado_final.posicao == (0, 3)
    assert resultado.estado_final.passos == 3
    assert resultado.estado_final.dinheiro == 80
    assert resultado.estado_final.ferro == 1
    assert resultado.estado_final.picareta_melhorada is False
    assert resultado.estado_final.minerios_coletados == ((0, 1), (0, 2), (0, 3))
    assert resultado.score.score_final == 77


def test_executar_missao_para_quando_utilidade_nao_e_positiva():
    dungeon = criar_grid_minerio_longe_sem_utilidade()
    estado = criar_estado_inicial((0, 0))

    resultado = executar_missao_coleta(
        grid=dungeon,
        estado_inicial=estado,
        algoritmo="a_estrela",
        utilidade_minima=1,
    )

    assert resultado.estado_final == estado
    assert resultado.planos_executados == ()
    assert resultado.motivo_parada == "Próxima coleta não possui utilidade positiva."


def test_formatar_planos_executados_sem_planos():
    linhas = formatar_planos_executados(())

    assert linhas == ["Nenhuma rota de coleta foi executada."]


def test_formatar_planos_executados_com_planos():
    dungeon = criar_grid_coleta_simples()
    estado = criar_estado_inicial((0, 0))

    resultado = executar_missao_coleta(
        grid=dungeon,
        estado_inicial=estado,
        algoritmo="a_estrela",
    )

    linhas = formatar_planos_executados(resultado.planos_executados)

    assert len(linhas) > 0
    assert "Alvo" in linhas[0]
    assert "Utilidade" in linhas[0]