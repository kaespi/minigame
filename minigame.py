import sys

v = sys.version_info
if v[0] < 3:
    print("Minigame needs Python 3 to run")
    sys.exit(1)

import src.game


def tmg_main():
    """Main starting point for the game to take off"""
    game = src.game.Game()
    if game.load_level('level_test1.txt'):
        game.run_level()


tmg_main()
