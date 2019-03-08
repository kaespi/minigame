import enum


class Direction(enum.Enum):
    """Movement directions"""
    up = 0
    right = 1
    down = 2
    left = 3


class Menuentry(enum.Enum):
    """Entries in the game menu"""
    run_level_1p = 1
    run_level_2p = 2
    settings = 3
    exit = 4
    continue_game = 5
    abort_game = 6
    player_1_settings = 7
    player_2_settings = 8
    back = 9


class LevelResult(enum.Enum):
    """Result of a level"""
    success = 0 # level was completed successfully
    abort = 1   # level was aborted (through the ESC-menu)
    fail = 2    # level failed (caught by bug)
    error = 3   # level error (e.g. wrongly composed level file)
