"""Entrypoint for the Tetris game."""

from __future__ import annotations

import pygame

from tetris.config import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from tetris.game import GameState
from tetris.persistence import HighScoreStore
from tetris.render import Renderer
from tetris.sound import SoundManager


def run() -> None:
    pygame.init()
    pygame.display.set_caption("Tetris")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    state = GameState()
    renderer = Renderer(screen)
    sounds = SoundManager()
    high_score_store = HighScoreStore()
    high_score = high_score_store.load()
    started = False
    game_over_recorded = False
    fall_timer_ms = 0

    running = True
    while running:
        dt = clock.tick(FPS)
        if started:
            fall_timer_ms += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif not started and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    state.reset()
                    started = True
                    game_over_recorded = False
                elif not started:
                    continue
                elif event.key == pygame.K_p:
                    state.toggle_pause()
                elif event.key == pygame.K_r:
                    state.reset()
                    fall_timer_ms = 0
                    started = True
                    game_over_recorded = False
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    if state.move(-1, 0):
                        sounds.play("move")
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    if state.move(1, 0):
                        sounds.play("move")
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if state.move(0, 1):
                        sounds.play("move")
                elif event.key in (pygame.K_UP, pygame.K_w, pygame.K_x):
                    if state.rotate(1):
                        sounds.play("rotate")
                elif event.key == pygame.K_z:
                    if state.rotate(-1):
                        sounds.play("rotate")
                elif event.key == pygame.K_SPACE:
                    result = state.hard_drop()
                    fall_timer_ms = 0
                    if result.locked:
                        sounds.play("hard_drop")
                    if result.cleared_lines:
                        sounds.play("line")
                    elif result.locked:
                        sounds.play("lock")
                    if result.game_over:
                        sounds.play("game_over")

        if not started:
            renderer.draw_start_screen(high_score)
            continue

        if fall_timer_ms >= state.fall_delay_ms:
            result = state.tick()
            fall_timer_ms = 0
            if result.cleared_lines:
                sounds.play("line")
            elif result.locked:
                sounds.play("lock")
            if result.game_over:
                sounds.play("game_over")

        if state.game_over and not game_over_recorded:
            if state.score > high_score:
                high_score = state.score
                high_score_store.save(high_score)
            game_over_recorded = True

        renderer.draw_game(state, high_score=high_score)

    pygame.quit()


if __name__ == "__main__":
    run()
