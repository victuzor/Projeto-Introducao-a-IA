from src.dungeon import AGENT, EMPTY, IRON, create_default_dungeon
from src.render import ROUTE, criar_grid_com_caminho


def test_criar_grid_com_caminho_marca_posicoes_intermediarias():
    dungeon = create_default_dungeon()

    caminho = ((0, 0), (0, 1), (0, 2))
    grid_visual = criar_grid_com_caminho(dungeon, caminho)

    assert grid_visual[0][0] == AGENT
    assert grid_visual[0][1] == ROUTE
    assert grid_visual[0][2] == IRON


def test_criar_grid_com_caminho_nao_altera_grid_original():
    dungeon = create_default_dungeon()

    caminho = ((0, 0), (0, 1), (0, 2))
    grid_visual = criar_grid_com_caminho(dungeon, caminho)

    assert dungeon[0][1] == EMPTY
    assert grid_visual[0][1] == ROUTE


def test_criar_grid_com_caminho_vazio_retorna_copia_do_grid():
    dungeon = create_default_dungeon()

    grid_visual = criar_grid_com_caminho(dungeon, ())

    assert grid_visual == dungeon
    assert grid_visual is not dungeon
    assert grid_visual[0] is not dungeon[0]