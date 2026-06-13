from src.actions import get_valid_moves
from src.agent import executar_caminho
from src.comparison import comparar_algoritmos, formatar_resultado_comparacao
from src.dungeon import create_default_dungeon, find_agent_position, get_perceptions
from src.planner import escolher_melhor_minerio
from src.render import render_grid, render_perception_grid
from src.score import calcular_score, formatar_score
from src.search import formatar_caminho
from src.state import criar_estado_inicial


def main():
    print("uAI Dungeon Miner")
    print("Projeto iniciado com sucesso.")

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

    print(f"Estado inicial do agente: {estado_agente}")
    print(f"Posição inicial do agente: {posicao_agente}")
    print(f"Percepções na posição inicial: {percepcoes}")
    print(f"Ações válidas na posição inicial: {acoes_validas}")

    plano = escolher_melhor_minerio(
        dungeon,
        posicao_inicial=estado_agente.posicao,
        picareta_melhorada=estado_agente.picareta_melhorada,
        algoritmo="a_estrela",
    )

    if plano is None:
        print("\nNenhum minério acessível foi encontrado.")
        return

    print("\nPlanejador de rotas:")
    print(f"Melhor alvo escolhido: {plano.alvo}")
    print(f"Valor do minério: {plano.valor_alvo}")
    print(f"Utilidade estimada: {plano.utilidade_estimada}")
    print(f"Caminho planejado: {formatar_caminho(plano.resultado_busca.caminho)}")

    print("\nComparação dos algoritmos:")
    resultados = comparar_algoritmos(
        grid=dungeon,
        posicao_inicial=estado_agente.posicao,
        posicao_objetivo=plano.alvo,
        picareta_melhorada=estado_agente.picareta_melhorada,
    )

    for resultado in resultados:
        print()
        print(formatar_resultado_comparacao(resultado))
        print(f"Caminho: {formatar_caminho(resultado.caminho)}")

    estado_final = executar_caminho(
        grid=dungeon,
        estado_inicial=estado_agente,
        caminho=plano.resultado_busca.caminho,
    )

    resultado_score = calcular_score(estado_final)

    print("\nExecução da rota escolhida pelo planejador:")
    print(f"Estado final: {estado_final}")

    print("\nScore final da rota:")
    print(formatar_score(resultado_score))


if __name__ == "__main__":
    main()