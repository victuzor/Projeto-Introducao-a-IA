from src.dungeon import (
    GRID_SIZE,
    AGENT,
    IRON,
    GOLD,
    SLIME,
    SKELETON,
    GOO_PERCEPTION,
    CRACK_PERCEPTION,
    create_default_dungeon,
    find_agent_position,
    is_inside_grid,
    is_ore,
    get_ore_value,
    get_neighbors,
    get_perceptions,
)


def test_dungeon_has_8_rows():
    dungeon = create_default_dungeon()

    assert len(dungeon) == GRID_SIZE


def test_dungeon_has_8_columns_in_each_row():
    dungeon = create_default_dungeon()

    for row in dungeon:
        assert len(row) == GRID_SIZE


def test_agent_starts_at_position_zero_zero():
    dungeon = create_default_dungeon()
    position = find_agent_position(dungeon)

    assert position == (0, 0)


def test_position_inside_grid():
    assert is_inside_grid((0, 0)) is True
    assert is_inside_grid((7, 7)) is True


def test_position_outside_grid():
    assert is_inside_grid((-1, 0)) is False
    assert is_inside_grid((8, 0)) is False
    assert is_inside_grid((0, 8)) is False


def test_ore_identification():
    assert is_ore(IRON) is True
    assert is_ore(GOLD) is True
    assert is_ore(AGENT) is False


def test_ore_value():
    assert get_ore_value(IRON) == 10
    assert get_ore_value(GOLD) == 50
    assert get_ore_value(AGENT) == 0
    

def test_get_neighbors_from_corner():
    neighbors = get_neighbors((0, 0))

    assert neighbors == [(1, 0), (0, 1)]


def test_get_neighbors_from_center():
    neighbors = get_neighbors((3, 3))

    assert (2, 3) in neighbors
    assert (4, 3) in neighbors
    assert (3, 2) in neighbors
    assert (3, 4) in neighbors
    assert len(neighbors) == 4


def test_perception_near_slime():
    dungeon = create_default_dungeon()

    # No mapa padrão, existe um slime em (0, 6).
    # Portanto, a posição (0, 5) deve perceber gosma.
    perceptions = get_perceptions(dungeon, (0, 5))

    assert GOO_PERCEPTION in perceptions


def test_perception_near_skeleton():
    dungeon = create_default_dungeon()

    # No mapa padrão, existe um esqueleto em (3, 5).
    # Portanto, a posição (3, 4) deve perceber crack.
    perceptions = get_perceptions(dungeon, (3, 4))

    assert CRACK_PERCEPTION in perceptions


def test_perception_without_monster_nearby():
    dungeon = create_default_dungeon()

    perceptions = get_perceptions(dungeon, (0, 0))

    assert perceptions == []