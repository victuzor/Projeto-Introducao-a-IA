from src.score import calcular_score, formatar_score
from src.state import EstadoAgente, criar_estado_inicial


def test_calcular_score_estado_inicial():
    estado = criar_estado_inicial((0, 0))

    resultado = calcular_score(estado)

    assert resultado.dinheiro == 0
    assert resultado.passos == 0
    assert resultado.custo_passos == 0
    assert resultado.penalidades == 0
    assert resultado.score_final == 0


def test_calcular_score_com_dinheiro_e_passos():
    estado = EstadoAgente(
        posicao=(0, 2),
        passos=2,
        dinheiro=10,
        penalidades=0,
    )

    resultado = calcular_score(estado)

    assert resultado.dinheiro == 10
    assert resultado.passos == 2
    assert resultado.custo_passos == 2
    assert resultado.penalidades == 0
    assert resultado.score_final == 8


def test_calcular_score_com_penalidade():
    estado = EstadoAgente(
        posicao=(0, 6),
        passos=5,
        dinheiro=50,
        penalidades=30,
    )

    resultado = calcular_score(estado)

    assert resultado.score_final == 15


def test_calcular_score_com_peso_de_passo_diferente():
    estado = EstadoAgente(
        posicao=(0, 4),
        passos=4,
        dinheiro=50,
        penalidades=0,
    )

    resultado = calcular_score(estado, peso_passo=2)

    assert resultado.custo_passos == 8
    assert resultado.score_final == 42


def test_formatar_score():
    estado = EstadoAgente(
        posicao=(0, 4),
        passos=4,
        dinheiro=50,
        penalidades=10,
    )

    resultado = calcular_score(estado)
    texto = formatar_score(resultado)

    assert "Dinheiro coletado: 50" in texto
    assert "Passos dados: 4" in texto
    assert "Penalidades: 10" in texto
    assert "Score final: 36" in texto