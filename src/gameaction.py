import pygame

from src.gridutil import grid_index_right, grid_index_down
from src.enumtypes import Direction


def bug_catched_player(bugs, players, bug_size=10/50, player_size=8/50):
    """Checks if any bug catched a player"""
    for bug in bugs:
        for player in players:
            if not player.caught:
                # compute the "Euclidean distance" between the bug and the player. If it is below the
                # sum of bug_size and player_size, the player has to be declared as "caught"
                dx = bug.x - player.x
                dy = bug.y - player.y
                d = dx*dx + dy*dy

                if d < (bug_size+player_size)*(bug_size+player_size):
                    player.caught = True


def can_you_see_me(p1, p2, gridlines):
    """Tries to find out whether positions p1 and p2 are connected with a (series of) horizontal/vertical gridline"""
    can_see = False

    if p1 == p2:
        return True

    if int(p1[1]) == p1[1] and p1[1] == p2[1]:
        gap_found = False

        # p1 and p2 seem to be both on a horizontal grid line with the same y-coordinate. Now we have
        # to check if there's no gap in between the two
        if p1[0] <= p2[0]:
            x1 = p1[0]
            x2 = p2[0]
        else:
            x1 = p2[0]
            x2 = p1[0]

        x_left = int(x1)
        ix_v, ix_h = grid_index_right(x_left, p1[1])
        while x_left < x2:
            if ix_h >= len(gridlines[ix_v]) or gridlines[ix_v][ix_h] is None:
                gap_found = True
                break
            x_left += 1
            ix_h += 1

        can_see = not gap_found

    elif int(p1[0]) == p1[0] and p1[0] == p2[0]:
        # p1 and p2 seem to be both on a vertical grid line with the same x-coordinate. Now we have
        # to check if there's no gap in between the two
        gap_found = False

        if p1[1] <= p2[1]:
            y1 = p1[1]
            y2 = p2[1]
        else:
            y1 = p2[1]
            y2 = p1[1]

        y_top = int(y1)
        ix_v, ix_h = grid_index_down(p1[0], y_top)
        while y_top < y2:
            if ix_v >= len(gridlines) or gridlines[ix_v][ix_h] is None:
                gap_found = True
                break
            y_top += 1
            ix_v += 2

        can_see = not gap_found

    return can_see


def run_level(screen, cfg, grid, players, bugs):
    """Runs a level (main while loop during playing)"""
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
            bug.update_position(dt_ms, players)

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