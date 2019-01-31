import pygame


class Square():
    """This class is a square patch between the grid lines"""

    def __init__(self, cfg, screen, p):
        """Constructor for a grid element"""
        self.screen = screen
        self.cfg = cfg

        self.completed = False  # true if this grid element is completed

        # initializes the rectangle object
        grid_left = cfg.grid_origin[0] + cfg.grid_height*p[0]
        grid_top = cfg.grid_origin[1] + cfg.grid_height*p[1]
        self.rect = pygame.Rect(grid_left, grid_top, cfg.grid_height, cfg.grid_height)

        # a list of gridlines around this square. If they are completed then this square is completed
        self.surrounding_gridlines = []

    def is_complete(self):
        """Checks if all surrounding gridlines are completed and therefore this square can be marked as completed"""
        if not self.completed:
            any_not_complete = False
            for gridline in self.surrounding_gridlines:
                if not gridline.completed:
                    any_not_complete = True
                    break

            self.completed = not any_not_complete

        return self.completed

    def draw(self):
        """Draws the scquare"""
        if self.completed:
            pygame.draw.rect(self.screen, self.cfg.square_color_complete, self.rect, 0)
        else:
            pygame.draw.rect(self.screen, self.cfg.square_color_fresh, self.rect, 0)
