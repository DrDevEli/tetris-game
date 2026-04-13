"""Board operations and collision checks."""

from __future__ import annotations

from tetris.config import BOARD_HEIGHT, BOARD_WIDTH
from tetris.pieces import Piece


class Board:
    def __init__(self) -> None:
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT
        self.grid: list[list[str | None]] = [
            [None for _ in range(self.width)] for _ in range(self.height)
        ]

    def inside(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and y < self.height

    def is_cell_empty(self, x: int, y: int) -> bool:
        if y < 0:
            return True
        return self.grid[y][x] is None

    def is_valid_position(self, piece: Piece, x: int | None = None, y: int | None = None, rotation: int | None = None) -> bool:
        for cx, cy in piece.cells(x=x, y=y, rotation=rotation):
            if not self.inside(cx, cy):
                return False
            if cy >= 0 and not self.is_cell_empty(cx, cy):
                return False
        return True

    def lock_piece(self, piece: Piece) -> None:
        for x, y in piece.cells():
            if y >= 0:
                self.grid[y][x] = piece.kind

    def clear_lines(self) -> int:
        remaining_rows: list[list[str | None]] = []
        cleared = 0
        for row in self.grid:
            if all(cell is not None for cell in row):
                cleared += 1
            else:
                remaining_rows.append(row)
        for _ in range(cleared):
            remaining_rows.insert(0, [None for _ in range(self.width)])
        self.grid = remaining_rows
        return cleared
