from src.state import EstadoAgente, criar_estado_inicial


def test_criar_estado_inicial():
    estado = criar_estado_inicial((0, 0))

    assert estado.posicao == (0, 0)
    assert estado.passos == 0
    assert estado.dinheiro == 0
    assert estado.ferro == 0
    assert estado.penalidades == 0
    assert estado.minerios_coletados == ()
    assert estado.caminho == ((0, 0),)


def test_mover_para_nova_posicao():
    estado = criar_estado_inicial((0, 0))
    novo_estado = estado.mover_para((0, 1))

    assert novo_estado.posicao == (0, 1)
    assert novo_estado.passos == 1
    assert novo_estado.caminho == ((0, 0), (0, 1))


def test_mover_nao_altera_estado_original():
    estado = criar_estado_inicial((0, 0))
    novo_estado = estado.mover_para((0, 1))

    assert estado.posicao == (0, 0)
    assert estado.passos == 0
    assert novo_estado.posicao == (0, 1)
    assert novo_estado.passos == 1


def test_adicionar_dinheiro():
    estado = criar_estado_inicial((0, 0))
    novo_estado = estado.adicionar_dinheiro(50)

    assert novo_estado.dinheiro == 50
    assert estado.dinheiro == 0


def test_adicionar_penalidade():
    estado = criar_estado_inicial((0, 0))
    novo_estado = estado.adicionar_penalidade(10)

    assert novo_estado.penalidades == 10
    assert estado.penalidades == 0


def test_coletar_minerio():
    estado = criar_estado_inicial((0, 0))
    novo_estado = estado.coletar_minerio(
        posicao_minerio=(0, 2),
        valor_minerio=10,
        quantidade_ferro=1,
    )

    assert novo_estado.dinheiro == 10
    assert novo_estado.ferro == 1
    assert novo_estado.minerios_coletados == ((0, 2),)


def test_nao_pode_coletar_mesmo_minerio_duas_vezes():
    estado = criar_estado_inicial((0, 0))

    estado = estado.coletar_minerio(
        posicao_minerio=(0, 2),
        valor_minerio=10,
        quantidade_ferro=1,
    )

    estado = estado.coletar_minerio(
        posicao_minerio=(0, 2),
        valor_minerio=10,
        quantidade_ferro=1,
    )

    assert estado.dinheiro == 10
    assert estado.ferro == 1
    assert estado.minerios_coletados == ((0, 2),)


def test_estado_agente_pode_ser_criado_diretamente():
    estado = EstadoAgente(posicao=(2, 3), passos=5, dinheiro=30)

    assert estado.posicao == (2, 3)
    assert estado.passos == 5
    assert estado.dinheiro == 30