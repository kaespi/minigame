import pygame
import os
import time

from src.config import Gameconfig
from src.menu import Menu
from src.grid import Grid
from src.player import Player
from src.bug import Bug
from src.gameaction import bug_catched_player
from src.enumtypes import Direction, Menuentry


class Game():
    """This is the main class for the game, handling all objects, menus, levels etc."""

    def __init__(self):
        """Constructor for the Game class"""
        # initializes pygame
        pygame.init()

        # loads the configuration (start with default values)
        self.cfg = Gameconfig()

        # initialize the window
        self.screen = pygame.display.set_mode(self.cfg.screen_size)

        # Instantiate the menu
        self.menu = Menu(self.screen, self.cfg)

        # initialize the main game objects
        self.grid = None
        self.players = []
        self.bugs = []

    def launch_menu(self):
        """Starts displaying the menu"""
        exit_menu = False
        while not exit_menu:
            menu_choice = self.menu.main_menu()
            if menu_choice == Menuentry.run_level:
                if self.load_level('level_test1.txt'):
                    level_result = self.run_level()
                    if level_result is None:
                        exit_menu = True
            else:
                exit_menu = True

    def load_level(self, filename):
        """Loads a level file"""

        # instantiate a new grid
        self.grid = Grid(self.cfg, self.screen)
        # parse the level/grid file
        self.grid.read_grid(os.path.join(os.path.dirname(__file__), '..', 'levels', filename))
        # check if the grid is ok
        success = self.grid.check_grid()

        if success:
            # initialize the squares between the gridlines
            self.grid.init_squares()

            # initialize the players
            self.players = []
            for player_start in self.grid.players_start:
                player = Player(self.cfg, self.screen)
                player.set_grid(self.grid)
                player.set_position(player_start[0], player_start[1])
                self.players.append(player)

            # initializes the bugs
            self.bugs = []
            bugs_start = self.grid.get_bugs_start()
            for bug_start in bugs_start:
                bug = Bug(self.cfg, self.screen)
                bug.set_grid(self.grid)
                bug.set_position(bug_start[0], bug_start[1])
                bug.find_starting_direction()
                # only if the bug can move set the velocity
                if bug.move_direction is not None:
                    bug.vel = self.cfg.speed
                self.bugs.append(bug)

        else:
            # the grid is illegal, therefore reset the grid variable
            self.grid = None

        return success

    def run_level(self):
        """Runs a level (main while loop during playing)"""
        if self.grid is None or len(self.players) == 0:
            # if there's no grid or no player cannot do anything and therefore terminate early
            return None

        t_ms = pygame.time.get_ticks()

        while True:
            self.screen.fill(self.cfg.bg_color)

            # needed to keep the events in sync with the system. According to pygame manual should
            # should be called once per game loop
            pygame.event.pump()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                    elif event.key == self.cfg.player1_up and len(self.players) >= 1:
                        self.players[0].command_direction(Direction.up)
                    elif event.key == self.cfg.player1_right and len(self.players) >= 1:
                        self.players[0].command_direction(Direction.right)
                    elif event.key == self.cfg.player1_down and len(self.players) >= 1:
                        self.players[0].command_direction(Direction.down)
                    elif event.key == self.cfg.player1_left and len(self.players) >= 1:
                        self.players[0].command_direction(Direction.left)
                    elif event.key == self.cfg.player2_up and len(self.players) >= 2:
                        self.players[1].command_direction(Direction.up)
                    elif event.key == self.cfg.player2_right and len(self.players) >= 2:
                        self.players[1].command_direction(Direction.right)
                    elif event.key == self.cfg.player2_down and len(self.players) >= 2:
                        self.players[1].command_direction(Direction.down)
                    elif event.key == self.cfg.player2_left and len(self.players) >= 2:
                        self.players[1].command_direction(Direction.left)

            t_now_ms = pygame.time.get_ticks()
            dt_ms = t_now_ms - t_ms
            t_ms = t_now_ms

            # move the players and bugs on the grid on time step ahead
            for player in self.players:
                player.update_position(dt_ms)
            for bug in self.bugs:
                bug.update_position(dt_ms, self.players)

            # check if any bug caught any player
            bug_catched_player(self.bugs, self.players,
                               .5*self.cfg.bug_size/self.cfg.grid_height,
                               .5*self.cfg.player_size/self.cfg.grid_height)
            any_player_alive = False
            for player in self.players:
                if not player.caught:
                    any_player_alive = True

            any_square_not_complete = False
            for square in self.grid.squares:
                if not square.is_complete():
                    any_square_not_complete = True

            # draw the grid
            self.grid.draw_grid()

            # draw the players and bugs
            for player in self.players:
                player.draw()
            for bug in self.bugs:
                bug.draw()

            pygame.display.update()

            if not any_player_alive:
                print("Level failed")
                time.sleep(3)
                return False
            elif not any_square_not_complete:
                print("Level completed")
                time.sleep(3)
                return True
