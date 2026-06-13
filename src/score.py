from dataclasses import dataclass

from src.state import EstadoAgente


PESO_PASSO = 1


@dataclass(frozen=True)
class ResultadoScore:
    """
    Guarda o detalhamento do score final do agente.
    """

    dinheiro: int
    passos: int
    custo_passos: int
    penalidades: int
    score_final: int


def calcular_score(estado: EstadoAgente, peso_passo: int = PESO_PASSO) -> ResultadoScore:
    """
    Calcula o score final do agente.

    Fórmula:

    score = dinheiro coletado - custo dos passos - penalidades

    O peso_passo controla quanto cada passo reduz do score.
    """
    custo_passos = estado.passos * peso_passo
    score_final = estado.dinheiro - custo_passos - estado.penalidades

    return ResultadoScore(
        dinheiro=estado.dinheiro,
        passos=estado.passos,
        custo_passos=custo_passos,
        penalidades=estado.penalidades,
        score_final=score_final,
    )


def formatar_score(resultado: ResultadoScore) -> str:
    """
    Formata o resultado do score para exibição no terminal.
    """
    return (
        f"Dinheiro coletado: {resultado.dinheiro}\n"
        f"Passos dados: {resultado.passos}\n"
        f"Custo dos passos: {resultado.custo_passos}\n"
        f"Penalidades: {resultado.penalidades}\n"
        f"Score final: {resultado.score_final}"
    )