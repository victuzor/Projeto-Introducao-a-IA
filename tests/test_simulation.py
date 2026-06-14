from src.dungeon import AGENT, EMPTY, IRON, create_default_dungeon
from src.render import ROUTE
from src.simulation import criar_grid_simulacao, criar_linhas_estado
from src.state import criar_estado_inicial


def test_criar_grid_simulacao_move_agente_visualmente():
    dungeon = create_default_dungeon()

    grid_visual = criar_grid_simulacao(
        grid=dungeon,
        posicao_agente=(0, 1),
        caminho_percorrido=((0, 0), (0, 1)),
    )

    assert grid_visual[0][0] == ROUTE
    assert grid_visual[0][1] == AGENT


def test_criar_grid_simulacao_preserva_alvo_final_planejado():
    dungeon = create_default_dungeon()

    grid_visual = criar_grid_simulacao(
        grid=dungeon,
        posicao_agente=(0, 0),
        caminho_planejado=((0, 0), (0, 1), (0, 2)),
    )

    assert grid_visual[0][1] == ROUTE
    assert grid_visual[0][2] == IRON


def test_criar_grid_simulacao_remove_agente_original():
    dungeon = create_default_dungeon()

    grid_visual = criar_grid_simulacao(
        grid=dungeon,
        posicao_agente=(1, 0),
        caminho_percorrido=((0, 0), (1, 0)),
    )

    assert grid_visual[0][0] == ROUTE
    assert grid_visual[1][0] == AGENT


def test_criar_linhas_estado():
    estado = criar_estado_inicial((0, 0))

    linhas = criar_linhas_estado(estado)

    assert "Posição: (0, 0)" in linhas
    assert "Passos: 0" in linhas
    assert "Dinheiro: 0" in linhas
    assert "Picareta: básica" in linhas
    assert "Score parcial: 0" in linhas