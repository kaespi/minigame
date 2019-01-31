from gridline import Gridline
from gridutil import grid_index_up, grid_index_right, grid_index_down, grid_index_left


class Grid():
    """The class managing the whole grid to be played on"""

    def __init__(self, cfg, screen):
        """Constructor for the grid"""
        self.gridnodes = []
        self.gridlines = []
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
        """Draws the grid lines"""
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
            if 0 <= ix_up_v < len(self.gridlines) and \
                    0 <= ix_up_h < len(self.gridlines[ix_up_v]) and \
                    self.gridlines[ix_up_v][ix_up_h] is not None:
                num_connecting_gridlines += 1

            # check if a grid element connects towards right
            ix_right_v, ix_right_h = grid_index_right(node[0], node[1])
            if 0 <= ix_right_v < len(self.gridlines) and \
                    0 <= ix_right_h < len(self.gridlines[ix_right_v]) and \
                    self.gridlines[ix_right_v][ix_right_h] is not None:
                num_connecting_gridlines += 1

            # check if a grid element connects towards down
            ix_down_v, ix_down_h = grid_index_down(node[0], node[1])
            if 0 <= ix_down_v < len(self.gridlines) and \
                    0 <= ix_down_h < len(self.gridlines[ix_down_v]) and \
                    self.gridlines[ix_down_v][ix_down_h] is not None:
                num_connecting_gridlines += 1

            # check if a grid element connects towards left
            ix_left_v, ix_left_h = grid_index_left(node[0], node[1])
            if 0 <= ix_left_v < len(self.gridlines) and \
                    0 <= ix_left_h < len(self.gridlines[ix_left_v]) and \
                    self.gridlines[ix_left_v][ix_left_h] is not None:
                num_connecting_gridlines += 1

            if num_connecting_gridlines < 2:
                grid_ok = False

        return grid_ok
