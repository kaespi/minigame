import pygame
import json


class Gameconfig():
    """Handles the configuration options for the game"""

    def __init__(self):
        """Constructor for the Gameconfig class"""

        # load default values first

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

        # menu
        self.menu_entry_color_bg = None             # background color for the menu entries square (RGB)
        self.menu_entry_color_sel = (0, 50, 150)    # background color for the selected menu entries (RGB)
        self.menu_entry_alpha_bg = 160              # alpha for the menu entries squares (0=full transparent, 255=not)
        self.menu_entry_color_text = (255, 255, 0)  # text color for the menu (RGB)

        self.load_config()

    def store_config(self):
        """Stores selected configuration values to settings.json on the harddisk (to be read back next time)"""
        with open('settings.json', 'w') as file_obj:
            # it doesn't make sense to store all configuration values. Only those which can be
            # configured in the menu make actually sense
            cfg = {'player1_up': self.player1_up,
                   'player1_right': self.player1_right,
                   'player1_dow': self.player1_down,
                   'player1_left': self.player1_left,
                   'player2_up': self.player2_up,
                   'player2_right': self.player2_right,
                   'player2_down': self.player2_down,
                   'player2_left': self.player2_left}
            json.dump(cfg, file_obj)

    def load_config(self):
        """Retrieves some configuration values from settings.json (if present)"""
        try:
            with open('settings.json', 'r') as file_obj:
                cfg = json.load(file_obj)

                # be careful: somebody might have modified the file and therefore not all
                # desired keys have to be present
                if 'player1_up' in cfg:
                    self.player1_up = cfg['player1_up']
                if 'player1_right' in cfg:
                    self.player1_right = cfg['player1_right']
                if 'player1_down' in cfg:
                    self.player1_down = cfg['player1_down']
                if 'player1_left' in cfg:
                    self.player1_left = cfg['player1_left']
                if 'player2_up' in cfg:
                    self.player2_up = cfg['player2_up']
                if 'player2_right' in cfg:
                    self.player2_right = cfg['player2_right']
                if 'player2_down' in cfg:
                    self.player2_down = cfg['player2_down']
                if 'player2_left' in cfg:
                    self.player2_left = cfg['player2_left']
        except FileNotFoundError:
            # there's no settings file present yet, therefore create one
            self.store_config()
