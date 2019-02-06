import pygame

import src.game


def tmg_main():
    """Main starting point for the game to take off"""
    pygame.init()

    game = src.game.Game()
    if game.load_level('level_test1.txt'):
        game.run_level()


tmg_main()
