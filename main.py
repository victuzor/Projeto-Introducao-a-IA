from src.dungeon import create_default_dungeon, find_agent_position, get_perceptions
from src.render import render_grid, render_perception_grid


def main():
    print("uAI Dungeon Miner")
    print("Projeto iniciado com sucesso.")

    dungeon = create_default_dungeon()
    agent_position = find_agent_position(dungeon)
    perceptions = get_perceptions(dungeon, agent_position)

    render_grid(dungeon)
    render_perception_grid(dungeon)

    print(f"Posição inicial do agente: {agent_position}")
    print(f"Percepções na posição inicial: {perceptions}")


if __name__ == "__main__":
    main()