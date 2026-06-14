from src.score import calcular_score, formatar_score
from src.state import EstadoAgente


def test_calcular_score_sem_penalidades():
    estado = EstadoAgente(
        posicao=(0, 0),
        passos=5,
        dinheiro=50,
        penalidades=0,
        custo_risco=0,
    )

    resultado = calcular_score(estado)

    assert resultado.dinheiro == 50
    assert resultado.passos == 5
    assert resultado.custo_passos == 5
    assert resultado.penalidades == 0
    assert resultado.custo_risco == 0
    assert resultado.score_final == 45


def test_calcular_score_com_penalidades():
    estado = EstadoAgente(
        posicao=(0, 0),
        passos=5,
        dinheiro=50,
        penalidades=30,
        custo_risco=0,
    )

    resultado = calcular_score(estado)

    assert resultado.score_final == 15


def test_calcular_score_com_custo_risco():
    estado = EstadoAgente(
        posicao=(0, 0),
        passos=5,
        dinheiro=50,
        penalidades=0,
        custo_risco=7,
    )

    resultado = calcular_score(estado)

    assert resultado.custo_risco == 7
    assert resultado.score_final == 38


def test_calcular_score_com_penalidade_e_custo_risco():
    estado = EstadoAgente(
        posicao=(0, 0),
        passos=5,
        dinheiro=50,
        penalidades=30,
        custo_risco=7,
    )

    resultado = calcular_score(estado)

    assert resultado.score_final == 8


def test_calcular_score_com_peso_passo_diferente():
    estado = EstadoAgente(
        posicao=(0, 0),
        passos=5,
        dinheiro=50,
        penalidades=0,
        custo_risco=0,
    )

    resultado = calcular_score(estado, peso_passo=2)

    assert resultado.custo_passos == 10
    assert resultado.score_final == 40


def test_formatar_score():
    estado = EstadoAgente(
        posicao=(0, 0),
        passos=5,
        dinheiro=50,
        penalidades=10,
        custo_risco=7,
    )

    resultado = calcular_score(estado)
    texto = formatar_score(resultado)

    assert "Dinheiro coletado: 50" in texto
    assert "Passos dados: 5" in texto
    assert "Custo dos passos: 5" in texto
    assert "Penalidades: 10" in texto
    assert "Custo por risco: 7" in texto
    assert "Score final: 28" in texto