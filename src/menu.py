import pygame
import time

from src.enumtypes import Menuentry
from src.lang import Lang

class Menu():
    """Class handling the game menu"""

    def __init__(self, screen, cfg):
        """Constructor for class Menu"""
        self.screen = screen
        self.cfg = cfg
        self.lang = Lang()

    def main_menu(self):
        """Displays the main menu"""
        menu_entries = [{'key': Menuentry.run_level_1p, 'text': self.lang.trans['menu_main_play_1p']},
                        {'key': Menuentry.run_level_2p, 'text': self.lang.trans['menu_main_play_2p']},
                        {'key': Menuentry.settings, 'text': self.lang.trans['menu_main_settings']},
                        {'key': Menuentry.exit, 'text': self.lang.trans['menu_main_quit']}]
        choice = self.show_menu(menu_entries)
        if choice is None:
            return Menuentry.exit
        elif choice == Menuentry.settings:
            return self.settings_menu()
        else:
            return choice

    def in_game_menu(self):
        """Displays the menu during the game"""
        menu_entries = [{'key': Menuentry.continue_game, 'text': self.lang.trans['menu_game_continue']},
                        {'key': Menuentry.abort_game, 'text': self.lang.trans['menu_game_end_game']}]
        return self.show_menu(menu_entries, escape_allowed=False, clear_background=False)

    def settings_menu(self):
        """Displays the settings menu"""
        menu_entries = [{'key': Menuentry.player_1_settings, 'text': self.lang.trans['menu_settings_player1']},
                        {'key': Menuentry.player_2_settings, 'text': self.lang.trans['menu_settings_player2']},
                        {'key': Menuentry.back, 'text': self.lang.trans['menu_settings_back']}]
        choice = self.show_menu(menu_entries)
        if choice is None or choice == Menuentry.back:
            return self.main_menu()
        elif choice == Menuentry.player_1_settings:
            return self.config_player_controls_menu(1)
        elif choice == Menuentry.player_2_settings:
            return self.config_player_controls_menu(2)

    def config_player_controls_menu(self, player_num=1):
        """Handles the menu for configuring the controls for any player"""
        if player_num == 1:
            self.cfg.player1_right = self.get_player_key(self.lang.trans['menu_settings_key_right'])
            self.cfg.player1_left = self.get_player_key(self.lang.trans['menu_settings_key_left'])
            self.cfg.player1_up = self.get_player_key(self.lang.trans['menu_settings_key_up'])
            self.cfg.player1_down = self.get_player_key(self.lang.trans['menu_settings_key_down'])
        elif player_num == 2:
            self.cfg.player2_right = self.get_player_key(self.lang.trans['menu_settings_key_right'])
            self.cfg.player2_left = self.get_player_key(self.lang.trans['menu_settings_key_left'])
            self.cfg.player2_up = self.get_player_key(self.lang.trans['menu_settings_key_up'])
            self.cfg.player2_down = self.get_player_key(self.lang.trans['menu_settings_key_down'])

        return self.settings_menu()

    def get_player_key(self, text):
        """Shows a menu entry for getting the player's keys"""
        # derive the font size from the amount of space available
        font_size = int(self.screen.get_height() / 9)

        # load font, prepare values
        font = pygame.font.Font(None, font_size)

        # empty the past events first
        pygame.event.pump()
        pygame.event.get()

        entries = [{'key': None, 'text': text}]
        self.draw_menu(entries, None, font, font_size, clear_background=True)

        key_detected = None
        while key_detected is None:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    key_detected = event.key
                    break
            time.sleep(0.005)

        return key_detected

    def show_menu(self, entries, selected=0, escape_allowed=True, clear_background=True):
        """Displays a menu with a number of (vertically arranged) entries"""

        # derive the font size from the amount of space available
        font_size = int(self.screen.get_height() / 9)

        # load font, prepare values
        font = pygame.font.Font(None, font_size)

        update_display = True

        # copy the current state of the screen (including all its drawings)
        if clear_background:
            screen_orig = None
        else:
            screen_orig = self.screen.copy()

        # empty the past events first
        pygame.event.pump()
        pygame.event.get()

        while True:
            if update_display:
                self.draw_menu(entries, selected, font, font_size, clear_background, screen_orig)

            update_display = False

            # needed to keep the events in sync with the system. According to pygame manual should
            # should be called once per game loop
            pygame.event.pump()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and escape_allowed:
                        return None
                    elif event.key == pygame.K_DOWN and selected < len(entries)-1:
                        selected += 1
                        update_display = True
                    elif event.key == pygame.K_UP and selected > 0:
                        selected -= 1
                        update_display = True
                    elif event.key == pygame.K_RETURN:
                        return entries[selected]['key']

    def draw_menu(self, entries, selected, font, font_size, clear_background=False, background_surface=None):
        """Actually draws the menu and updates the display"""
        screen_width, screen_height = self.screen.get_size()

        if clear_background:
            self.screen.fill(self.cfg.bg_color)

        if background_surface:
            self.screen.blit(background_surface, (0, 0))

        box_width = 0
        box_height = 0

        surfaces_text = []
        for entry in entries:
            s = font.render(entry['text'], 1, self.cfg.menu_entry_color_text)

            surfaces_text.append(s)
            w, h = s.get_size()
            if w > box_width:
                box_width = w
            if h > box_height:
                box_height = h

        d = int(box_height * 0.1)
        box_height += d
        box_width += d

        dy = int(font_size * 1.5)

        menu_height = (len(entries)-1) * dy + box_height
        y = int((screen_height - menu_height) / 3)

        if box_width < screen_width / 2:
            box_width = int(screen_width/2)

        box_x = int((screen_width - box_width)/2)

        for ix in range(0, len(surfaces_text)):
            if selected == ix and self.cfg.menu_entry_color_sel is not None:
                # draw the box of a selected menu entry (if configured)
                surface_rect = pygame.Surface((box_width, box_height))
                surface_rect.fill(self.cfg.menu_entry_color_sel)
                surface_rect.set_alpha(self.cfg.menu_entry_alpha_bg)
                self.screen.blit(surface_rect, (box_x, y))
            elif selected != ix and self.cfg.menu_entry_color_bg is not None:
                # draw the box of a not-selected menu entry (if configured)
                surface_rect = pygame.Surface((box_width, box_height))
                surface_rect.fill(self.cfg.menu_entry_color_bg)
                surface_rect.set_alpha(self.cfg.menu_entry_alpha_bg)
                self.screen.blit(surface_rect, (box_x, y))

            w = surfaces_text[ix].get_width()
            text_x = int((screen_width - w)/2)
            # ok, we have to "cheat" here, because the size of the surface doesn't take into account if the
            # space below the line (for e.g. y, g, characters) is actually used or not
            h = get_true_text_height(font, entries[ix]['text'])
            text_y = y + int((box_height - h)/2 - 0.5)
            self.screen.blit(surfaces_text[ix], (text_x, text_y))
            y += dy

        pygame.display.update()


def get_true_text_height(font, text):
    """Returns the true height of the text (in pixels) for a given font and string"""

    # unfortunately the height is more complicated compared to the width, because pygame doesn't
    # return the real height, but the height to be expected for all characters in this font. I.e.
    # it does take into account that there are characters which have some parts below the "bottom
    # line" (e.g. y, g, p). But if there's no such character that's too much. We really want to
    # center the text, vertically
    y_min = 0
    y_max = 0
    for metric in font.metrics(text):
        if metric[2] < y_min:
            y_min = metric[2]
        if metric[3] > y_max:
            y_max = metric[3]

    return y_max - y_min
