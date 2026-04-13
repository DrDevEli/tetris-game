"""Entrypoint for the Contructor game."""

from __future__ import annotations

import pygame

from tetris.config import DEFAULT_SETTINGS, FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from tetris.game import GameState
from tetris.persistence import HighScoreStore
from tetris.render import Renderer
from tetris.sound import SoundManager


SETTINGS_TABS = ["audio", "controls", "display"]
TAB_ITEMS = {
    "audio": ["music_volume", "sfx_volume", "back"],
    "controls": [
        "move_left",
        "move_right",
        "soft_drop",
        "rotate_cw",
        "rotate_ccw",
        "hard_drop",
        "back",
    ],
    "display": ["fullscreen", "back"],
}
GAME_MODES = ["classic", "sprint", "ultra"]
MODE_LABELS = {"classic": "Classic", "sprint": "Sprint", "ultra": "Ultra"}


def key_to_name(key: int) -> str:
    return pygame.key.name(key).lower()


def matches_action(settings: dict, action: str, key: int) -> bool:
    return key_to_name(key) in settings["keybinds"][action]


def apply_display_mode(fullscreen: bool) -> pygame.Surface:
    flags = pygame.FULLSCREEN if fullscreen else 0
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)


def run() -> None:
    pygame.init()
    pygame.display.set_caption("Contructor")
    screen = apply_display_mode(False)
    clock = pygame.time.Clock()

    state = GameState()
    renderer = Renderer(screen)
    sounds = SoundManager()
    high_score_store = HighScoreStore()
    profile = high_score_store.load_profile()
    high_score = profile["best_score"]
    settings = high_score_store.load_settings()
    settings.setdefault("keybinds", DEFAULT_SETTINGS["keybinds"].copy())
    if settings.get("fullscreen", False):
        screen = apply_display_mode(True)
        renderer = Renderer(screen)
    sounds.set_music_volume(settings["music_volume"])
    sounds.set_sfx_volume(settings["sfx_volume"])

    started = False
    in_mode_select = False
    in_settings = False
    game_over_recorded = False
    fall_timer_ms = 0
    mode_elapsed_ms = 0
    mode_select_index = 0
    current_mode = "classic"
    settings_tab_index = 0
    settings_item_index = 0
    waiting_for_rebind: str | None = None

    running = True
    while running:
        dt = clock.tick(FPS)
        if started and not in_settings:
            fall_timer_ms += dt
            if not state.paused and not state.game_over:
                mode_elapsed_ms += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if in_settings:
                        in_settings = False
                        waiting_for_rebind = None
                        high_score_store.save_settings(settings)
                    elif in_mode_select:
                        in_mode_select = False
                    else:
                        running = False
                elif waiting_for_rebind:
                    settings["keybinds"][waiting_for_rebind] = [key_to_name(event.key)]
                    waiting_for_rebind = None
                    high_score_store.save_settings(settings)
                elif in_settings:
                    active_tab = SETTINGS_TABS[settings_tab_index]
                    items = TAB_ITEMS[active_tab]
                    if event.key == pygame.K_UP:
                        settings_item_index = (settings_item_index - 1) % len(items)
                    elif event.key == pygame.K_DOWN:
                        settings_item_index = (settings_item_index + 1) % len(items)
                    elif event.key == pygame.K_TAB:
                        settings_tab_index = (settings_tab_index + 1) % len(SETTINGS_TABS)
                        settings_item_index = 0
                    elif event.key == pygame.K_LEFT:
                        settings_tab_index = (settings_tab_index - 1) % len(SETTINGS_TABS)
                        settings_item_index = 0
                    elif event.key == pygame.K_RIGHT:
                        settings_tab_index = (settings_tab_index + 1) % len(SETTINGS_TABS)
                        settings_item_index = 0
                    elif event.key in (pygame.K_a, pygame.K_d):
                        item = items[settings_item_index]
                        if item == "music_volume":
                            delta = 0.05 if event.key == pygame.K_d else -0.05
                            settings["music_volume"] = max(0.0, min(1.0, settings["music_volume"] + delta))
                            sounds.set_music_volume(settings["music_volume"])
                        elif item == "sfx_volume":
                            delta = 0.05 if event.key == pygame.K_d else -0.05
                            settings["sfx_volume"] = max(0.0, min(1.0, settings["sfx_volume"] + delta))
                            sounds.set_sfx_volume(settings["sfx_volume"])
                        if item in ("music_volume", "sfx_volume"):
                            high_score_store.save_settings(settings)
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        item = items[settings_item_index]
                        if item in settings["keybinds"]:
                            waiting_for_rebind = item
                        elif item == "fullscreen":
                            settings["fullscreen"] = not settings["fullscreen"]
                            screen = apply_display_mode(settings["fullscreen"])
                            renderer = Renderer(screen)
                            high_score_store.save_settings(settings)
                        elif item == "back":
                            in_settings = False
                            high_score_store.save_settings(settings)
                elif in_mode_select:
                    if event.key == pygame.K_UP:
                        mode_select_index = (mode_select_index - 1) % len(GAME_MODES)
                    elif event.key == pygame.K_DOWN:
                        mode_select_index = (mode_select_index + 1) % len(GAME_MODES)
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        current_mode = GAME_MODES[mode_select_index]
                        state.reset(mode=current_mode)
                        started = True
                        in_mode_select = False
                        game_over_recorded = False
                        mode_elapsed_ms = 0
                elif not started and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    in_mode_select = True
                elif not started and matches_action(settings, "settings", event.key):
                    in_settings = True
                elif not started:
                    continue
                elif matches_action(settings, "settings", event.key):
                    in_settings = True
                elif matches_action(settings, "pause", event.key):
                    state.toggle_pause()
                elif matches_action(settings, "restart", event.key):
                    state.reset(mode=current_mode)
                    fall_timer_ms = 0
                    started = True
                    game_over_recorded = False
                    mode_elapsed_ms = 0
                elif matches_action(settings, "move_left", event.key):
                    if state.move(-1, 0):
                        sounds.play("move")
                elif matches_action(settings, "move_right", event.key):
                    if state.move(1, 0):
                        sounds.play("move")
                elif matches_action(settings, "soft_drop", event.key):
                    if state.move(0, 1):
                        sounds.play("move")
                elif matches_action(settings, "rotate_cw", event.key):
                    if state.rotate(1):
                        sounds.play("rotate")
                elif matches_action(settings, "rotate_ccw", event.key):
                    if state.rotate(-1):
                        sounds.play("rotate")
                elif matches_action(settings, "hard_drop", event.key):
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

        if in_settings:
            renderer.draw_settings_screen(
                settings=settings,
                active_tab=SETTINGS_TABS[settings_tab_index],
                selected_index=settings_item_index,
                waiting_for_action=waiting_for_rebind,
            )
            continue

        if in_mode_select:
            renderer.draw_mode_select_screen(mode_select_index)
            continue

        if not started:
            renderer.draw_start_screen(profile)
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

        mode_detail = state.mode_detail(mode_elapsed_ms)
        if state.apply_mode_rules(mode_elapsed_ms):
            sounds.play("game_over")

        if state.game_over and not game_over_recorded:
            if state.score > high_score:
                high_score = state.score
                high_score_store.save(high_score)
            profile["best_score"] = max(profile["best_score"], state.score)
            profile["games_played"] += 1
            profile["total_lines"] += state.lines
            profile["avg_lines_per_game"] = round(
                profile["total_lines"] / profile["games_played"], 2
            )
            high_score_store.save_profile(profile)
            game_over_recorded = True

        renderer.draw_game(
            state,
            high_score=high_score,
            mode_name=MODE_LABELS[current_mode],
            mode_detail=mode_detail,
        )

    pygame.quit()


if __name__ == "__main__":
    run()
