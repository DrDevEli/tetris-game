"""Persistence helpers for local game data."""

from __future__ import annotations

import json
from pathlib import Path

from tetris.config import DEFAULT_SETTINGS

class HighScoreStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path(".tetris_highscore.json")

    def _load_payload(self) -> dict:
        if not self.path.exists():
            return {}
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}

    def load(self) -> int:
        return self.load_profile()["best_score"]

    def save(self, score: int) -> None:
        payload = self._load_payload()
        profile = self.load_profile()
        profile["best_score"] = max(profile["best_score"], max(0, int(score)))
        payload["profile"] = profile
        payload["high_score"] = profile["best_score"]
        if "settings" not in payload:
            payload["settings"] = DEFAULT_SETTINGS
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def load_profile(self) -> dict:
        payload = self._load_payload()
        profile = payload.get("profile", {})
        best = int(profile.get("best_score", payload.get("high_score", 0)))
        total_lines = int(profile.get("total_lines", 0))
        games_played = int(profile.get("games_played", 0))
        avg = (total_lines / games_played) if games_played > 0 else 0.0
        return {
            "best_score": max(0, best),
            "total_lines": max(0, total_lines),
            "games_played": max(0, games_played),
            "avg_lines_per_game": round(avg, 2),
        }

    def save_profile(self, profile: dict) -> None:
        payload = self._load_payload()
        games_played = max(0, int(profile.get("games_played", 0)))
        total_lines = max(0, int(profile.get("total_lines", 0)))
        best = max(0, int(profile.get("best_score", 0)))
        payload["profile"] = {
            "best_score": best,
            "total_lines": total_lines,
            "games_played": games_played,
        }
        payload["high_score"] = best
        payload.setdefault("settings", DEFAULT_SETTINGS)
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def load_settings(self) -> dict:
        payload = self._load_payload()
        merged = DEFAULT_SETTINGS.copy()
        stored = payload.get("settings", {})
        merged.update({k: v for k, v in stored.items() if k != "keybinds"})
        keybinds = DEFAULT_SETTINGS["keybinds"].copy()
        keybinds.update(stored.get("keybinds", {}))
        merged["keybinds"] = keybinds
        return merged

    def save_settings(self, settings: dict) -> None:
        payload = self._load_payload()
        payload["settings"] = settings
        payload.setdefault("high_score", 0)
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
