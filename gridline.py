import pygame


class Gridline():
    """This class is an element of the grid (grid line)"""

    def __init__(self, cfg, screen, p1, p2):
        """Constructor for a grid element"""
        self.screen = screen

        self.completed = 0  # true if this grid element is completed
        self.ratioDone1 = 0.0  # how much of the grid element is completed (top->bottom, left->right)
        self.ratioDone2 = 0.0  # how much of the grid element is completed (bottom->top, right->left)

        # coordinates of the grid element end points (we always require x1<x2 and y1<y2)
        if p2[0] < p1[0]:
            self.x1 = p2[0]
            self.x2 = p1[0]
        else:
            self.x1 = p1[0]
            self.x2 = p2[0]

        if p2[1] < p1[1]:
            self.y1 = p2[1]
            self.y2 = p1[1]
        else:
            self.y1 = p1[1]
            self.y2 = p2[1]

        self.x1 = self.x1*cfg.grid_height + cfg.grid_origin[0]
        self.x2 = self.x2*cfg.grid_height + cfg.grid_origin[0]
        self.y1 = self.y1*cfg.grid_height + cfg.grid_origin[1]
        self.y2 = self.y2*cfg.grid_height + cfg.grid_origin[1]

        # style of the grid element
        self.w = cfg.grid_width
        self.color_fresh = cfg.grid_color_fresh
        self.color_done = cfg.grid_color_done

    def is_complete(self):
        """Returns true if the element is completed"""
        if self.completed:
            return 1
        elif self.ratioDone1 + self.ratioDone2 >= 1:
            self.completed = 1
            return 1
        else:
            return 0

    def update(self, p1, p2):
        """Updates the grid element from p1 to p2"""
        # the update is only relevant if one of the two coordinates is in the interval [0,1]
        # and if the element isn't complete yet
        if ((0 <= p1 <= 1) or (0 <= p2 <= 1)) and not self.is_complete():
            if (p2 > p1) and p1 < (1.0 - self.ratioDone2):
                # moving top->bottom/left->right
                if p2 <= 1:
                    self.ratioDone1 = max(self.ratioDone1, p2)
                else:
                    self.ratioDone2 = 1.0
            elif (p1 > p2) and p1 > self.ratioDone1:
                # moving bottom->top/right->left
                if p2 >= 0:
                    self.ratioDone2 = max(self.ratioDone2, (1.0 - p2))
                else:
                    self.ratioDone2 = 1.0

    def draw(self):
        """Draws the grid element"""
        if self.is_complete():
            #self.draw_line(self.color_complete, self.x1, self.y1, self.x2, self.y2)
            self.draw_line((0,0,200), self.x1, self.y1, self.x2, self.y2)
        else:
            x1 = self.x1
            y1 = self.y1
            x2 = self.x2
            y2 = self.y2

            if self.ratioDone1 > 0:
                # the next line starts where this ended
                x1 = self.x1 + self.ratioDone1 * (self.x2 - self.x1)
                y1 = self.y1 + self.ratioDone1 * (self.y2 - self.y1)
                self.draw_line(self.color_done, self.x1, self.y1, x1, y1)

            if self.ratioDone2 > 0:
                # the next line ends where this started
                x2 = self.x2 - self.ratioDone2 * (self.x2 - self.x1)
                y2 = self.y2 - self.ratioDone2 * (self.y2 - self.y1)
                self.draw_line(self.color_done, x2, y2, self.x2, self.y2)

            self.draw_line(self.color_fresh, x1, y1, x2, y2)

    def draw_line(self, color, x1, y1, x2, y2):
        """Draws a line"""
        pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), self.w)
