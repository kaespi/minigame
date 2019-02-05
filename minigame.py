
import pygame
import os

from src.config import Gameconfig
from src.grid import Grid
import src.gameaction
from src.player import Player
from src.bug import Bug


def tmg_main():
    """Main starting point for the game to take off"""
    cfg = Gameconfig()
    pygame.init()

    # initialize the window
    screen = pygame.display.set_mode(cfg.screen_size)

    grid = Grid(cfg, screen)
    grid.read_grid(os.path.join(os.path.dirname(__file__), 'levels', 'level_test1.txt'))
    grid.check_grid()

    grid.init_squares()

    player = Player(cfg, screen)
    player.set_grid(grid)
    player.set_position(grid.players_start[0][0], grid.players_start[0][1])
    players = [player]

    # initializes the bugs
    bugs = []
    bugs_start = grid.get_bugs_start()
    for bug_start in bugs_start:
        bug = Bug(cfg, screen)
        bug.set_grid(grid)
        bug.set_position(bug_start[0], bug_start[1])
        bug.find_starting_direction()
        # only if the bug can move set the velocity
        if bug.move_direction is not None:
            bug.vel = cfg.speed
        bugs.append(bug)

    src.gameaction.run_level(screen, cfg, grid, players, bugs)


tmg_main()
