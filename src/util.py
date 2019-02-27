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
