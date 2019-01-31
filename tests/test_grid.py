
import unittest
import context

from config import Gameconfig
from gridline import Gridline
from grid import Grid


class TestGridline(unittest.TestCase):
    """Unittest class for the grid element class (Gridline)"""

    def setUp(self):
        """Initializes the variables etc."""
        self.cfg = Gameconfig()

    def test_update_lo2hi(self):
        """Tests the multiple updating for the grid element (left/upper side)"""
        ge = Gridline(self.cfg, None, (0, 0), (1, 0))

        # initially both grid elements are not yet completed
        self.assertFalse(ge.is_complete())
        self.assertEqual(ge.ratioDone1, 0)
        self.assertEqual(ge.ratioDone2, 0)

        # update with out of bounds positions, should still not
        # be completed and ratioDone1/2 should still be zero
        ge.update(-.5, -.25)
        self.assertEqual(ge.ratioDone1, 0)
        self.assertEqual(ge.ratioDone2, 0)
        self.assertFalse(ge.is_complete())

        # update from "outside" to "inside" positions
        ge.update(-.25, .25)
        self.assertTrue(.24 < ge.ratioDone1 < .26)
        self.assertEqual(ge.ratioDone2, 0)
        self.assertFalse(ge.is_complete())

        # going back again
        ge.update(.25, .15)
        self.assertTrue(.24 < ge.ratioDone1 < .26)
        self.assertEqual(ge.ratioDone2, 0)
        self.assertFalse(ge.is_complete())

        # going a big step forth
        ge.update(.15, .35)
        self.assertTrue(.34 < ge.ratioDone1 < .36)
        self.assertEqual(ge.ratioDone2, 0)
        self.assertFalse(ge.is_complete())

        # leaving the grid element again (towards lower end)
        ge.update(.15, -.5)
        self.assertTrue(.34 < ge.ratioDone1 < .36)
        self.assertEqual(ge.ratioDone2, 0)
        self.assertFalse(ge.is_complete())

        # entering the grid element again (towards lower end)
        ge.update(-.5, .8)
        self.assertTrue(.79 < ge.ratioDone1 < .81)
        self.assertEqual(ge.ratioDone2, 0)
        self.assertFalse(ge.is_complete())

        # leaving on the other side
        ge.update(.8, 1.0)
        self.assertTrue(.99 < ge.ratioDone1 < 1.01)
        self.assertEqual(ge.ratioDone2, 0)
        self.assertTrue(ge.is_complete())

    def test_update_hi2lo(self):
        """Tests the multiple updating for the grid element (right/lower side)"""
        ge = Gridline(self.cfg, None, (0, 0), (1, 0))

        # update with out of bounds positions, should still not
        # be completed and ratioDone1/2 should still be zero
        ge.update(1.5, 1.25)
        self.assertEqual(ge.ratioDone1, 0)
        self.assertEqual(ge.ratioDone2, 0)
        self.assertFalse(ge.is_complete())

        # update from "outside" to "inside" positions
        ge.update(1.25, .75)
        self.assertEqual(ge.ratioDone1, 0)
        self.assertTrue(.24 < ge.ratioDone2 < .26)
        self.assertFalse(ge.is_complete())

        # going back again
        ge.update(.75, .85)
        self.assertEqual(ge.ratioDone1, 0)
        self.assertTrue(.24 < ge.ratioDone2 < .26)
        self.assertFalse(ge.is_complete())

        # going a big step forth
        ge.update(.85, .65)
        self.assertEqual(ge.ratioDone1, 0)
        self.assertTrue(.34 < ge.ratioDone2 < .36)
        self.assertFalse(ge.is_complete())

        # leaving the grid element again (towards lower end)
        ge.update(.85, 1.5)
        self.assertEqual(ge.ratioDone1, 0)
        self.assertTrue(.34 < ge.ratioDone2 < .36)
        self.assertFalse(ge.is_complete())

        # entering the grid element again (towards lower end)
        ge.update(1.5, .2)
        self.assertEqual(ge.ratioDone1, 0)
        self.assertTrue(.79 < ge.ratioDone2 < .81)
        self.assertFalse(ge.is_complete())

        # leaving on the other side
        ge.update(.2, -.2)
        self.assertEqual(ge.ratioDone1, 0)
        self.assertTrue(.99 < ge.ratioDone2 < 1.01)
        self.assertTrue(ge.is_complete())

    def test_update_both_sides(self):
        """Tests the multiple updating for the grid element in both directions"""
        ge = Gridline(self.cfg, None, (0, 0), (1, 0))

        # update from "right to left"
        ge.update(1.25, .75)
        self.assertEqual(ge.ratioDone1, 0)
        self.assertTrue(.24 < ge.ratioDone2 < .26)
        self.assertFalse(ge.is_complete())

        # update from "left to right"
        ge.update(0.0, .25)
        self.assertTrue(.24 < ge.ratioDone1 < .26)
        self.assertTrue(.24 < ge.ratioDone2 < .26)
        self.assertFalse(ge.is_complete())

        # more update from "right to left"
        ge.update(.75, .5)
        self.assertTrue(.24 < ge.ratioDone1 < .26)
        self.assertTrue(.49 < ge.ratioDone2 < .51)
        self.assertFalse(ge.is_complete())

        # more update from "left to right"
        ge.update(.25, .5)
        self.assertTrue(.49 < ge.ratioDone1 < .51)
        self.assertTrue(.49 < ge.ratioDone2 < .51)
        self.assertTrue(ge.is_complete())

    def test_update_reenter_lo2hi(self):
        """Tests the multiple updating for the grid element (left/upper side)"""
        ge = Gridline(self.cfg, None, (0, 0), (1, 0))

        # initially both grid elements are not yet completed
        self.assertFalse(ge.is_complete())
        self.assertEqual(ge.ratioDone1, 0)
        self.assertEqual(ge.ratioDone2, 0)

        # update from the node towards right/down
        ge.update(0, 0.25)
        self.assertTrue(.24 < ge.ratioDone1 < .26)
        self.assertEqual(ge.ratioDone2, 0)
        self.assertFalse(ge.is_complete())

        # update again from the node but not as far
        ge.update(0, .15)
        self.assertTrue(.24 < ge.ratioDone1 < .26)
        self.assertEqual(ge.ratioDone2, 0)
        self.assertFalse(ge.is_complete())

        # update a bit more
        ge.update(0.15, .20)
        self.assertTrue(.24 < ge.ratioDone1 < .26)
        self.assertEqual(ge.ratioDone2, 0)
        self.assertFalse(ge.is_complete())

        # update a new piece
        ge.update(0.25, .30)
        self.assertTrue(.29 < ge.ratioDone1 < .31)
        self.assertEqual(ge.ratioDone2, 0)
        self.assertFalse(ge.is_complete())

    def test_update_hi2lo(self):
        """Tests the multiple updating for the grid element (right/lower side)"""
        ge = Gridline(self.cfg, None, (0, 0), (1, 0))

        # update from the node towards left/up
        ge.update(1.0, 0.75)
        self.assertEqual(ge.ratioDone1, 0)
        self.assertTrue(0.24 < ge.ratioDone2 < 0.26)
        self.assertFalse(ge.is_complete())

        # update again from the not bot nus as far
        ge.update(1.0, 0.85)
        self.assertEqual(ge.ratioDone1, 0)
        self.assertTrue(0.24 < ge.ratioDone2 < 0.26)
        self.assertFalse(ge.is_complete())

        # update a bit more
        ge.update(0.85, 0.8)
        self.assertEqual(ge.ratioDone1, 0)
        self.assertTrue(0.24 < ge.ratioDone2 < 0.26)
        self.assertFalse(ge.is_complete())

        # update a new piece
        ge.update(0.8, 0.7)
        self.assertEqual(ge.ratioDone1, 0)
        self.assertTrue(0.29 < ge.ratioDone2 < 0.31)
        self.assertFalse(ge.is_complete())

    def test_grid_x1x2_y1y2(self):
        """Tests that when the arguments x1/y1 and x2/y2 are always stored such that  x1 < x2 and y1 < y2, always"""
        g1 = Gridline(self.cfg, None, (0, 0), (1, 1))
        self.assertTrue(g1.x1 < g1.x2)
        self.assertTrue(g1.y1 < g1.y2)

        g2 = Gridline(self.cfg, None, (1, 1), (0, 0))
        self.assertTrue(g2.x1 < g2.x2)
        self.assertTrue(g2.y1 < g2.y2)


