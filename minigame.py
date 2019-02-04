
import pygame
import os

from src.config import Gameconfig
from src.grid import Grid
from src.gameaction import bug_catched_player
from src.player import Player
from src.bug import Bug
from src.enumtypes import Direction


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

    t_ms = pygame.time.get_ticks()

    while True:
        screen.fill(cfg.bg_color)

        # needed to keep the events in sync with the system. According to pygame manual should
        # should be called once per game loop
        pygame.event.pump()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
                elif event.key == pygame.K_UP:
                    players[0].command_direction(Direction.up)
                elif event.key == pygame.K_RIGHT:
                    players[0].command_direction(Direction.right)
                elif event.key == pygame.K_DOWN:
                    players[0].command_direction(Direction.down)
                elif event.key == pygame.K_LEFT:
                    players[0].command_direction(Direction.left)

        t_now_ms = pygame.time.get_ticks()
        dt_ms = t_now_ms - t_ms
        t_ms = t_now_ms

        # move the players and bugs on the grid on time step ahead
        for player in players:
            player.update_position(dt_ms)
        for bug in bugs:
            bug.update_position(dt_ms)

        # check if any bug caught any player
        bug_catched_player(bugs, players, .5*cfg.bug_size/cfg.grid_height, .5*cfg.player_size/cfg.grid_height)

        any_square_not_complete = False
        for square in grid.squares:
            if not square.is_complete():
                any_square_not_complete = True
        if not any_square_not_complete:
            print("Level completed")
            break

        # draw the grid
        grid.draw_grid()

        # draw the players and bugs
        for player in players:
            player.draw()
        for bug in bugs:
            bug.draw()

        pygame.display.update()


tmg_main()
