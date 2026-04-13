# Contructor

A playable block-stacking game built with Python and Pygame.

## Features

- 7-bag randomizer for fair piece distribution
- Rotation with basic wall kicks
- Soft drop and hard drop scoring
- Line clear scoring and level-based speed increase
- Pause and restart controls
- Next piece preview and ghost piece
- Start screen before gameplay
- Mode select screen: Classic, Sprint (40 lines), Ultra (2 minutes)
- Generated sound effects for move/rotate/lock/line clear/game over
- Local high-score persistence in `.tetris_highscore.json`
- Local profile stats persistence: best score, total lines, games played, avg lines/game
- Settings menu with music/SFX volume, keybind remap, and fullscreen toggle

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -e ".[dev]"
```

## Run

```bash
python -m src.main
```

## Test

```bash
pytest
```

## Controls

- Left / A: move left
- Right / D: move right
- Down / S: soft drop
- Up / W / X: rotate clockwise
- Z: rotate counterclockwise
- Space: hard drop
- P: pause
- R: restart
- Esc: quit
- Enter: start from title screen
- Enter on title: open mode select
- O: open settings

