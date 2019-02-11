
class Lang():
    """offers multi-language support for the game"""

    def __init__(self, locale='en'):
        """Constructor for the Lang class"""
        # translations (default, if there's no localization available for a selected language
        self.trans = {'menu_main_play_1p': 'Single Player',
                      'menu_main_play_2p': 'Two Player',
                      'menu_main_settings': 'Settings',
                      'menu_main_quit': 'Quit',
                      'menu_game_continue': 'Continue',
                      'menu_game_end_game': 'End Game',
                      'menu_settings_player1': 'Player 1 Controls',
                      'menu_settings_player2': 'Player 2 Controls',
                      'menu_settings_back': 'Back',
                      'menu_settings_key_right': 'Press key for "Right"',
                      'menu_settings_key_left': 'Press key for "Left"',
                      'menu_settings_key_up': 'Press key for "Up"',
                      'menu_settings_key_down': 'Press key for "Down"',}
