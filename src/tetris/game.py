"""Core Tetris game state and rules."""

from __future__ import annotations

from dataclasses import dataclass

from tetris.board import Board
from tetris.config import (
    BASE_FALL_DELAY_MS,
    FALL_SPEED_STEP_MS,
    HARD_DROP_POINTS,
    LINES_PER_LEVEL,
    LINE_CLEAR_POINTS,
    MIN_FALL_DELAY_MS,
    SOFT_DROP_POINTS,
)
from tetris.pieces import Piece, PieceFactory

SPRINT_LINES_TARGET = 40
ULTRA_DURATION_MS = 120_000


@dataclass
class TickResult:
    locked: bool = False
    cleared_lines: int = 0
    game_over: bool = False


class GameState:
    def __init__(self, seed: int | None = None) -> None:
        self.factory = PieceFactory(seed=seed)
        self.mode = "classic"
        self.reset(mode=self.mode)

    def reset(self, mode: str = "classic") -> None:
        self.mode = mode
        self.board = Board()
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.paused = False

        self.current_piece = self.factory.next_piece()
        self.next_piece = self.factory.next_piece()
        if not self.board.is_valid_position(self.current_piece):
            self.game_over = True

    def mode_detail(self, elapsed_ms: int) -> str | None:
        if self.mode == "sprint":
            remaining = max(0, SPRINT_LINES_TARGET - self.lines)
            return f"Lines Left: {remaining}"
        if self.mode == "ultra":
            time_left = max(0, ULTRA_DURATION_MS - elapsed_ms)
            return f"Time Left: {time_left // 1000}s"
        return None

    def apply_mode_rules(self, elapsed_ms: int) -> bool:
        if self.game_over:
            return False
        if self.mode == "sprint" and self.lines >= SPRINT_LINES_TARGET:
            self.game_over = True
            return True
        if self.mode == "ultra" and elapsed_ms >= ULTRA_DURATION_MS:
            self.game_over = True
            return True
        return False

    @property
    def fall_delay_ms(self) -> int:
        delay = BASE_FALL_DELAY_MS - (self.level - 1) * FALL_SPEED_STEP_MS
        return max(MIN_FALL_DELAY_MS, delay)

    def toggle_pause(self) -> None:
        if not self.game_over:
            self.paused = not self.paused

    def move(self, dx: int, dy: int) -> bool:
        if self.game_over or self.paused:
            return False
        new_x = self.current_piece.x + dx
        new_y = self.current_piece.y + dy
        if self.board.is_valid_position(self.current_piece, x=new_x, y=new_y):
            self.current_piece.x = new_x
            self.current_piece.y = new_y
            if dy > 0:
                self.score += SOFT_DROP_POINTS
            return True
        return False

    def hard_drop(self) -> TickResult:
        if self.game_over or self.paused:
            return TickResult()
        dropped = 0
        while self.board.is_valid_position(
            self.current_piece, y=self.current_piece.y + 1
        ):
            self.current_piece.y += 1
            dropped += 1
        self.score += dropped * HARD_DROP_POINTS
        cleared, game_over = self._lock_and_spawn()
        return TickResult(locked=True, cleared_lines=cleared, game_over=game_over)

    def rotate(self, direction: int = 1) -> bool:
        if self.game_over or self.paused:
            return False
        test_rotation = (self.current_piece.rotation + direction) % len(
            self._shape_states()
        )
        # Basic wall kicks for common near-wall and stack collisions.
        kicks = [(0, 0), (-1, 0), (1, 0), (-2, 0), (2, 0), (0, -1)]
        for dx, dy in kicks:
            new_x = self.current_piece.x + dx
            new_y = self.current_piece.y + dy
            if self.board.is_valid_position(
                self.current_piece, x=new_x, y=new_y, rotation=test_rotation
            ):
                self.current_piece.x = new_x
                self.current_piece.y = new_y
                self.current_piece.rotation = test_rotation
                return True
        return False

    def tick(self) -> TickResult:
        if self.game_over or self.paused:
            return TickResult()
        if self.board.is_valid_position(self.current_piece, y=self.current_piece.y + 1):
            self.current_piece.y += 1
            return TickResult()
        cleared, game_over = self._lock_and_spawn()
        return TickResult(locked=True, cleared_lines=cleared, game_over=game_over)

    def ghost_drop_distance(self) -> int:
        distance = 0
        while self.board.is_valid_position(
            self.current_piece, y=self.current_piece.y + distance + 1
        ):
            distance += 1
        return distance

    def _lock_and_spawn(self) -> tuple[int, bool]:
        self.board.lock_piece(self.current_piece)
        cleared = self.board.clear_lines()
        game_over = False
        if cleared:
            self.lines += cleared
            self.score += LINE_CLEAR_POINTS.get(cleared, 0) * self.level
            self.level = self.lines // LINES_PER_LEVEL + 1

        self.current_piece = self.next_piece
        self.next_piece = self.factory.next_piece()
        if not self.board.is_valid_position(self.current_piece):
            self.game_over = True
            game_over = True
        return cleared, game_over

    def _shape_states(self) -> list[list[tuple[int, int]]]:
        from tetris.pieces import SHAPES

        return SHAPES[self.current_piece.kind]
