"""Rendering utilities for Contructor."""

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
        self._draw_side_panel(state, high_score=0)
        if state.paused and not state.game_over:
            self._draw_center_text("Paused")
        if state.game_over:
            self._draw_center_text("Game Over - Press R")
        pygame.display.flip()

    def draw_game(
        self,
        state: GameState,
        high_score: int,
        mode_name: str,
        mode_detail: str | None = None,
    ) -> None:
        self.screen.fill(COLORS["bg"])
        self._draw_board(state)
        self._draw_active_piece(state.current_piece)
        self._draw_ghost_piece(state)
        self._draw_side_panel(state, high_score=high_score, mode_name=mode_name, mode_detail=mode_detail)
        if state.paused and not state.game_over:
            self._draw_center_text("Paused")
        if state.game_over:
            self._draw_center_text("Game Over - Press R")
        pygame.display.flip()

    def draw_start_screen(self, profile: dict) -> None:
        self.screen.fill(COLORS["bg"])
        title = self.font.render("Contructor", True, COLORS["text"])
        prompt = self.small_font.render("Press Enter for Mode Select", True, COLORS["text"])
        settings = self.small_font.render("Press O for Settings", True, COLORS["text"])
        controls = self.small_font.render("Arrows/A,D,S | W/Up/X rotate | Space hard drop", True, COLORS["text"])
        pause_text = self.small_font.render("P pause  R restart  Esc quit", True, COLORS["text"])
        hs_text = self.font.render(f"Best Score: {profile['best_score']}", True, COLORS["text"])
        totals = self.small_font.render(
            f"Total Lines: {profile['total_lines']}  Games: {profile['games_played']}  Avg Lines/Game: {profile['avg_lines_per_game']}",
            True,
            COLORS["text"],
        )

        self.screen.blit(title, title.get_rect(center=(self.screen.get_width() // 2, 210)))
        self.screen.blit(hs_text, hs_text.get_rect(center=(self.screen.get_width() // 2, 280)))
        self.screen.blit(totals, totals.get_rect(center=(self.screen.get_width() // 2, 320)))
        self.screen.blit(prompt, prompt.get_rect(center=(self.screen.get_width() // 2, 360)))
        self.screen.blit(settings, settings.get_rect(center=(self.screen.get_width() // 2, 390)))
        self.screen.blit(controls, controls.get_rect(center=(self.screen.get_width() // 2, 420)))
        self.screen.blit(pause_text, pause_text.get_rect(center=(self.screen.get_width() // 2, 450)))
        pygame.display.flip()

    def draw_mode_select_screen(self, selected_index: int) -> None:
        self.screen.fill(COLORS["bg"])
        title = self.font.render("Select Mode", True, COLORS["text"])
        modes = [
            ("Classic", "Endless run"),
            ("Sprint", "Clear 40 lines as fast as possible"),
            ("Ultra", "Score as high as possible in 2 minutes"),
        ]
        self.screen.blit(title, title.get_rect(center=(self.screen.get_width() // 2, 130)))
        y = 240
        for idx, (name, description) in enumerate(modes):
            color = COLORS["I"] if idx == selected_index else COLORS["text"]
            mode_line = self.font.render(name, True, color)
            desc_line = self.small_font.render(description, True, color)
            self.screen.blit(mode_line, mode_line.get_rect(center=(self.screen.get_width() // 2, y)))
            self.screen.blit(desc_line, desc_line.get_rect(center=(self.screen.get_width() // 2, y + 28)))
            y += 120
        hint = self.small_font.render("Up/Down select, Enter start, Esc back", True, COLORS["text"])
        self.screen.blit(hint, hint.get_rect(center=(self.screen.get_width() // 2, 650)))
        pygame.display.flip()

    def draw_settings_screen(
        self,
        settings: dict,
        active_tab: str,
        selected_index: int,
        waiting_for_action: str | None,
    ) -> None:
        self.screen.fill(COLORS["bg"])
        title = self.font.render("Settings", True, COLORS["text"])
        self.screen.blit(title, title.get_rect(center=(self.screen.get_width() // 2, 90)))

        tabs = [("audio", "Audio"), ("controls", "Controls"), ("display", "Display")]
        tab_x = 90
        for tab_id, label in tabs:
            color = COLORS["I"] if tab_id == active_tab else COLORS["text"]
            tab_text = self.small_font.render(label, True, color)
            self.screen.blit(tab_text, (tab_x, 125))
            tab_x += 120

        keybinds = settings["keybinds"]
        if active_tab == "audio":
            rows = [
                f"Music Volume: {int(settings['music_volume'] * 100)}%",
                f"SFX Volume: {int(settings['sfx_volume'] * 100)}%",
                "Back",
            ]
        elif active_tab == "controls":
            rows = [
                f"Remap Move Left: {', '.join(keybinds['move_left']).upper()}",
                f"Remap Move Right: {', '.join(keybinds['move_right']).upper()}",
                f"Remap Soft Drop: {', '.join(keybinds['soft_drop']).upper()}",
                f"Remap Rotate CW: {', '.join(keybinds['rotate_cw']).upper()}",
                f"Remap Rotate CCW: {', '.join(keybinds['rotate_ccw']).upper()}",
                f"Remap Hard Drop: {', '.join(keybinds['hard_drop']).upper()}",
                "Back",
            ]
        else:
            rows = [
                f"Fullscreen: {'On' if settings['fullscreen'] else 'Off'}",
                "Back",
            ]

        y = 170
        for idx, row in enumerate(rows):
            color = COLORS["I"] if idx == selected_index else COLORS["text"]
            row_surface = self.small_font.render(row, True, color)
            self.screen.blit(row_surface, (80, y))
            y += 38

        help_line = self.small_font.render("Left/Right tabs, Up/Down select, A/D adjust, Enter edit", True, COLORS["text"])
        self.screen.blit(help_line, (80, 600))
        if waiting_for_action:
            wait = self.small_font.render(
                f"Press new key for {waiting_for_action.replace('_', ' ').title()}",
                True,
                COLORS["O"],
            )
            self.screen.blit(wait, (80, 640))
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

    def _draw_side_panel(
        self,
        state: GameState,
        high_score: int,
        mode_name: str,
        mode_detail: str | None = None,
    ) -> None:
        label_x = PREVIEW_OFFSET_X
        value_x = PREVIEW_OFFSET_X + 165
        row_y = 40
        row_gap = 30

        score_label = self.small_font.render("Score:", True, COLORS["text"])
        score_value = self.font.render(str(state.score), True, COLORS["text"])
        best_label = self.small_font.render("Best:", True, COLORS["text"])
        best_value = self.font.render(str(high_score), True, COLORS["text"])

        self.screen.blit(score_label, (label_x, row_y + 6))
        self.screen.blit(score_value, score_value.get_rect(topright=(value_x, row_y)))
        self.screen.blit(best_label, (label_x, row_y + row_gap + 6))
        self.screen.blit(best_value, best_value.get_rect(topright=(value_x, row_y + row_gap)))

        mode_text = self.small_font.render(f"Mode: {mode_name}", True, COLORS["text"])
        level_text = self.font.render(f"Level: {state.level}", True, COLORS["text"])
        lines_text = self.font.render(f"Lines: {state.lines}", True, COLORS["text"])
        controls_text = self.small_font.render("Arrows/A,D + W/Up + Space", True, COLORS["text"])
        pause_text = self.small_font.render("P: Pause  R: Restart  Esc: Quit", True, COLORS["text"])

        self.screen.blit(mode_text, (PREVIEW_OFFSET_X, 100))
        self.screen.blit(level_text, (PREVIEW_OFFSET_X, 130))
        self.screen.blit(lines_text, (PREVIEW_OFFSET_X, 160))
        if mode_detail:
            detail_text = self.small_font.render(mode_detail, True, COLORS["text"])
            self.screen.blit(detail_text, (PREVIEW_OFFSET_X, 190))

        next_preview_y = 280
        next_text = self.font.render("Next:", True, COLORS["text"])
        self.screen.blit(next_text, (PREVIEW_OFFSET_X, next_preview_y - 35))
        self._draw_preview_piece(state.next_piece, preview_y=next_preview_y)

        self.screen.blit(controls_text, (40, BOARD_OFFSET_Y + BOARD_HEIGHT * BLOCK_SIZE + 16))
        self.screen.blit(pause_text, (40, BOARD_OFFSET_Y + BOARD_HEIGHT * BLOCK_SIZE + 42))

    def _draw_preview_piece(self, piece: Piece, preview_y: int) -> None:
        shape = SHAPES[piece.kind][0]
        for ox, oy in shape:
            x = PREVIEW_OFFSET_X + (ox + 1) * BLOCK_SIZE
            y = preview_y + (oy + 1) * BLOCK_SIZE
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(self.screen, COLORS[piece.kind], rect.inflate(-2, -2))

    def _draw_center_text(self, text: str) -> None:
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.screen.blit(overlay, (0, 0))
        text_surface = self.font.render(text, True, COLORS["text"])
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text_surface, text_rect)
