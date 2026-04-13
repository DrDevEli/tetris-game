"""Simple generated sounds for game events."""

from __future__ import annotations

import math
from array import array

import pygame


class SoundManager:
    def __init__(self) -> None:
        self.enabled = False
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=1)
            self.enabled = True
            self.sounds = {
                "move": self._tone(220, 0.03, 0.14),
                "rotate": self._tone(320, 0.04, 0.16),
                "lock": self._tone(170, 0.05, 0.2),
                "line": self._tone(520, 0.08, 0.2),
                "hard_drop": self._tone(120, 0.08, 0.2),
                "game_over": self._tone(95, 0.35, 0.18),
            }
            self.music = self._tone(130, 1.2, 0.08)
            self.music_channel = pygame.mixer.Channel(1)
        except pygame.error:
            self.enabled = False

    def play(self, event: str) -> None:
        if not self.enabled:
            return
        sound = self.sounds.get(event)
        if sound:
            sound.play()

    def play_music(self) -> None:
        if not self.enabled:
            return
        if not self.music_channel.get_busy():
            self.music_channel.play(self.music, loops=-1)

    def set_sfx_volume(self, volume: float) -> None:
        if not self.enabled:
            return
        for sound in self.sounds.values():
            sound.set_volume(max(0.0, min(1.0, volume)))

    def set_music_volume(self, volume: float) -> None:
        if not self.enabled:
            return
        self.music_channel.set_volume(max(0.0, min(1.0, volume)))

    def _tone(self, frequency: int, duration: float, volume: float) -> pygame.mixer.Sound:
        sample_rate = 44100
        sample_count = max(1, int(duration * sample_rate))
        buffer = array("h")
        amplitude = int(32767 * max(0.0, min(1.0, volume)))
        for i in range(sample_count):
            t = i / sample_rate
            buffer.append(int(amplitude * math.sin(2 * math.pi * frequency * t)))
        return pygame.mixer.Sound(buffer=buffer.tobytes())
