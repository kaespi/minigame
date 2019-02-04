

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
