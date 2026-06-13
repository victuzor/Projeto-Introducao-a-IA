from src.comparison import (
    comparar_algoritmos,
    avaliar_algoritmo,
    formatar_resultado_comparacao,
)

from src.dungeon import (
    AGENT,
    EMPTY,
    GOLD,
    WALL,
    create_default_dungeon,
)

from src.search import busca_bfs


def criar_grid_simples():
    return [
        [AGENT, EMPTY, GOLD, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    ]


def test_avaliar_algoritmo_bfs():
    dungeon = criar_grid_simples()

    resultado = avaliar_algoritmo(
        nome_algoritmo="BFS",
        funcao_busca=busca_bfs,
        grid=dungeon,
        posicao_inicial=(0, 0),
        posicao_objetivo=(0, 2),
    )

    assert resultado.algoritmo == "BFS"
    assert resultado.encontrou is True
    assert resultado.caminho == ((0, 0), (0, 1), (0, 2))
    assert resultado.custo_busca == 2
    assert resultado.passos == 2
    assert resultado.dinheiro == 50
    assert resultado.score_final == 48
    assert resultado.nos_expandidos > 0
    assert resultado.tempo_execucao >= 0


def test_comparar_algoritmos_retorna_tres_resultados():
    dungeon = criar_grid_simples()

    resultados = comparar_algoritmos(
        grid=dungeon,
        posicao_inicial=(0, 0),
        posicao_objetivo=(0, 2),
    )

    assert len(resultados) == 3
    assert resultados[0].algoritmo == "BFS"
    assert resultados[1].algoritmo == "UCS"
    assert resultados[2].algoritmo == "A*"


def test_comparar_algoritmos_todos_encontram_caminho_simples():
    dungeon = criar_grid_simples()

    resultados = comparar_algoritmos(
        grid=dungeon,
        posicao_inicial=(0, 0),
        posicao_objetivo=(0, 2),
    )

    for resultado in resultados:
        assert resultado.encontrou is True
        assert resultado.dinheiro == 50
        assert resultado.passos == 2
        assert resultado.score_final == 48


def test_avaliar_algoritmo_sem_caminho():
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

    resultado = avaliar_algoritmo(
        nome_algoritmo="BFS",
        funcao_busca=busca_bfs,
        grid=dungeon,
        posicao_inicial=(0, 0),
        posicao_objetivo=(0, 2),
    )

    assert resultado.encontrou is False
    assert resultado.caminho == ()
    assert resultado.dinheiro == 0
    assert resultado.score_final == 0


def test_formatar_resultado_comparacao():
    dungeon = create_default_dungeon()

    resultado = avaliar_algoritmo(
        nome_algoritmo="BFS",
        funcao_busca=busca_bfs,
        grid=dungeon,
        posicao_inicial=(0, 0),
        posicao_objetivo=(0, 2),
    )

    texto = formatar_resultado_comparacao(resultado)

    assert "Algoritmo: BFS" in texto
    assert "Encontrou caminho: True" in texto
    assert "Nós expandidos:" in texto
    assert "Score final:" in texto