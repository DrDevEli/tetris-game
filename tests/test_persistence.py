from pathlib import Path

from tetris.config import DEFAULT_SETTINGS
from tetris.persistence import HighScoreStore


def test_load_missing_file_returns_zero(tmp_path: Path) -> None:
    store = HighScoreStore(path=tmp_path / "hs.json")
    assert store.load() == 0


def test_save_and_load_high_score(tmp_path: Path) -> None:
    store = HighScoreStore(path=tmp_path / "hs.json")
    store.save(1234)
    assert store.load() == 1234


def test_load_settings_defaults(tmp_path: Path) -> None:
    store = HighScoreStore(path=tmp_path / "hs.json")
    settings = store.load_settings()
    assert settings["music_volume"] == DEFAULT_SETTINGS["music_volume"]
    assert settings["keybinds"]["hard_drop"] == DEFAULT_SETTINGS["keybinds"]["hard_drop"]


def test_save_settings_persists_values(tmp_path: Path) -> None:
    store = HighScoreStore(path=tmp_path / "hs.json")
    settings = store.load_settings()
    settings["music_volume"] = 0.9
    settings["keybinds"]["move_left"] = ["j"]
    store.save_settings(settings)
    loaded = store.load_settings()
    assert loaded["music_volume"] == 0.9
    assert loaded["keybinds"]["move_left"] == ["j"]


def test_profile_defaults_and_average(tmp_path: Path) -> None:
    store = HighScoreStore(path=tmp_path / "hs.json")
    profile = store.load_profile()
    assert profile["best_score"] == 0
    assert profile["total_lines"] == 0
    assert profile["games_played"] == 0
    assert profile["avg_lines_per_game"] == 0.0


def test_save_profile_persists_stats(tmp_path: Path) -> None:
    store = HighScoreStore(path=tmp_path / "hs.json")
    store.save_profile({"best_score": 999, "total_lines": 120, "games_played": 8})
    profile = store.load_profile()
    assert profile["best_score"] == 999
    assert profile["total_lines"] == 120
    assert profile["games_played"] == 8
    assert profile["avg_lines_per_game"] == 15.0
