from src.actions import get_valid_moves
from src.agent import aplicar_movimento
from src.dungeon import create_default_dungeon, find_agent_position, get_perceptions
from src.planner import escolher_melhor_minerio
from src.render import render_grid, render_perception_grid
from src.score import calcular_score, formatar_score
from src.search import (
    busca_a_estrela,
    busca_bfs,
    busca_ucs,
    formatar_caminho,
    obter_proxima_posicao,
)
from src.state import criar_estado_inicial


def exibir_resultado_busca(nome_algoritmo, resultado):
    print(f"\nBusca {nome_algoritmo}:")
    print(f"Encontrou caminho: {resultado.encontrou}")
    print(f"Caminho: {formatar_caminho(resultado.caminho)}")
    print(f"Custo acumulado: {resultado.custo}")
    print(f"Nós expandidos: {resultado.nos_expandidos}")


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

    objetivo = plano.alvo

    print("\nPlanejador de rotas:")
    print(f"Melhor alvo escolhido: {plano.alvo}")
    print(f"Valor do minério: {plano.valor_alvo}")
    print(f"Utilidade estimada: {plano.utilidade_estimada}")
    print(f"Caminho planejado: {formatar_caminho(plano.resultado_busca.caminho)}")

    resultado_bfs = busca_bfs(
        dungeon,
        posicao_inicial=posicao_agente,
        posicao_objetivo=objetivo,
        picareta_melhorada=estado_agente.picareta_melhorada,
    )

    resultado_ucs = busca_ucs(
        dungeon,
        posicao_inicial=posicao_agente,
        posicao_objetivo=objetivo,
        picareta_melhorada=estado_agente.picareta_melhorada,
    )

    resultado_a_estrela = busca_a_estrela(
        dungeon,
        posicao_inicial=posicao_agente,
        posicao_objetivo=objetivo,
        picareta_melhorada=estado_agente.picareta_melhorada,
    )

    print(f"\nObjetivo usado na comparação: {objetivo}")

    exibir_resultado_busca("BFS", resultado_bfs)
    exibir_resultado_busca("UCS", resultado_ucs)
    exibir_resultado_busca("A*", resultado_a_estrela)

    proxima_posicao = obter_proxima_posicao(resultado_a_estrela.caminho)

    if proxima_posicao is not None:
        novo_estado = aplicar_movimento(dungeon, estado_agente, proxima_posicao)

        print("\nDemonstração de execução do primeiro movimento do A*:")
        print(f"Nova posição: {proxima_posicao}")
        print(f"Novo estado: {novo_estado}")

        resultado_score = calcular_score(novo_estado)

        print("\nScore após o movimento:")
        print(formatar_score(resultado_score))


if __name__ == "__main__":
    main()