from src.gridline import Gridline
from src.gridutil import grid_index_up, grid_index_right, grid_index_down, grid_index_left
from src.enumtypes import Direction
from src.square import Square


class Grid():
    """The class managing the whole grid to be played on"""

    def __init__(self, cfg, screen):
        """Constructor for the grid"""
        self.gridnodes = []
        self.gridlines = []
        self.squares = []
        self.num_lines_horiz = 0
        self.num_lines_vert = 0

        # starting points for players and bugs
        self.players_start = []
        self.bugs_start = []

        self.cfg = cfg
        self.screen = screen

    def read_grid(self, gridfile):
        """Reads the grid from an ASCI textfile"""
        self.players_start = []
        self.bugs_start = []
        self.gridlines = []

        with open(gridfile, "r") as fh:
            lines = fh.readlines()

        for nl in range(0, len(lines)):
            line_nl = lines[nl].rstrip()
            g = []
            if nl % 2 == 0:
                # horizontal grid lines
                for nc in range(0, len(line_nl)):
                    if nc % 2 == 0:
                        if line_nl[nc] == "P":
                            self.players_start.append((nc/2, nl/2))
                        elif line_nl[nc] == "B":
                            self.bugs_start.append((nc/2, nl/2))
                    else:
                        if line_nl[nc] == "-":
                            g.append(Gridline(self.cfg, self.screen, ((nc-1)/2, nl/2), ((nc+1)/2, nl/2)))
                        else:
                            g.append(None)
            else:
                # vertical grid lines
                for nc in range(0, len(line_nl)):
                    if nc % 2 == 0:
                        if line_nl[nc] == "|":
                            g.append(Gridline(self.cfg, self.screen, (nc/2, (nl-1)/2), (nc/2, (nl+1)/2)))
                        else:
                            g.append(None)

            # adds the parsed grid lines
            self.gridlines.append(g)

    def get_players_start(self):
        """Returns the starting points for the players"""
        return self.players_start[:]

    def get_bugs_start(self):
        """Returns the starting points for the bugs"""
        return self.bugs_start[:]

    def draw_grid(self):
        """Draws the grid (squares+lines)"""
        # draw the squares first
        for square in self.squares:
            square.draw()

        # draw the grid lines second
        for nv in range(0, len(self.gridlines)):
            for nh in range(0, len(self.gridlines[nv])):
                if self.gridlines[nv][nh]:
                    self.gridlines[nv][nh].draw()

    def get_nodes(self):
        """Parses the grid and returns the coordinates of all nodes in the grid"""
        nodes = []
        for ix_v in range(0, len(self.gridlines)):
            for ix_h in range(0, len(self.gridlines[ix_v])):
                # only have to check defined grid elements
                if self.gridlines[ix_v][ix_h] is None:
                    continue

                if ix_v % 2 == 0:
                    # horizontal grid line
                    node1 = (ix_h, ix_v/2)
                    node2 = (ix_h+1, ix_v/2)
                else:
                    # vertical grid line
                    node1 = (ix_h, (ix_v-1)/2)
                    node2 = (ix_h, (ix_v+1)/2)

                if node1 not in nodes:
                    nodes.append(node1)
                if node2 not in nodes:
                    nodes.append(node2)

        return nodes[:]

    def get_grid_size(self):
        """Returns the width and height of the grid in number of grid squares"""
        width = 0
        height = 0
        for ix_v in range(0, len(self.gridlines)):
            for ix_h in range(0, len(self.gridlines[ix_v])):
                if self.gridlines[ix_v][ix_h] is None:
                    continue

                if ix_v % 2 == 0 and ix_h+1 > width:
                    # horizontal grid line
                    width = ix_h + 1
                elif ix_v % 2 == 1 and (ix_v - 1)/2 + 1 > height:
                    # vertical grid line
                    height = (ix_v - 1)/2 + 1
        return [width, height]

    def is_gridline(self, ix_v, ix_h):
        """Checks if the indices ix_v and ix_h index a defined gridline"""
        if 0 <= ix_v < len(self.gridlines) and \
                0 <= ix_h < len(self.gridlines[ix_v]) and \
                self.gridlines[ix_v][ix_h] is not None:
            return True
        else:
            return False

    def check_grid(self):
        """Checks the parsed grid for consistency"""
        grid_ok = True

        # check if each node connects to two grid elements
        nodes = self.get_nodes()
        for node in nodes:
            # get for the node the grid lines connecting to it and count these
            # grid elements. If the grid is ok, then all nodes connect to at least
            # two grid lines
            num_connecting_gridlines = 0

            # check if a grid element connects towards up
            ix_up_v, ix_up_h = grid_index_up(node[0], node[1])
            if self.is_gridline(ix_up_v, ix_up_h):
                num_connecting_gridlines += 1

            # check if a grid element connects towards right
            ix_right_v, ix_right_h = grid_index_right(node[0], node[1])
            if self.is_gridline(ix_right_v, ix_right_h):
                num_connecting_gridlines += 1

            # check if a grid element connects towards down
            ix_down_v, ix_down_h = grid_index_down(node[0], node[1])
            if self.is_gridline(ix_down_v, ix_down_h):
                num_connecting_gridlines += 1

            # check if a grid element connects towards left
            ix_left_v, ix_left_h = grid_index_left(node[0], node[1])
            if self.is_gridline(ix_left_v, ix_left_h):
                num_connecting_gridlines += 1

            if num_connecting_gridlines < 2:
                grid_ok = False

        return grid_ok

    def init_squares(self):
        """Initializes the squares in the grid"""
        # the whole square initialization is a bit complicated because there might be actually few squares
        # being surrounded by more than 4 grid lines!
        nv = len(self.gridlines)
        square_coordinates = []     # buffer the squares' coordinates to avoid duplicates

        for y in range(0, int(nv/2)):
            # start in the "top left corner" (=when there's a grid line on the left and above)
            for x in range(0, len(self.gridlines[y])):
                # no need to continue if this square was already added...
                p = [x, y]
                if p in square_coordinates:
                    continue

                ix_down_v, ix_down_h = grid_index_down(x, y)
                ix_right_v, ix_right_h = grid_index_right(x, y)

                if self.is_gridline(ix_down_v, ix_down_h) and \
                        self.is_gridline(ix_right_v, ix_right_h):
                    # we found a "top left corner". Now we have to continue this patch until it is complete
                    # (be careful, it can extend towards down and right etc.!)
                    current_squares = [p]
                    self.add_neighbour_squares(p, current_squares)

                    # now we have the squares, but we have to check if they actually are all surroundded by
                    # gridlines
                    gridlines_around = []
                    if self.get_surrounding_gridlines(p, gridlines_around):
                        self.add_squares(current_squares, gridlines_around)

                    for s in current_squares:
                        square_coordinates.append(s)

    def add_neighbour_squares(self, p, square_coord):
        """For one square adds the neighbouring patches (up, right, down, left) if not separated by ag gridline"""
        # This function is targeted to be called recursively
        # remember: the coordinates of the square (p) are given as the coordinates of the square's top left node

        # check if there's a grid line separating this square from the one above
        if p[1] > 0:
            ix_v, ix_h = grid_index_right(p[0], p[1])
            if 2 <= ix_v < len(self.gridlines) and \
                    0 <= ix_h < len(self.gridlines[ix_v]) and \
                    self.gridlines[ix_v][ix_h] is None:
                p_next = [p[0], p[1]-1]
                if p_next not in square_coord:
                    square_coord.append(p_next)
                    self.add_neighbour_squares(p_next, square_coord)

        # check if there's a grid line separating this square from the one to the right
        ix_v, ix_h = grid_index_down(p[0]+1, p[1])
        if 0 <= ix_v < len(self.gridlines) and \
                1 <= ix_h < len(self.gridlines[ix_v]) and \
                self.gridlines[ix_v][ix_h] is None:
            p_next = [p[0]+1, p[1]]
            if p_next not in square_coord:
                square_coord.append(p_next)
                self.add_neighbour_squares(p_next, square_coord)

        # check if there's a grid line separating this square from the one below
        ix_v, ix_h = grid_index_right(p[0], p[1]+1)
        if 0 <= ix_v < len(self.gridlines)-2 and \
                0 <= ix_h < len(self.gridlines[ix_v]) and \
                self.gridlines[ix_v][ix_h] is None:
            p_next = [p[0], p[1]+1]
            if p_next not in square_coord:
                square_coord.append(p_next)
                self.add_neighbour_squares(p_next, square_coord)

        # check if there's a grid line separating this square from the one to the left
        if p[0] > 0:
            ix_v, ix_h = grid_index_down(p[0], p[1])
            if 0 <= ix_v < len(self.gridlines) and \
                    1 <= ix_h < len(self.gridlines[ix_v]) and \
                    self.gridlines[ix_v][ix_h] is None:
                p_next = [p[0]-1, p[1]]
                if p_next not in square_coord:
                    square_coord.append(p_next)
                    self.add_neighbour_squares(p_next, square_coord)

    def get_surrounding_gridlines(self, p_start, gridlines_around):
        """Finds the gridlines surrounding the squares given with the upper left coordinates"""

        # basic idea goes as follows:
        # we know that we start at a top left corner of a square, i.e. at a node p_start where there is a gridline
        # towards right and towards down. Now we start towards right and try to make one closed loop along gridlines
        # such that we again end up at the node where we started. After moving from one to the next node we always
        # try to continue with the next gridline counter clockwise. In this way we guarantee that we always follow
        # the smallest path around the squares.
        # We have a problem whenever the top left corner of the square we start with actually lies outside a closed
        # loop. In this case we can still make a closed loop but not enclosing the square we actually want to. In
        # this case we have to return False. We try to detect a valid circle around the square by virtually counting
        # how many times the middle of the square is crossed in either x- or y-coordinate in the right direction.

        p = p_start[:]
        p_prev = p[:]

        # how many times the starting x coordinate is reached with larger y coordinate than the starting node.
        # Reaching "from right" counts as +1, reaching "from left" as -1.
        num_x_crossed = 0
        # how many times the starting y coordinate is reached with larger x coordinate than the starting node.
        # Reaching "from bottom" counts as +1, reaching "from top" as -1.
        num_y_crossed = 0

        # start from the top grid line
        ix_v, ix_h = grid_index_right(p[0], p[1])
        gridlines_around.append(self.gridlines[ix_v][ix_h])
        p[0] += 1

        while p != p_start:
            dx = 0
            dy = 0

            continue_direction = self.get_next_gridline_ccw(p, p_prev)
            if continue_direction is None:
                break
            elif continue_direction == Direction.up:
                ix_v, ix_h = grid_index_up(p[0], p[1])
                gridlines_around.append(self.gridlines[ix_v][ix_h])
                dy = -1
            elif continue_direction == Direction.right:
                ix_v, ix_h = grid_index_right(p[0], p[1])
                gridlines_around.append(self.gridlines[ix_v][ix_h])
                dx = 1
            elif continue_direction == Direction.down:
                ix_v, ix_h = grid_index_down(p[0], p[1])
                gridlines_around.append(self.gridlines[ix_v][ix_h])
                dy = 1
            elif continue_direction == Direction.left:
                ix_v, ix_h = grid_index_left(p[0], p[1])
                gridlines_around.append(self.gridlines[ix_v][ix_h])
                dx = -1

            p_prev = p[:]
            p[0] += dx
            p[1] += dy

            if p[0] == p_start[0] and p[1] >= p_start[1] and continue_direction == Direction.left:
                num_x_crossed += 1
            elif p[0] == p_start[0] and p[1] >= p_start[1] and continue_direction == Direction.right:
                num_x_crossed -= 1
            elif p[1] == p_start[1] and p[0] >= p_start[0] and continue_direction == Direction.up:
                num_y_crossed += 1
            elif p[1] == p_start[1] and p[0] >= p_start[0] and continue_direction == Direction.down:
                num_y_crossed -= 1

        if num_x_crossed == 1 and num_y_crossed == 1:
            return True
        else:
            return False

    def get_next_gridline_ccw(self, p, p_prev):
        """Checks in which direction follows the next gridline after reaching node p from node p_prev"""
        ixd_v, ixd_h = grid_index_down(p[0], p[1])
        ixr_v, ixr_h = grid_index_right(p[0], p[1])
        ixu_v, ixu_h = grid_index_up(p[0], p[1])
        ixl_v, ixl_h = grid_index_left(p[0], p[1])

        if p[0] > p_prev[0]:
            # arrived from left to right:
            if self.is_gridline(ixd_v, ixd_h):
                return Direction.down
            elif self.is_gridline(ixr_v, ixr_h):
                return Direction.right
            elif self.is_gridline(ixu_v, ixu_h):
                return Direction.up

        elif p[0] < p_prev[0]:
            # arrived from right to left:
            if self.is_gridline(ixu_v, ixu_h):
                return Direction.up
            elif self.is_gridline(ixl_v, ixl_h):
                return Direction.left
            elif self.is_gridline(ixd_v, ixd_h):
                return Direction.down

        elif p[1] > p_prev[1]:
            # arrived from top to bottom:
            if self.is_gridline(ixl_v, ixl_h):
                return Direction.left
            elif self.is_gridline(ixd_v, ixd_h):
                return Direction.down
            elif self.is_gridline(ixr_v, ixr_h):
                return Direction.right

        elif p[1] < p_prev[1]:
            # arrived from bottom to top:
            if self.is_gridline(ixr_v, ixr_h):
                return Direction.right
            elif self.is_gridline(ixu_v, ixu_h):
                return Direction.up
            elif self.is_gridline(ixl_v, ixl_h):
                return Direction.left

        return None

    def add_squares(self, squares_coord, gridlines_around):
        """Creates a list of squares which all are surrounded by the same gridlines"""
        for sq in squares_coord:
            square = Square(self.cfg, self.screen, sq)
            square.set_surrounding_gridlines(gridlines_around)
            self.squares.append(square)
