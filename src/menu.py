import pygame

from src.enumtypes import Menuentry

class Menu():
    """Class handling the game menu"""

    def __init__(self, screen, cfg):
        """Constructor for class Menu"""
        self.screen = screen
        self.cfg = cfg

        print(self.screen.get_height())

    def main_menu(self):
        """Displays the main menu"""
        menu_entries = [{'key': Menuentry.run_level, 'text': 'Play'},
                        {'key': Menuentry.exit, 'text': 'Quit'}]
        choice = self.show_menu(menu_entries)
        if choice is None:
            return Menuentry.exit
        else:
            return choice

    def in_game_menu(self):
        """Displays the menu during the game"""
        menu_entries = [{'key': Menuentry.continue_game, 'text': 'Continue'},
                        {'key': Menuentry.abort_game, 'text': 'End Game'}]
        return self.show_menu(menu_entries, escape_allowed=False)

    def show_menu(self, entries, selected=0, escape_allowed=True):
        """Displays a menu with a number of (vertically arranged) entries"""

        # derive the font size from the amount of space available
        font_size = int(self.screen.get_height() / 9)

        # load font, prepare values
        font = pygame.font.Font(None, font_size)

        update_display = True

        # empty the past events first
        pygame.event.pump()
        pygame.event.get()

        while True:
            if update_display:
                self.draw_menu(entries, selected, font, font_size)

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
                    elif event.key == pygame.K_UP and selected > 0:
                        selected -= 1
                    elif event.key == pygame.K_RETURN:
                        return entries[selected]['key']

    def draw_menu(self, entries, selected, font, font_size):
        """Actually draws the menu and updates the display"""
        y = 10

        self.screen.fill(self.cfg.bg_color)

        for ix in range(0, len(entries)):
            if selected == ix:
                render_surface = font.render(entries[ix]['text'], 0, (255, 255, 0), (0, 0, 100))
            else:
                render_surface = font.render(entries[ix]['text'], 0, (255, 255, 0), (0, 0, 0))
            self.screen.blit(render_surface, (10, y))

            y += int(font_size * 1.5)

        pygame.display.update()