class TestGrid(unittest.TestCase):
    """Unittest class for the grid class (Grid)"""

    def setUp(self):
        """Initializes the variables etc."""
        self.cfg = Gameconfig()
        self.grid = Grid(self.cfg, None)

    def test_read_grid1(self):
        """Tests grid parsing from file test_grid1.txt (square)"""
        self.grid.read_grid("test_grid1.txt")

        # check if the players starting position were correctly parsed (should be 0,0 and 1,1)
        players = self.grid.get_players_start()
        self.assertTrue(len(players) == 2)
        self.assertTrue(((0, 0) in players))
        self.assertTrue(((1, 1) in players))

        # check if the bugs starting position were correctly parsed (should be 1,0 and 0,1)
        bugs = self.grid.get_bugs_start()
        self.assertTrue(len(bugs) == 2)
        self.assertTrue(((1, 0) in bugs))
        self.assertTrue(((0, 1) in bugs))

        # check if the gridlines were initialized correctly
        self.assertEqual(len(self.grid.gridlines), 3)
        self.assertEqual(len(self.grid.gridlines[0]), 1)
        self.assertTrue(self.grid.gridlines[0][0] is not None)
        self.assertEqual(len(self.grid.gridlines[1]), 2)
        self.assertTrue(self.grid.gridlines[1][0] is not None)
        self.assertTrue(self.grid.gridlines[1][1] is not None)
        self.assertEqual(len(self.grid.gridlines[2]), 1)
        self.assertTrue(self.grid.gridlines[2][0] is not None)

        self.assertTrue(self.grid.check_grid())

    def test_read_grid2(self):
        """Tests grid parsing from file test_grid2.txt (square with one open side)"""
        self.grid.read_grid("test_grid2.txt")

        self.assertFalse(self.grid.check_grid())


unittest.main()
