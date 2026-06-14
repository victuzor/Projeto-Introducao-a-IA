from src.actions import get_valid_moves
from src.comparison import comparar_algoritmos
from src.dungeon import create_default_dungeon, find_agent_position, get_perceptions
from src.multisimulation import simular_algoritmos_visual
from src.planner import escolher_melhor_minerio
from src.render import (
    render_comparacao_algoritmos,
    render_grid,
    render_painel,
    render_perception_grid,
    render_titulo,
)
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
        estado_agente.ferro,
    )

    render_grid(dungeon)
    render_perception_grid(dungeon)

    render_painel(
        "Estado Inicial",
        [
            f"Posição inicial: {posicao_agente}",
            f"Percepções iniciais: {percepcoes}",
            f"Ações válidas iniciais: {acoes_validas}",
        ],
    )

    plano_inicial = escolher_melhor_minerio(
        dungeon,
        posicao_inicial=estado_agente.posicao,
        picareta_melhorada=estado_agente.picareta_melhorada,
        ferro_disponivel=estado_agente.ferro,
        algoritmo="a_estrela",
    )

    if plano_inicial is None:
        render_painel(
            "Planejador de Rotas",
            ["Nenhum minério acessível foi encontrado."],
        )
        return

    render_painel(
        "Primeiro Alvo Planejado",
        [
            "Algoritmo usado para exemplo inicial: A*",
            f"Alvo escolhido: {plano_inicial.alvo}",
            f"Valor do minério: {plano_inicial.valor_alvo}",
            f"Utilidade estimada: {plano_inicial.utilidade_estimada}",
            f"Caminho planejado: {formatar_caminho(plano_inicial.resultado_busca.caminho)}",
        ],
    )

    resultados = comparar_algoritmos(
        grid=dungeon,
        posicao_inicial=estado_agente.posicao,
        posicao_objetivo=plano_inicial.alvo,
        picareta_melhorada=estado_agente.picareta_melhorada,
    )

    render_comparacao_algoritmos(resultados, formatar_caminho)

    render_painel(
        "Simulação Comparativa",
        [
            "BFS, UCS e A* serão executados lado a lado.",
            "Cada algoritmo tentará coletar minérios enquanto houver utilidade positiva.",
            "Casas com gosma/crack agora geram custo de risco no score.",
        ],
    )

    resultados_simulacao = simular_algoritmos_visual(
        grid=dungeon,
        estado_inicial=estado_agente,
        utilidade_minima=1,
        delay=0.8,
    )

    for resultado_algoritmo in resultados_simulacao:
        resultado_missao = resultado_algoritmo.resultado_missao
        estado_final = resultado_missao.estado_final

        render_painel(
            f"Resumo da Missão - {resultado_algoritmo.algoritmo}",
            [
                f"Motivo da parada: {resultado_missao.motivo_parada}",
                f"Quantidade de rotas executadas: {len(resultado_missao.planos_executados)}",
                f"Minérios coletados: {estado_final.minerios_coletados}",
                f"Posição final: {estado_final.posicao}",
                f"Passos: {estado_final.passos}",
                f"Dinheiro: {estado_final.dinheiro}",
                f"Ferro: {estado_final.ferro}",
                f"Picareta melhorada: {estado_final.picareta_melhorada}",
                f"Penalidades: {estado_final.penalidades}",
                f"Custo por risco: {estado_final.custo_risco}",
                f"Score final: {resultado_missao.score.score_final}",
            ],
        )


if __name__ == "__main__":
    main()