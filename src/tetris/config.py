"""Game constants and balancing values."""

SCREEN_WIDTH = 520
SCREEN_HEIGHT = 720
FPS = 60

BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLOCK_SIZE = 30

BOARD_OFFSET_X = 40
BOARD_OFFSET_Y = 40

PREVIEW_OFFSET_X = BOARD_OFFSET_X + BOARD_WIDTH * BLOCK_SIZE + 40
PREVIEW_OFFSET_Y = 120

COLORS = {
    "bg": (18, 18, 24),
    "grid": (35, 35, 45),
    "text": (235, 235, 245),
    "I": (80, 220, 240),
    "O": (245, 220, 60),
    "T": (180, 90, 220),
    "S": (90, 210, 120),
    "Z": (230, 90, 90),
    "J": (90, 120, 230),
    "L": (240, 160, 80),
}

LINES_PER_LEVEL = 10
SOFT_DROP_POINTS = 1
HARD_DROP_POINTS = 2

LINE_CLEAR_POINTS = {
    1: 100,
    2: 300,
    3: 500,
    4: 800,
}

BASE_FALL_DELAY_MS = 700
MIN_FALL_DELAY_MS = 80
FALL_SPEED_STEP_MS = 55

DEFAULT_SETTINGS = {
    "music_volume": 0.35,
    "sfx_volume": 0.7,
    "fullscreen": False,
    "keybinds": {
        "move_left": ["left", "a"],
        "move_right": ["right", "d"],
        "soft_drop": ["down", "s"],
        "rotate_cw": ["up", "w", "x"],
        "rotate_ccw": ["z"],
        "hard_drop": ["space"],
        "pause": ["p"],
        "restart": ["r"],
        "settings": ["o"],
    },
}
