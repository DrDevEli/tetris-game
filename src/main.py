"""Entrypoint for the Tetris game."""

from __future__ import annotations

import pygame

from tetris.config import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from tetris.game import GameState
from tetris.render import Renderer


def run() -> None:
    pygame.init()
    pygame.display.set_caption("Tetris")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    state = GameState()
    renderer = Renderer(screen)
    fall_timer_ms = 0

    running = True
    while running:
        dt = clock.tick(FPS)
        fall_timer_ms += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p:
                    state.toggle_pause()
                elif event.key == pygame.K_r:
                    state.reset()
                    fall_timer_ms = 0
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    state.move(-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    state.move(1, 0)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    state.move(0, 1)
                elif event.key in (pygame.K_UP, pygame.K_w, pygame.K_x):
                    state.rotate(1)
                elif event.key == pygame.K_z:
                    state.rotate(-1)
                elif event.key == pygame.K_SPACE:
                    state.hard_drop()
                    fall_timer_ms = 0

        if fall_timer_ms >= state.fall_delay_ms:
            state.tick()
            fall_timer_ms = 0

        renderer.draw(state)

    pygame.quit()


if __name__ == "__main__":
    run()
