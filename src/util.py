import os

from src.enumtypes import Direction


def get_reverse_direction(direction):
    """Returns the reverse direction (i.e. up(0)<->down(2), right(1)<->left(3)"""
    if direction is not None:
        if direction == Direction.up:
            direction = Direction.down
        elif direction == Direction.right:
            direction = Direction.left
        elif direction == Direction.down:
            direction = Direction.up
        elif direction == Direction.left:
            direction = Direction.right
        else:
            direction = None

    return direction


def scan_for_levels(num_players=1):
    """Scans the levels folder for level files"""
    path_to_file = os.path.dirname(os.path.realpath(__file__))
    path_to_levels = os.path.join(path_to_file, '..', 'levels')
    files_found = os.listdir(path_to_levels)
    level_files = []
    for file in files_found:
        if is_valid_level_file(file, num_players):
            level_files.append(os.path.join(path_to_levels, file))

    return sorted(level_files)


def is_valid_level_file(filename, num_players=None):
    """Returns True if the filename is a valid level filename"""
    # a level file should follow a naming pattern as level_Np_M.txt, with
    # N the number of players and M the level number

    valid_filename = True

    # 1. check the length of the filename
    if len(filename) < 14:
        valid_filename = False

    # 2. check for the file ending
    if valid_filename and filename[-4:] != '.txt':
        valid_filename = False

    # 3. check for the pattern
    if valid_filename:
        filename = filename[:-4]
        parts = filename.split('_')
        # should contain at least two underscores
        if len(parts) >= 3:
            # first part should be "level"
            if parts[0] != 'level':
                valid_filename = False
            # last part should be a number (level number)
            if not parts[-1].isdigit():
                valid_filename = False
            # second last part should be a number with "p" appended
            if parts[-2][-1] != 'p':
                valid_filename = False
            if not parts[-2][:-1].isdigit():
                valid_filename = False
            # the number of players argument should match the one selected
            if valid_filename and num_players is not None:
                if int(parts[-2][:-1]) != num_players:
                    valid_filename = False
        else:
            valid_filename = False

    return valid_filename
