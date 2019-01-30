import pygame

from config import Gameconfig
from grid import Grid
from square import Square
from player import Player
from bug import Bug
from enumtypes import Direction


def tmg_main():
    """Main starting point for the game to take off"""
    cfg = Gameconfig()
    pygame.init()

    # initialize the window
    screen = pygame.display.set_mode(cfg.screen_size)

    grid = Grid(cfg, screen)
    #grid.read_grid("level_test2.txt")
    grid.read_grid("test_grid1.txt")
    grid.check_grid()

    player = Player(cfg, screen)
    player.set_grid(grid)
    player.set_position(1, 1)
    players = [player]

    squares = [Square(cfg, screen, (0, 0))]
    squares[0].surrounding_gridlines = [grid.gridlines[0][0],
                                        grid.gridlines[1][0],
                                        grid.gridlines[1][1],
                                        grid.gridlines[2][0]]

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

        any_square_not_complete = False
        for square in squares:
            if not square.is_complete():
                any_square_not_complete = True
        if not any_square_not_complete:
            print("Level completed")
            break

        # draw the grid
        for square in squares:
            square.draw()
        grid.draw_grid()

        # draw the players and bugs
        for player in players:
            player.draw()
        for bug in bugs:
            bug.draw()

        pygame.display.update()


tmg_main()
