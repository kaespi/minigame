import pygame


class Gameconfig():
    """Handles the configuration options for the game"""

    def __init__(self):
        # screen
        self.screen_size = (400, 400)               # size of the screen [pixel]
        self.bg_color = (0, 0, 0)                   # screen background color (RGB)

        # grid
        self.grid_origin = (50, 50)                 # origin of the grid (left/top node)
        self.grid_color_fresh = (140, 140, 140)     # color of the grid, when it's not yet done (RGB)
        self.grid_color_done = (30, 0, 120)         # color of the grid, when it's done (RGB)
        self.grid_color_complete = (30, 0, 120)     # color of the grid, when it's completed (RGB)
        self.grid_width = 5                         # width of the grid lines [pixel]
        self.grid_height = 50                       # length of the grid lines [pixel]

        # squares
        self.square_color_fresh = (20, 20, 20)      # color of the square when it's not yet done (RGB)
        self.square_color_complete = (50, 50, 50)   # color of the square when it's completed (RGB)

        # players
        self.player_size = 10                       # diameter of the player [pixel]
        self.player_color = (0, 130, 0)             # color of the player (circle) (RGB)
        self.player_color_caught = (80, 80, 80)     # color of the player after it was caught (RGB)

        # bugs
        self.bug_size = 12                          # diameter of the bug [pixel]
        self.bug_color = (150, 30, 0)               # color of the bug (circle) (RGB)

        # game behavior
        self.speed = 0.0019                         # movement speed [pixel/ms]

        # controls
        self.player1_up = pygame.K_UP               # player 1: key up
        self.player1_right = pygame.K_RIGHT         # player 1: key right
        self.player1_down = pygame.K_DOWN           # player 1: key down
        self.player1_left = pygame.K_LEFT           # player 1: key left

        self.player2_up = pygame.K_w                # player 2: key up
        self.player2_right = pygame.K_d             # player 2: key right
        self.player2_down = pygame.K_s              # player 2: key down
        self.player2_left = pygame.K_a              # player 2: key left
