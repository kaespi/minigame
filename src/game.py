import pygame
import os
import time

from src.config import Gameconfig
from src.menu import Menu
from src.grid import Grid
from src.player import Player
from src.bug import Bug
from src.gameaction import bug_catched_player, bounce_back
from src.enumtypes import Direction, Menuentry, LevelResult
import src.util as util


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
            if menu_choice == Menuentry.run_level_1p:
                self.start_game(num_players=1)
            elif menu_choice == Menuentry.run_level_2p:
                self.start_game(num_players=2)
            else:
                exit_menu = True

    def start_game(self, num_players=1):
        """Starts the game with a given number of players"""
        levels = util.scan_for_levels(num_players)
        level_num = 1
        for level in levels:
            if self.load_level(level):
                level_result = self.run_level(level_num)

                if level_result == LevelResult.abort:
                    # level was aborted, therefore stop the game
                    return False
            level_num += 1

        return True

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

    def run_level(self, level=None):
        """Runs a level (main while loop during playing)"""
        if self.grid is None or len(self.players) == 0:
            # if there's no grid or no player cannot do anything and therefore terminate early
            return LevelResult.error

        if level is not None:
            self.level_countdown(level)

        t_ms = pygame.time.get_ticks()

        while True:
            # needed to keep the events in sync with the system. According to pygame manual should
            # should be called once per game loop
            pygame.event.pump()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        in_game_menu_choice = self.menu.in_game_menu()
                        if in_game_menu_choice == Menuentry.abort_game:
                            return LevelResult.abort
                        t_ms = pygame.time.get_ticks()
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

            # save CPU: if no full millisecond elapsed since the last update, there's really
            # no need to redraw everythiing. Therefore just continue
            if dt_ms == 0:
                continue

            # move the players and bugs on the grid on time step ahead
            for player in self.players:
                player.update_position(dt_ms)
            for bug in self.bugs:
                bug.update_position(dt_ms, self.players)

            # let the bugs bounce back when they hit each other
            bounce_back(self.bugs, self.cfg.bug_size/self.cfg.grid_height)

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

            # drawing
            self.draw_game_screen()

            if not any_player_alive:
                time.sleep(2)
                return LevelResult.fail
            elif not any_square_not_complete:
                time.sleep(2)
                return LevelResult.success

    def draw_game_screen(self):
        """Draws the game (i.e. grid, players, bugs)"""
        # drawing
        self.screen.fill(self.cfg.bg_color)

        # draw the grid
        self.grid.draw_grid()

        # draw the players and bugs
        for player in self.players:
            player.draw()
        for bug in self.bugs:
            bug.draw()

        pygame.display.update()

    def level_countdown(self, level=1):
        """Starts the countdown for the level"""
        # draws the game in the background (to help the player familiarize himself with the level)
        self.draw_game_screen()

        # empty the past events first (the user can abort the countdown by pressing
        # any key...)
        pygame.event.pump()
        pygame.event.get()

        t_start_ms = pygame.time.get_ticks() + 2000

        end_countdown = False
        while not end_countdown and pygame.time.get_ticks() < t_start_ms:
            time.sleep(0.005)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    end_countdown = True
                    break
