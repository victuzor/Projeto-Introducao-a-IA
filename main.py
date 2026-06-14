from src.actions import get_valid_moves
from src.agent import executar_caminho
from src.comparison import comparar_algoritmos
from src.dungeon import create_default_dungeon, find_agent_position, get_perceptions
from src.planner import escolher_melhor_minerio
from src.render import (
    render_comparacao_algoritmos,
    render_grid,
    render_painel,
    render_perception_grid,
    render_route_grid,
    render_score_final,
    render_titulo,
)
from src.score import calcular_score, formatar_score
from src.search import formatar_caminho
from src.state import criar_estado_inicial


def main():
    render_titulo()

    dungeon = create_default_dungeon()

    posicao_agente = find_agent_position(dungeon)
    estado_agente = criar_estado_inicial(posicao_agente)

    percepcoes = get_perceptions(dungeon, posicao_agente)
    acoes_validas = get_valid_moves(
        dungeon,
        posicao_agente,
        estado_agente.picareta_melhorada,
    )

    render_grid(dungeon)
    render_perception_grid(dungeon)

    render_painel(
        "Estado Inicial",
        [
            f"Estado do agente: {estado_agente}",
            f"Posição inicial: {posicao_agente}",
            f"Percepções iniciais: {percepcoes}",
            f"Ações válidas iniciais: {acoes_validas}",
        ],
    )

    plano = escolher_melhor_minerio(
        dungeon,
        posicao_inicial=estado_agente.posicao,
        picareta_melhorada=estado_agente.picareta_melhorada,
        algoritmo="a_estrela",
    )

    if plano is None:
        render_painel(
            "Planejador de Rotas",
            ["Nenhum minério acessível foi encontrado."],
        )
        return

    render_painel(
        "Planejador de Rotas",
        [
            "Algoritmo usado: A*",
            f"Melhor alvo escolhido: {plano.alvo}",
            f"Valor do minério: {plano.valor_alvo}",
            f"Utilidade estimada: {plano.utilidade_estimada}",
            f"Caminho planejado: {formatar_caminho(plano.resultado_busca.caminho)}",
        ],
    )

    render_route_grid(dungeon, plano.resultado_busca.caminho)

    resultados = comparar_algoritmos(
        grid=dungeon,
        posicao_inicial=estado_agente.posicao,
        posicao_objetivo=plano.alvo,
        picareta_melhorada=estado_agente.picareta_melhorada,
    )

    render_comparacao_algoritmos(resultados, formatar_caminho)

    estado_final = executar_caminho(
        grid=dungeon,
        estado_inicial=estado_agente,
        caminho=plano.resultado_busca.caminho,
    )

    resultado_score = calcular_score(estado_final)

    render_painel(
        "Execução da Rota Escolhida",
        [
            f"Estado final: {estado_final}",
            f"Caminho executado: {formatar_caminho(plano.resultado_busca.caminho)}",
        ],
    )

    render_score_final(formatar_score(resultado_score))


if __name__ == "__main__":
    main()