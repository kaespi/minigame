
import unittest
import context

from config import Gameconfig
from gridline import Gridline
import gameaction


class TestGameaction(unittest.TestCase):
    """Unittest class for testing the game actions"""

    def setUp(self):
        """Initializes the variables etc."""
        self.cfg = Gameconfig()

    def test_canyouseeme(self):
        """Tests can_you_see_me()"""

        # horizontal visibility

        # constructs a grid as follows: o-o-o o-o (with x a node and - a grid line)
        #                               |
        #                               o
        #                               |
        #                               o
        #
        #                               o
        #                               |
        #                               o
        gridlines = [[Gridline(self.cfg, None, [0, 0], [1, 0]),
                      Gridline(self.cfg, None, [1, 0], [2, 0]),
                      None,     # horizontal gap between (2,0) and (3,0)
                      Gridline(self.cfg, None, [3, 0], [4, 0])],
                     [Gridline(self.cfg, None, [0, 0], [0, 1])],
                     [None],    # horizontal gridlines with y=1
                     [Gridline(self.cfg, None, [0, 1], [0, 2])],
                     [None],    # horizontal gridlines with y=2
                     [None],    # vertical gap between (0,2) and (0,3)
                     [None],    # horizontal gridlines with y=3
                     [Gridline(self.cfg, None, [0, 3], [0, 4])]]

        # checks that at the same node the two points are visible
        self.assertTrue(gameaction.can_you_see_me([0, 0], [0, 0], gridlines))
        self.assertTrue(gameaction.can_you_see_me([1, 0], [1, 0], gridlines))
        self.assertTrue(gameaction.can_you_see_me([0, 1], [0, 1], gridlines))

        # checks the first horizontal part of the grid, x-coordinates [0..2] (first two gridlines
        # where all points are visible by each other)
        self.assertTrue(gameaction.can_you_see_me([0.5, 0], [0.7, 0], gridlines))
        self.assertTrue(gameaction.can_you_see_me([0.5, 0], [1.5, 0], gridlines))
        self.assertTrue(gameaction.can_you_see_me([1.5, 0], [0.5, 0], gridlines))
        self.assertTrue(gameaction.can_you_see_me([1.5, 0], [1.7, 0], gridlines))
        self.assertTrue(gameaction.can_you_see_me([1.0, 0], [1.0, 0], gridlines))
        self.assertTrue(gameaction.can_you_see_me([0.0, 0], [1.0, 0], gridlines))

        # checks the second horizontal part of the grid, x-coordinates [3..4] (where all points are
        # visible by each other)
        self.assertTrue(gameaction.can_you_see_me([3.0, 0], [4.0, 0], gridlines))
        self.assertTrue(gameaction.can_you_see_me([3.2, 0], [4.0, 0], gridlines))
        self.assertTrue(gameaction.can_you_see_me([3.0, 0], [3.2, 0], gridlines))
        self.assertTrue(gameaction.can_you_see_me([4.0, 0], [4.0, 0], gridlines))

        # checks that points in the horizontal interval [0..2] and [3..4] are not visible by each other
        # because there's a gap (i.e. no gridline) between 2 and 3
        self.assertFalse(gameaction.can_you_see_me([2.0, 0], [3.0, 0], gridlines))
        self.assertFalse(gameaction.can_you_see_me([1.9, 0], [3.0, 0], gridlines))
        self.assertFalse(gameaction.can_you_see_me([2.0, 0], [3.1, 0], gridlines))
        self.assertFalse(gameaction.can_you_see_me([1.9, 0], [3.1, 0], gridlines))
        self.assertFalse(gameaction.can_you_see_me([2.0, 0], [4.0, 0], gridlines))
        self.assertFalse(gameaction.can_you_see_me([1.9, 0], [4.0, 0], gridlines))
        self.assertFalse(gameaction.can_you_see_me([1.0, 0], [4.0, 0], gridlines))
        self.assertFalse(gameaction.can_you_see_me([1.9, 0], [4.0, 0], gridlines))
        self.assertFalse(gameaction.can_you_see_me([0.0, 0], [4.0, 0], gridlines))
        self.assertFalse(gameaction.can_you_see_me([0.9, 0], [4.0, 0], gridlines))
        self.assertFalse(gameaction.can_you_see_me([0.0, 0], [3.0, 0], gridlines))
        self.assertFalse(gameaction.can_you_see_me([0.9, 0], [3.1, 0], gridlines))

        # vertical visibility

        # checks the first vertical part of the grid, y-coordinates [0..2] (first two gridlines
        # where all points are visible by each other)
        self.assertTrue(gameaction.can_you_see_me([0, 0.5], [0, 0.7], gridlines))
        self.assertTrue(gameaction.can_you_see_me([0, 0.5], [0, 1.5], gridlines))
        self.assertTrue(gameaction.can_you_see_me([0, 1.5], [0, 0.5], gridlines))
        self.assertTrue(gameaction.can_you_see_me([0, 1.5], [0, 1.7], gridlines))
        self.assertTrue(gameaction.can_you_see_me([0, 1.0], [0, 1.0], gridlines))
        self.assertTrue(gameaction.can_you_see_me([0, 0.0], [0, 1.0], gridlines))

        # checks the second part of the grid, x-coordinates [3..4] (where all points are
        # visible by each other)
        self.assertTrue(gameaction.can_you_see_me([0, 3.0], [0, 4.0], gridlines))
        self.assertTrue(gameaction.can_you_see_me([0, 3.2], [0, 4.0], gridlines))
        self.assertTrue(gameaction.can_you_see_me([0, 3.0], [0, 3.2], gridlines))
        self.assertTrue(gameaction.can_you_see_me([0, 4.0], [0, 4.0], gridlines))

        # checks that points in the interval [0..2] and [3..4] are not visible by each other
        # because there's a gap (i.e. no gridline) between 2 and 3
        self.assertFalse(gameaction.can_you_see_me([0, 2.0], [0, 3.0], gridlines))
        self.assertFalse(gameaction.can_you_see_me([0, 1.9], [0, 3.0], gridlines))
        self.assertFalse(gameaction.can_you_see_me([0, 2.0], [0, 3.1], gridlines))
        self.assertFalse(gameaction.can_you_see_me([0, 1.9], [0, 3.1], gridlines))
        self.assertFalse(gameaction.can_you_see_me([0, 2.0], [0, 4.0], gridlines))
        self.assertFalse(gameaction.can_you_see_me([0, 1.9], [0, 4.0], gridlines))
        self.assertFalse(gameaction.can_you_see_me([0, 1.0], [0, 4.0], gridlines))
        self.assertFalse(gameaction.can_you_see_me([0, 1.9], [0, 4.0], gridlines))
        self.assertFalse(gameaction.can_you_see_me([0, 0.0], [0, 4.0], gridlines))
        self.assertFalse(gameaction.can_you_see_me([0, 0.9], [0, 4.0], gridlines))
        self.assertFalse(gameaction.can_you_see_me([0, 0.0], [0, 3.0], gridlines))
        self.assertFalse(gameaction.can_you_see_me([0, 0.9], [0, 3.1], gridlines))


unittest.main()
