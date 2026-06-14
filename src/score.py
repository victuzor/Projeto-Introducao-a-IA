from dataclasses import dataclass

from src.state import EstadoAgente


PESO_PASSO = 1


@dataclass(frozen=True)
class ResultadoScore:
    """
    Guarda os componentes do cálculo de score.
    """

    dinheiro: int
    passos: int
    custo_passos: int
    penalidades: int
    custo_risco: int
    score_final: int


def calcular_score(
    estado: EstadoAgente,
    peso_passo: int = PESO_PASSO,
) -> ResultadoScore:
    """
    Calcula o score final do agente.

    Fórmula:

    score = dinheiro - custo_passos - penalidades - custo_risco

    Onde:
    - dinheiro: valor dos minérios coletados;
    - custo_passos: quantidade de passos vezes o peso do passo;
    - penalidades: punições diretas por cair em monstros;
    - custo_risco: custo de andar com cautela em áreas com gosma/crack.
    """
    custo_passos = estado.passos * peso_passo

    score_final = (
        estado.dinheiro
        - custo_passos
        - estado.penalidades
        - estado.custo_risco
    )

    return ResultadoScore(
        dinheiro=estado.dinheiro,
        passos=estado.passos,
        custo_passos=custo_passos,
        penalidades=estado.penalidades,
        custo_risco=estado.custo_risco,
        score_final=score_final,
    )


def formatar_score(resultado: ResultadoScore) -> str:
    """
    Formata o score para exibição no terminal.
    """
    return (
        f"Dinheiro coletado: {resultado.dinheiro}\n"
        f"Passos dados: {resultado.passos}\n"
        f"Custo dos passos: {resultado.custo_passos}\n"
        f"Penalidades: {resultado.penalidades}\n"
        f"Custo por risco: {resultado.custo_risco}\n"
        f"Score final: {resultado.score_final}"
    )