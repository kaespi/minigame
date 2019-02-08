import sys

v = sys.version_info
if v[0] < 3:
    print("Minigame needs Python 3 to run")
    sys.exit(1)

import src.game


def tmg_main():
    """Main starting point for the game to take off"""
    game = src.game.Game()
    game.launch_menu()


tmg_main()
