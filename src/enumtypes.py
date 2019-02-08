import enum


class Direction(enum.Enum):
    """Movement directions"""
    up = 0
    right = 1
    down = 2
    left = 3

class Menuentry(enum.Enum):
    """Entries in the game menu"""
    run_level = 1
    exit = 2