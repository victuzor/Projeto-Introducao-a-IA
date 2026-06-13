from src.dungeon import create_default_dungeon
from src.search import busca_bfs, formatar_caminho, obter_proxima_posicao


def test_bfs_encontra_caminho_para_ferro_proximo():
    dungeon = create_default_dungeon()

    resultado = busca_bfs(
        dungeon,
        posicao_inicial=(0, 0),
        posicao_objetivo=(0, 2),
    )

    assert resultado.encontrou is True
    assert resultado.caminho == ((0, 0), (0, 1), (0, 2))
    assert resultado.custo == 2
    assert resultado.nos_expandidos > 0


def test_bfs_retorna_caminho_zero_quando_inicio_igual_objetivo():
    dungeon = create_default_dungeon()

    resultado = busca_bfs(
        dungeon,
        posicao_inicial=(0, 0),
        posicao_objetivo=(0, 0),
    )

    assert resultado.encontrou is True
    assert resultado.caminho == ((0, 0),)
    assert resultado.custo == 0


def test_bfs_nao_atravessa_parede_comum():
    dungeon = create_default_dungeon()

    resultado = busca_bfs(
        dungeon,
        posicao_inicial=(1, 0),
        posicao_objetivo=(1, 1),
    )

    assert resultado.encontrou is False
    assert resultado.caminho == ()


def test_bfs_nao_atravessa_parede_fragil_sem_picareta():
    dungeon = create_default_dungeon()

    resultado = busca_bfs(
        dungeon,
        posicao_inicial=(0, 2),
        posicao_objetivo=(0, 3),
        picareta_melhorada=False,
    )

    assert resultado.encontrou is False


def test_bfs_atravessa_parede_fragil_com_picareta():
    dungeon = create_default_dungeon()

    resultado = busca_bfs(
        dungeon,
        posicao_inicial=(0, 2),
        posicao_objetivo=(0, 3),
        picareta_melhorada=True,
    )

    assert resultado.encontrou is True
    assert resultado.caminho == ((0, 2), (0, 3))
    assert resultado.custo == 1


def test_formatar_caminho():
    caminho = ((0, 0), (0, 1), (0, 2))

    texto = formatar_caminho(caminho)

    assert texto == "(0, 0) -> (0, 1) -> (0, 2)"


def test_formatar_caminho_vazio():
    texto = formatar_caminho(())

    assert texto == "Nenhum caminho encontrado."


def test_obter_proxima_posicao():
    caminho = ((0, 0), (0, 1), (0, 2))

    proxima = obter_proxima_posicao(caminho)

    assert proxima == (0, 1)


def test_obter_proxima_posicao_caminho_curto():
    caminho = ((0, 0),)

    proxima = obter_proxima_posicao(caminho)

    assert proxima is None