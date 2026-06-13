from dataclasses import dataclass

from src.state import EstadoAgente


PESO_PASSO = 1


@dataclass(frozen=True)
class ResultadoScore:

    dinheiro: int
    passos: int
    custo_passos: int
    penalidades: int
    score_final: int


def calcular_score(estado: EstadoAgente, peso_passo: int = PESO_PASSO) -> ResultadoScore:
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
    return (
        f"Dinheiro coletado: {resultado.dinheiro}\n"
        f"Passos dados: {resultado.passos}\n"
        f"Custo dos passos: {resultado.custo_passos}\n"
        f"Penalidades: {resultado.penalidades}\n"
        f"Score final: {resultado.score_final}"
    )