from src.actions import get_valid_moves
from src.agent import aplicar_movimento
from src.dungeon import create_default_dungeon, find_agent_position, get_perceptions
from src.render import render_grid, render_perception_grid
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

    if acoes_validas:
        nome_acao, nova_posicao = acoes_validas[0]
        novo_estado = aplicar_movimento(dungeon, estado_agente, nova_posicao)

        print("\nDemonstração de movimento:")
        print(f"Ação escolhida: {nome_acao}")
        print(f"Nova posição: {nova_posicao}")
        print(f"Novo estado: {novo_estado}")


if __name__ == "__main__":
    main()