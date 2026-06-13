from src.actions import get_valid_moves
from src.agent import aplicar_movimento
from src.dungeon import create_default_dungeon, find_agent_position, get_perceptions
from src.render import render_grid, render_perception_grid
from src.score import calcular_score, formatar_score
from src.search import busca_bfs, formatar_caminho, obter_proxima_posicao
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

    objetivo = (0, 2)
    resultado_bfs = busca_bfs(
        dungeon,
        posicao_inicial=posicao_agente,
        posicao_objetivo=objetivo,
        picareta_melhorada=estado_agente.picareta_melhorada,
    )

    print("\nBusca BFS:")
    print(f"Objetivo: {objetivo}")
    print(f"Encontrou caminho: {resultado_bfs.encontrou}")
    print(f"Caminho: {formatar_caminho(resultado_bfs.caminho)}")
    print(f"Custo em passos: {resultado_bfs.custo}")
    print(f"Nós expandidos: {resultado_bfs.nos_expandidos}")

    proxima_posicao = obter_proxima_posicao(resultado_bfs.caminho)

    if proxima_posicao is not None:
        novo_estado = aplicar_movimento(dungeon, estado_agente, proxima_posicao)

        print("\nDemonstração de execução do primeiro movimento do BFS:")
        print(f"Nova posição: {proxima_posicao}")
        print(f"Novo estado: {novo_estado}")

        resultado_score = calcular_score(novo_estado)

        print("\nScore após o movimento:")
        print(formatar_score(resultado_score))


if __name__ == "__main__":
    main()