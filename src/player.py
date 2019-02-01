import pygame

from src.runner import Runner
from src.enumtypes import Direction
from src.gridutil import grid_index


class Player(Runner):
    """This is the class for a player running around on the grid"""

    def __init__(self, cfg, screen):
        """Constructor for the Player class"""
        # geometric details
        self.color = cfg.player_color
        self.r = int(0.5 * cfg.player_size)

        super().__init__(cfg, screen)

    def draw(self):
        """Draws the player"""
        if self.x is not None and self.y is not None:
            x = int(self.x * self.cfg.grid_height + self.cfg.grid_origin[0] + 0.5)
            y = int(self.y * self.cfg.grid_height + self.cfg.grid_origin[1] + 0.5)
            pygame.draw.circle(self.screen, self.color, (x, y), self.r, 0)

    def update_position(self, dt_ms):
        """updates the position of the player"""

        if dt_ms > 0:
            # reset the node visited (but only if it's not the second part of a partial movement)
            if self.dt_ms_rem == 0:
                self.node_visited_x = None
                self.node_visited_y = None

            node_crossed = False

            can_move = self.can_move_on()

            # backup from the the player started moving
            x_start = self.x
            y_start = self.y

            if can_move:
                node_crossed = self.move(dt_ms)

            if x_start != self.x or y_start != self.y:
                # need to update the corresponding gridline
                self.update_gridline_done((x_start, y_start), (self.x, self.y))

            # if a node was crossed in the movement above then another move has to be executed
            # (but since the remaining time was recorded internally we don't have to worry
            # about what's remaining)
            if node_crossed:
                # there's a movement direction change "queued". Apply it now. The player risks
                # that this will lead to no movement, because it's not possible. But this has
                # to be left to the player!

                old_direction = self.move_direction
                old_vel = self.vel

                if self.next_direction is not None:
                    self.move_direction = self.next_direction
                    self.next_direction = None

                can_move = self.can_move_on()

                if can_move:
                    self.move(0)
                else:
                    # restore the previous (i.e. current) movement and continue with it if possible. If
                    # possible then the commanded direction change has to be applied later. If cannot continue
                    # with the previous (i.e. current) movement then stand still
                    self.vel = old_vel
                    self.next_direction = self.move_direction
                    self.move_direction = old_direction

                    if self.can_move_on():
                        self.move(0)
                    else:
                        self.vel = 0
                        self.move_direction = None
                        self.next_direction = None

            self.dt_ms_rem = 0

    def command_direction(self, new_move_direction):
        """Changes the movement direction of the player (only if allowed!)"""
        self.next_direction = None  # reset the "queued" movement change
        if self.vel == 0:
            # check if we can start moving in a certain direction
            self.vel = self.cfg.speed
            self.move_direction = new_move_direction
            if not self.can_move_on():
                # cannot move in the desired direction: therefore reset the movement
                self.vel = 0
                self.move_direction = None
        elif self.move_direction != new_move_direction:
            # the player is already moving, let's check if the new commanded direction is immediately taking action
            # or if we just store it
            if (self.move_direction == Direction.up and new_move_direction == Direction.down) or \
                    (self.move_direction == Direction.down and new_move_direction == Direction.up) or \
                    (self.move_direction == Direction.right and new_move_direction == Direction.left) or \
                    (self.move_direction == Direction.left and new_move_direction == Direction.right):
                # a reverse of the direction is commanded, this can immediately by applied
                self.move_direction = new_move_direction
            else:
                # command is "queued" for later action at the next node
                self.next_direction = new_move_direction

    def update_gridline_done(self, p1, p2):
        """Updates the gridlines to mark the next piece as done"""
        ix_v = None
        ix_h = None
        if p1[0] != int(p1[0]) or p1[1] != int(p1[1]):
            ix_v, ix_h = grid_index(p1[0], p1[1])
            x_ref = int(p1[0])
            y_ref = int(p1[1])
        elif p2[0] != int(p2[0]) and p2[1] != int(p2[1]):
            ix_v, ix_h = grid_index(p2[0], p2[1])
            x_ref = int(p2[0])
            y_ref = int(p2[1])

        if (ix_v is not None) and (ix_h is not None):
            if self.move_direction == Direction.up or self.move_direction == Direction.down:
                self.grid.gridlines[ix_v][ix_h].update(p1[1] - y_ref, p2[1] - y_ref)
            else:
                self.grid.gridlines[ix_v][ix_h].update(p1[0] - x_ref, p2[0] - x_ref)
