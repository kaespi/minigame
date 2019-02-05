
from src.gridutil import grid_index_right, grid_index_down


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
