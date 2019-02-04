import pygame

from src.runner import Runner
from src.enumtypes import Direction


class Bug(Runner):
    """This is the class for a bug running on the grid trying to catch the player"""

    def __init__(self, cfg, screen):
        """Constructor for the Bug class"""
        super().__init__(cfg, screen)

    def find_starting_direction(self):
        """Tries to find a valid starting moving direction"""
        if self.can_move_up():
            self.move_direction = Direction.up
        elif self.can_move_down():
            self.move_direction = Direction.down
        elif self.can_move_right():
            self.move_direction = Direction.right
        elif self.can_move_left():
            self.move_direction = Direction.left
        else:
            self.move_direction = None

    def draw(self):
        """Draws the bug"""
        if self.x is not None and self.y is not None:
            x = int(self.x * self.cfg.grid_height + self.cfg.grid_origin[0] + 0.5)
            y = int(self.y * self.cfg.grid_height + self.cfg.grid_origin[1] + 0.5)
            pygame.draw.circle(self.screen, self.cfg.bug_color, (x, y), int(0.5 * self.cfg.bug_size), 0)

    def reverse_direction(self):
        """Reverses the direction (i.e. up(0)<->down(2), right(1)<->left(3)"""
        if self.move_direction is not None:
            if self.move_direction == Direction.up:
                self.move_direction = Direction.down
            elif self.move_direction == Direction.right:
                self.move_direction = Direction.left
            elif self.move_direction == Direction.down:
                self.move_direction = Direction.up
            elif self.move_direction == Direction.left:
                self.move_direction = Direction.right
            else:
                self.move_direction = None

    def update_position(self, dt_ms):
        """updates the position of the bug"""

        if dt_ms > 0:
            node_crossed = False

            can_move = self.can_move_on()

            if can_move:
                node_crossed = self.move(dt_ms)
            else:
                self.reverse_direction()
                if can_move:
                    node_crossed = self.move(dt_ms)

            # if a node was crossed in the movement above then another move has to be executed
            # (but since the remaining time was recorded internally we don't have to worry
            # about what's remaining)
            if node_crossed:
                can_move = self.can_move_on()

                if can_move:
                    self.move(0)
                else:
                    self.reverse_direction()
                    can_move = self.can_move_on()
                    if can_move:
                        self.move(0)
                    self.dt_ms_rem = 0

            self.dt_ms_rem = 0
