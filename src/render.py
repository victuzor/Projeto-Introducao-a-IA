from src.dungeon import (
    Grid,
    SLIME,
    SKELETON,
    GOO_PERCEPTION,
    CRACK_PERCEPTION,
    get_perceptions,
)


def render_grid(grid: Grid) -> None:
    print("\nDungeon 8x8:")
    print("-" * 40)

    for row in grid:
        formatted_row = []

        for cell in row:
            formatted_row.append(f"{cell:>2}")

        print(" ".join(formatted_row))

    print("-" * 40)


def render_perception_grid(grid: Grid) -> None:
    print("\nMapa de percepções:")
    print("-" * 40)

    for row_index, row in enumerate(grid):
        formatted_row = []

        for col_index, cell in enumerate(row):
            position = (row_index, col_index)

            if cell == SLIME:
                symbol = "S"
            elif cell == SKELETON:
                symbol = "E"
            else:
                perceptions = get_perceptions(grid, position)

                has_goo = GOO_PERCEPTION in perceptions
                has_crack = CRACK_PERCEPTION in perceptions

                if has_goo and has_crack:
                    symbol = "GC"
                elif has_goo:
                    symbol = "G"
                elif has_crack:
                    symbol = "C"
                else:
                    symbol = "."

            formatted_row.append(f"{symbol:>2}")

        print(" ".join(formatted_row))

    print("-" * 40)
    print("Legenda: G = gosma próxima | C = crack próximo | GC = ambos")