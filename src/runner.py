
from src.gridutil import grid_index_up, grid_index_right, grid_index_down, grid_index_left
from src.enumtypes import Direction

class Runner():
    """This class handles objects moving/running on the grid"""

    def __init__(self, cfg, screen):
        """Constructor for the Runner"""
        self.cfg = cfg
        self.screen = screen
        self.grid = None

        # (center) position of the runner
        self.x = None
        self.y = None
        self.vel = 0                    # velocity [grid step/ms]
        self.move_direction = None      # direction of the movement (0=up, 1=right, 2=down, 3=left)
        self.next_direction = None      # commanded next direction (0=up, 1=right, 2=down, 3=left)
        self.dt_ms_rem = 0              # if a time step has to be split into two parts, then that's the remaining part [ms]

        self.node_visited_x = None      # x-coordinate of the node visited right now
        self.node_visited_y = None      # y-coordinate of the node visited right now

    def set_position(self, x, y):
        """Initializes the position of the player"""
        self.x = x
        self.y = y

    def set_grid(self, grid):
        """Stores a reference to the grid in this runner (such that he knows where to run!)"""
        self.grid = grid

    def can_move_up(self):
        """Inspects the grid and decides whether the runner can move up from a node"""
        # rounding to integer is actually not really needed, but for safety reasons included
        ix_v, ix_h = grid_index_up(self.x, self.y)
        if 0 <= ix_v < len(self.grid.gridlines) and \
                0 <= ix_h < len(self.grid.gridlines[ix_v]) and \
                self.grid.gridlines[ix_v][ix_h]:
            return True
        else:
            return False

    def can_move_right(self):
        """Inspects the grid and decides whether the runner can move right from a node"""
        ix_v, ix_h = grid_index_right(self.x, self.y)
        if 0 <= ix_v < len(self.grid.gridlines) and \
                0 <= ix_h < len(self.grid.gridlines[ix_v]) and \
                self.grid.gridlines[ix_v][ix_h]:
            return True
        else:
            return False

    def can_move_down(self):
        """Inspects the grid and decides whether the runner can move down from a node"""
        ix_v, ix_h = grid_index_down(self.x, self.y)
        if 0 <= ix_v < len(self.grid.gridlines) and \
                0 <= ix_h < len(self.grid.gridlines[ix_v]) and \
                self.grid.gridlines[ix_v][ix_h]:
            return True
        else:
            return False

    def can_move_left(self):
        """Inspects the grid and decides whether the runner can move left from a node"""
        ix_v, ix_h = grid_index_left(self.x, self.y)
        if 0 <= ix_v < len(self.grid.gridlines) and \
                0 <= ix_h < len(self.grid.gridlines[ix_v]) and \
                self.grid.gridlines[ix_v][ix_h]:
            return True
        else:
            return False

    def can_move_on(self):
        """Returns True if the runner can move on in the same direction as previously"""
        is_at_node = (self.x == int(self.x)) and (self.y == int(self.y))
        can_continue = False
        if is_at_node:
            if (self.move_direction == Direction.up and self.can_move_up()) or \
                    (self.move_direction == Direction.right and self.can_move_right()) or \
                    (self.move_direction == Direction.down and self.can_move_down()) or \
                    (self.move_direction == Direction.left and self.can_move_left()):
                can_continue = True
        else:
            # he's in the middle of a grid-element, therefore, of course he can move on
            can_continue = True
        return can_continue

    def move(self, dt_ms):
        """Move for dt_ms milliseconds"""
        dt_ms = dt_ms + self.dt_ms_rem  # don't forget about the remaining step of the last movement!

        x_next = self.x
        y_next = self.y

        # we cannot move freely because the grid constrains the movements. Therefore we only update the
        # position until a node is crossed
        cross_node = False

        # when starting at a node we have to be careful that immediately the rounded coordiantes will differ, but
        # in this case that's ok!
        start_at_node = (self.x == int(self.x)) and (self.y == int(self.y))

        if self.vel > 0:
            # moving up
            if self.move_direction == Direction.up:
                y_next = self.y - self.vel * dt_ms
                # check if moving across a grid node...
                if not start_at_node and int(y_next) != int(self.y):
                    self.dt_ms_rem = (int(self.y) - y_next) / self.vel
                    y_next = int(self.y)
                    cross_node = True
                elif not start_at_node and y_next < 0:
                    self.dt_ms_rem = -y_next / self.vel
                    y_next = 0
                    cross_node = True

            # moving right
            elif self.move_direction == Direction.right:
                x_next = self.x + self.vel * dt_ms
                # check if moving across a grid node...
                if not start_at_node and int(x_next) != int(self.x):
                    self.dt_ms_rem = (x_next - int(x_next)) / self.vel
                    x_next = int(x_next)
                    cross_node = True

            # moving down
            elif self.move_direction == Direction.down:
                y_next = self.y + self.vel * dt_ms
                # check if moving across a grid node...
                if not start_at_node and int(y_next) != int(self.y):
                    self.dt_ms_rem = (y_next - int(y_next)) / self.vel
                    y_next = int(y_next)
                    cross_node = True

            # moving left
            elif self.move_direction == Direction.left:
                x_next = self.x - self.vel * dt_ms
                # check if moving across a grid node...
                if not start_at_node and int(x_next) != int(self.x):
                    self.dt_ms_rem = (int(self.x) - x_next) / self.vel
                    x_next = int(self.x)
                    cross_node = True
                elif not start_at_node and x_next < 0:
                    self.dt_ms_rem = -x_next / self.vel
                    x_next = 0
                    cross_node = True

        self.x = x_next
        self.y = y_next

        # remember the node (if we crossed one!)
        if cross_node:
            self.node_visited_x = self.x
            self.node_visited_y = self.y

        return cross_node
