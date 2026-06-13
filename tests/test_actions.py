from src.actions import get_action_name, get_valid_moves
from src.dungeon import create_default_dungeon


def test_action_name_move_down():
    action = get_action_name((0, 0), (1, 0))

    assert action == "mover_baixo"


def test_action_name_move_right():
    action = get_action_name((0, 0), (0, 1))

    assert action == "mover_direita"


def test_action_name_move_up():
    action = get_action_name((1, 0), (0, 0))

    assert action == "mover_cima"


def test_action_name_move_left():
    action = get_action_name((0, 1), (0, 0))

    assert action == "mover_esquerda"


def test_valid_moves_from_initial_position():
    dungeon = create_default_dungeon()

    valid_moves = get_valid_moves(dungeon, (0, 0))

    assert ("mover_baixo", (1, 0)) in valid_moves
    assert ("mover_direita", (0, 1)) in valid_moves
    assert len(valid_moves) == 2


def test_blocked_cell_is_not_valid_move():
    dungeon = create_default_dungeon()

    valid_moves = get_valid_moves(dungeon, (1, 0))

    assert ("mover_direita", (1, 1)) not in valid_moves

def test_parede_fragil_nao_e_movimento_valido_sem_picareta():
    dungeon = create_default_dungeon()

    valid_moves = get_valid_moves(dungeon, (0, 2), picareta_melhorada=False)

    assert ("mover_direita", (0, 3)) not in valid_moves


def test_parede_fragil_e_movimento_valido_com_picareta():
    dungeon = create_default_dungeon()

    valid_moves = get_valid_moves(dungeon, (0, 2), picareta_melhorada=True)

    assert ("mover_direita", (0, 3)) in valid_moves