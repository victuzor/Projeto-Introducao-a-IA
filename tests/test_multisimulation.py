from src.dungeon import AGENT, EMPTY, IRON
from src.multisimulation import (
    avancar_simulacao_algoritmo,
    criar_estado_simulacao_algoritmo,
    criar_linhas_estado_algoritmo,
    todos_finalizados,
)
from src.state import criar_estado_inicial


def criar_grid_simples():
    return [
        [AGENT, IRON, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    ]


def test_criar_estado_simulacao_algoritmo():
    estado = criar_estado_inicial((0, 0))

    simulacao = criar_estado_simulacao_algoritmo(
        nome_exibicao="A*",
        algoritmo="a_estrela",
        estado_inicial=estado,
    )

    assert simulacao.nome_exibicao == "A*"
    assert simulacao.algoritmo == "a_estrela"
    assert simulacao.estado_atual == estado
    assert simulacao.finalizado is False


def test_avancar_simulacao_algoritmo_cria_plano():
    dungeon = criar_grid_simples()
    estado = criar_estado_inicial((0, 0))
    simulacao = criar_estado_simulacao_algoritmo("A*", "a_estrela", estado)

    avancar_simulacao_algoritmo(dungeon, simulacao)

    assert simulacao.plano_atual is not None
    assert simulacao.plano_atual.alvo == (0, 1)


def test_avancar_simulacao_algoritmo_move_agente():
    dungeon = criar_grid_simples()
    estado = criar_estado_inicial((0, 0))
    simulacao = criar_estado_simulacao_algoritmo("A*", "a_estrela", estado)

    avancar_simulacao_algoritmo(dungeon, simulacao)
    avancar_simulacao_algoritmo(dungeon, simulacao)

    assert simulacao.estado_atual.posicao == (0, 1)
    assert simulacao.estado_atual.dinheiro == 10
    assert simulacao.estado_atual.minerios_coletados == ((0, 1),)


def test_criar_linhas_estado_algoritmo():
    estado = criar_estado_inicial((0, 0))
    simulacao = criar_estado_simulacao_algoritmo("BFS", "bfs", estado)

    linhas = criar_linhas_estado_algoritmo(simulacao)

    assert "Posição: (0, 0)" in linhas
    assert "Passos: 0" in linhas
    assert "Score: 0" in linhas


def test_todos_finalizados():
    estado = criar_estado_inicial((0, 0))

    s1 = criar_estado_simulacao_algoritmo("BFS", "bfs", estado)
    s2 = criar_estado_simulacao_algoritmo("UCS", "ucs", estado)

    assert todos_finalizados((s1, s2)) is False

    s1.finalizado = True
    s2.finalizado = True

    assert todos_finalizados((s1, s2)) is True