"""Rendering utilities for Tetris."""

from __future__ import annotations

import pygame

from tetris.config import (
    BLOCK_SIZE,
    BOARD_HEIGHT,
    BOARD_OFFSET_X,
    BOARD_OFFSET_Y,
    BOARD_WIDTH,
    COLORS,
    PREVIEW_OFFSET_X,
    PREVIEW_OFFSET_Y,
)
from tetris.game import GameState
from tetris.pieces import Piece, SHAPES


class Renderer:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)

    def draw(self, state: GameState) -> None:
        self.screen.fill(COLORS["bg"])
        self._draw_board(state)
        self._draw_active_piece(state.current_piece)
        self._draw_ghost_piece(state)
        self._draw_side_panel(state)
        if state.paused and not state.game_over:
            self._draw_center_text("Paused")
        if state.game_over:
            self._draw_center_text("Game Over - Press R")
        pygame.display.flip()

    def _draw_board(self, state: GameState) -> None:
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                rect = pygame.Rect(
                    BOARD_OFFSET_X + x * BLOCK_SIZE,
                    BOARD_OFFSET_Y + y * BLOCK_SIZE,
                    BLOCK_SIZE,
                    BLOCK_SIZE,
                )
                pygame.draw.rect(self.screen, COLORS["grid"], rect, width=1)
                kind = state.board.grid[y][x]
                if kind:
                    pygame.draw.rect(self.screen, COLORS[kind], rect.inflate(-2, -2))

    def _draw_active_piece(self, piece: Piece) -> None:
        for x, y in piece.cells():
            if y < 0:
                continue
            rect = pygame.Rect(
                BOARD_OFFSET_X + x * BLOCK_SIZE,
                BOARD_OFFSET_Y + y * BLOCK_SIZE,
                BLOCK_SIZE,
                BLOCK_SIZE,
            )
            pygame.draw.rect(self.screen, COLORS[piece.kind], rect.inflate(-2, -2))

    def _draw_ghost_piece(self, state: GameState) -> None:
        drop = state.ghost_drop_distance()
        if drop <= 0:
            return
        for x, y in state.current_piece.cells(y=state.current_piece.y + drop):
            if y < 0:
                continue
            rect = pygame.Rect(
                BOARD_OFFSET_X + x * BLOCK_SIZE,
                BOARD_OFFSET_Y + y * BLOCK_SIZE,
                BLOCK_SIZE,
                BLOCK_SIZE,
            )
            pygame.draw.rect(self.screen, COLORS["grid"], rect.inflate(-6, -6), width=2)

    def _draw_side_panel(self, state: GameState) -> None:
        score_text = self.font.render(f"Score: {state.score}", True, COLORS["text"])
        level_text = self.font.render(f"Level: {state.level}", True, COLORS["text"])
        lines_text = self.font.render(f"Lines: {state.lines}", True, COLORS["text"])
        controls_text = self.small_font.render("Arrows/A,D + W/Up + Space", True, COLORS["text"])
        pause_text = self.small_font.render("P: Pause  R: Restart  Esc: Quit", True, COLORS["text"])

        self.screen.blit(score_text, (PREVIEW_OFFSET_X, 40))
        self.screen.blit(level_text, (PREVIEW_OFFSET_X, 70))
        self.screen.blit(lines_text, (PREVIEW_OFFSET_X, 100))

        next_text = self.font.render("Next:", True, COLORS["text"])
        self.screen.blit(next_text, (PREVIEW_OFFSET_X, PREVIEW_OFFSET_Y - 35))
        self._draw_preview_piece(state.next_piece)

        self.screen.blit(controls_text, (40, BOARD_OFFSET_Y + BOARD_HEIGHT * BLOCK_SIZE + 16))
        self.screen.blit(pause_text, (40, BOARD_OFFSET_Y + BOARD_HEIGHT * BLOCK_SIZE + 42))

    def _draw_preview_piece(self, piece: Piece) -> None:
        shape = SHAPES[piece.kind][0]
        for ox, oy in shape:
            x = PREVIEW_OFFSET_X + (ox + 1) * BLOCK_SIZE
            y = PREVIEW_OFFSET_Y + (oy + 1) * BLOCK_SIZE
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(self.screen, COLORS[piece.kind], rect.inflate(-2, -2))

    def _draw_center_text(self, text: str) -> None:
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.screen.blit(overlay, (0, 0))
        text_surface = self.font.render(text, True, COLORS["text"])
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text_surface, text_rect)
