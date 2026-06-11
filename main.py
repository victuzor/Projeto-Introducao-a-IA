from src.actions import get_valid_moves
from src.dungeon import create_default_dungeon, find_agent_position, get_perceptions
from src.render import render_grid, render_perception_grid
from src.state import criar_estado_inicial


def main():
    print("uAI Dungeon Miner")
    print("Projeto iniciado com sucesso.")

    dungeon = create_default_dungeon()
    agent_position = find_agent_position(dungeon)
    agent_state = criar_estado_inicial(agent_position)

    perceptions = get_perceptions(dungeon, agent_position)
    valid_moves = get_valid_moves(dungeon, agent_position)

    render_grid(dungeon)
    render_perception_grid(dungeon)

    print(f"Estado inicial do agente: {agent_state}")
    print(f"Posição inicial do agente: {agent_position}")
    print(f"Percepções na posição inicial: {perceptions}")
    print(f"Ações válidas na posição inicial: {valid_moves}")


if __name__ == "__main__":
    main()