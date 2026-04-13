"""Piece models and random generation."""

from __future__ import annotations

from dataclasses import dataclass
import random

from tetris.config import BOARD_WIDTH

SHAPES: dict[str, list[list[tuple[int, int]]]] = {
    "I": [
        [(-1, 0), (0, 0), (1, 0), (2, 0)],
        [(1, -1), (1, 0), (1, 1), (1, 2)],
    ],
    "O": [
        [(0, 0), (1, 0), (0, 1), (1, 1)],
    ],
    "T": [
        [(-1, 0), (0, 0), (1, 0), (0, 1)],
        [(0, -1), (0, 0), (1, 0), (0, 1)],
        [(-1, 0), (0, 0), (1, 0), (0, -1)],
        [(0, -1), (0, 0), (-1, 0), (0, 1)],
    ],
    "S": [
        [(0, 0), (1, 0), (-1, 1), (0, 1)],
        [(0, -1), (0, 0), (1, 0), (1, 1)],
    ],
    "Z": [
        [(-1, 0), (0, 0), (0, 1), (1, 1)],
        [(1, -1), (1, 0), (0, 0), (0, 1)],
    ],
    "J": [
        [(-1, 0), (0, 0), (1, 0), (-1, 1)],
        [(0, -1), (0, 0), (0, 1), (1, 1)],
        [(-1, 0), (0, 0), (1, 0), (1, -1)],
        [(0, -1), (0, 0), (0, 1), (-1, -1)],
    ],
    "L": [
        [(-1, 0), (0, 0), (1, 0), (1, 1)],
        [(0, -1), (0, 0), (0, 1), (1, -1)],
        [(-1, 0), (0, 0), (1, 0), (-1, -1)],
        [(0, -1), (0, 0), (0, 1), (-1, 1)],
    ],
}

PIECE_BAG = tuple(SHAPES.keys())


@dataclass
class Piece:
    kind: str
    x: int
    y: int
    rotation: int = 0

    def cells(self, x: int | None = None, y: int | None = None, rotation: int | None = None) -> list[tuple[int, int]]:
        px = self.x if x is None else x
        py = self.y if y is None else y
        pr = self.rotation if rotation is None else rotation
        shape_states = SHAPES[self.kind]
        offsets = shape_states[pr % len(shape_states)]
        return [(px + ox, py + oy) for ox, oy in offsets]

    def rotate(self, direction: int = 1) -> int:
        total_states = len(SHAPES[self.kind])
        self.rotation = (self.rotation + direction) % total_states
        return self.rotation


class PieceFactory:
    def __init__(self, seed: int | None = None) -> None:
        self._rng = random.Random(seed)
        self._bag: list[str] = []

    def _refill_bag(self) -> None:
        self._bag = list(PIECE_BAG)
        self._rng.shuffle(self._bag)

    def next_piece(self) -> Piece:
        if not self._bag:
            self._refill_bag()
        kind = self._bag.pop()
        return Piece(kind=kind, x=BOARD_WIDTH // 2, y=0)
