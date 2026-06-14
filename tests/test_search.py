from src.dungeon import (
    AGENT,
    EMPTY,
    FRAGILE_WALL,
    GOLD,
    IRON,
    SLIME,
    WALL,
    create_default_dungeon,
)

from src.search import (
    EstadoPlanejamento,
    atualizar_estado_planejamento,
    busca_a_estrela,
    busca_bfs,
    busca_ucs,
    calcular_custo_movimento,
    calcular_custo_percepcao,
    calcular_heuristica_manhattan,
    criar_estado_planejamento_inicial,
    formatar_caminho,
    obter_proxima_posicao,
)


def criar_grid_teste_ucs():
    return [
        [AGENT, SLIME, GOLD, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, WALL, WALL, WALL, WALL, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    ]


def criar_grid_parede_fragil_sem_ferro():
    return [
        [AGENT, FRAGILE_WALL, GOLD, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [WALL, WALL, WALL, WALL, WALL, WALL, WALL, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY],
    ]


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


def test_calcular_custo_percepcao_sem_percepcao():
    dungeon = create_default_dungeon()

    custo = calcular_custo_percepcao(dungeon, (0, 1))

    assert custo == 0


def test_calcular_custo_percepcao_gosma():
    dungeon = create_default_dungeon()

    custo = calcular_custo_percepcao(dungeon, (0, 5))

    assert custo == 3


def test_calcular_custo_percepcao_crack():
    dungeon = create_default_dungeon()

    custo = calcular_custo_percepcao(dungeon, (3, 4))

    assert custo == 4


def test_calcular_custo_movimento_celula_vazia():
    dungeon = criar_grid_teste_ucs()

    custo = calcular_custo_movimento(dungeon, (1, 0))

    assert custo == 1


def test_calcular_custo_movimento_celula_com_gosma():
    dungeon = create_default_dungeon()

    custo = calcular_custo_movimento(dungeon, (0, 5))

    assert custo == 4


def test_calcular_custo_movimento_celula_com_crack():
    dungeon = create_default_dungeon()

    custo = calcular_custo_movimento(dungeon, (3, 4))

    assert custo == 5


def test_calcular_custo_movimento_slime():
    dungeon = criar_grid_teste_ucs()

    custo = calcular_custo_movimento(dungeon, (0, 1))

    assert custo == 31


def test_calcular_custo_movimento_parede_fragil():
    dungeon = [
        [AGENT, FRAGILE_WALL, GOLD, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    ]

    custo = calcular_custo_movimento(dungeon, (0, 1))

    assert custo == 2


def test_criar_estado_planejamento_inicial_marca_ferro_da_posicao_inicial():
    dungeon = create_default_dungeon()

    estado = criar_estado_planejamento_inicial(
        grid=dungeon,
        posicao_inicial=(0, 2),
        picareta_melhorada=False,
        ferro_inicial=0,
    )

    assert estado.posicao == (0, 2)
    assert estado.ferro == 0
    assert estado.picareta_melhorada is False
    assert estado.ferros_coletados == ((0, 2),)


def test_ucs_encontra_caminho_para_ferro_proximo():
    dungeon = create_default_dungeon()

    resultado = busca_ucs(
        dungeon,
        posicao_inicial=(0, 0),
        posicao_objetivo=(0, 2),
    )

    assert resultado.encontrou is True
    assert resultado.caminho == ((0, 0), (0, 1), (0, 2))
    assert resultado.custo == 2
    assert resultado.nos_expandidos > 0


def test_ucs_evitar_caminho_com_slime_quando_existe_caminho_mais_barato():
    dungeon = criar_grid_teste_ucs()

    resultado = busca_ucs(
        dungeon,
        posicao_inicial=(0, 0),
        posicao_objetivo=(0, 2),
    )

    assert resultado.encontrou is True
    assert (0, 1) not in resultado.caminho
    assert resultado.custo == 9


def test_ucs_nao_atravessa_parede_fragil_sem_picareta_ou_ferro():
    dungeon = criar_grid_parede_fragil_sem_ferro()

    resultado = busca_ucs(
        dungeon,
        posicao_inicial=(0, 0),
        posicao_objetivo=(0, 2),
        picareta_melhorada=False,
        ferro_inicial=0,
    )

    assert resultado.encontrou is False


def test_ucs_atravessa_parede_fragil_com_picareta():
    dungeon = create_default_dungeon()

    resultado = busca_ucs(
        dungeon,
        posicao_inicial=(0, 2),
        posicao_objetivo=(0, 3),
        picareta_melhorada=True,
    )

    assert resultado.encontrou is True
    assert resultado.caminho == ((0, 2), (0, 3))
    assert resultado.custo == 2


def test_calcular_heuristica_manhattan_mesma_posicao():
    distancia = calcular_heuristica_manhattan((0, 0), (0, 0))

    assert distancia == 0


def test_calcular_heuristica_manhattan_posicoes_diferentes():
    distancia = calcular_heuristica_manhattan((0, 0), (3, 4))

    assert distancia == 7


def test_a_estrela_encontra_caminho_para_ferro_proximo():
    dungeon = create_default_dungeon()

    resultado = busca_a_estrela(
        dungeon,
        posicao_inicial=(0, 0),
        posicao_objetivo=(0, 2),
    )

    assert resultado.encontrou is True
    assert resultado.caminho == ((0, 0), (0, 1), (0, 2))
    assert resultado.custo == 2
    assert resultado.nos_expandidos > 0


def test_a_estrela_evitar_caminho_com_slime_quando_existe_caminho_mais_barato():
    dungeon = criar_grid_teste_ucs()

    resultado = busca_a_estrela(
        dungeon,
        posicao_inicial=(0, 0),
        posicao_objetivo=(0, 2),
    )

    assert resultado.encontrou is True
    assert (0, 1) not in resultado.caminho
    assert resultado.custo == 9


def test_a_estrela_nao_atravessa_parede_fragil_sem_picareta_ou_ferro():
    dungeon = criar_grid_parede_fragil_sem_ferro()

    resultado = busca_a_estrela(
        dungeon,
        posicao_inicial=(0, 0),
        posicao_objetivo=(0, 2),
        picareta_melhorada=False,
        ferro_inicial=0,
    )

    assert resultado.encontrou is False


def test_a_estrela_atravessa_parede_fragil_com_picareta():
    dungeon = create_default_dungeon()

    resultado = busca_a_estrela(
        dungeon,
        posicao_inicial=(0, 2),
        posicao_objetivo=(0, 3),
        picareta_melhorada=True,
    )

    assert resultado.encontrou is True
    assert resultado.caminho == ((0, 2), (0, 3))
    assert resultado.custo == 2


def test_planejamento_guarda_ferro_ate_precisar_da_picareta():
    dungeon = create_default_dungeon()

    estado = EstadoPlanejamento(
        posicao=(0, 1),
        ferro=0,
        picareta_melhorada=False,
    )

    estado_com_ferro = atualizar_estado_planejamento(
        grid=dungeon,
        estado_atual=estado,
        nova_posicao=(0, 2),
    )

    assert estado_com_ferro.posicao == (0, 2)
    assert estado_com_ferro.ferro == 1
    assert estado_com_ferro.picareta_melhorada is False

    estado_com_picareta = atualizar_estado_planejamento(
        grid=dungeon,
        estado_atual=estado_com_ferro,
        nova_posicao=(0, 3),
    )

    assert estado_com_picareta.posicao == (0, 3)
    assert estado_com_picareta.ferro == 0
    assert estado_com_picareta.picareta_melhorada is True


def test_ucs_planeja_coletar_ferro_para_atravessar_parede_fragil():
    dungeon = create_default_dungeon()

    resultado = busca_ucs(
        dungeon,
        posicao_inicial=(0, 0),
        posicao_objetivo=(0, 4),
        picareta_melhorada=False,
        ferro_inicial=0,
    )

    assert resultado.encontrou is True
    assert resultado.caminho == ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4))
    assert resultado.custo == 5


def test_a_estrela_planeja_coletar_ferro_para_atravessar_parede_fragil():
    dungeon = create_default_dungeon()

    resultado = busca_a_estrela(
        dungeon,
        posicao_inicial=(0, 0),
        posicao_objetivo=(0, 4),
        picareta_melhorada=False,
        ferro_inicial=0,
    )

    assert resultado.encontrou is True
    assert resultado.caminho == ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4))
    assert resultado.custo == 5