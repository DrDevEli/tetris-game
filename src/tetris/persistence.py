"""Persistence helpers for local game data."""

from __future__ import annotations

import json
from pathlib import Path


class HighScoreStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path(".tetris_highscore.json")

    def load(self) -> int:
        if not self.path.exists():
            return 0
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return 0
        return int(payload.get("high_score", 0))

    def save(self, score: int) -> None:
        payload = {"high_score": max(0, int(score))}
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
