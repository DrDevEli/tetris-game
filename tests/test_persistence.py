from pathlib import Path

from tetris.persistence import HighScoreStore


def test_load_missing_file_returns_zero(tmp_path: Path) -> None:
    store = HighScoreStore(path=tmp_path / "hs.json")
    assert store.load() == 0


def test_save_and_load_high_score(tmp_path: Path) -> None:
    store = HighScoreStore(path=tmp_path / "hs.json")
    store.save(1234)
    assert store.load() == 1234
