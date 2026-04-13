from tetris.board import Board
from tetris.game import GameState
from tetris.pieces import Piece


def test_piece_collision_with_wall() -> None:
    board = Board()
    piece = Piece(kind="I", x=0, y=0, rotation=0)
    assert not board.is_valid_position(piece, x=-1)


def test_lock_piece_marks_cells() -> None:
    board = Board()
    piece = Piece(kind="O", x=4, y=0)
    board.lock_piece(piece)
    assert board.grid[0][4] == "O"
    assert board.grid[1][5] == "O"


def test_clear_single_line() -> None:
    board = Board()
    board.grid[-1] = ["I"] * board.width
    cleared = board.clear_lines()
    assert cleared == 1
    assert all(cell is None for cell in board.grid[0])


def test_game_over_when_spawn_blocked() -> None:
    game = GameState(seed=7)
    game.next_piece = Piece(kind="O", x=game.board.width // 2, y=0)
    game.board.grid[0][game.next_piece.x] = "Z"
    game.board.grid[0][game.next_piece.x + 1] = "Z"
    game.hard_drop()
    assert game.game_over
