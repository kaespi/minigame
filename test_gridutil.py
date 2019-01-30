
import unittest

from gridutil import *


class TestGridutil(unittest.TestCase):
    """Unittest class for grid utility functions"""

    def test_index_up(self):
        """Tests the function return the indices of the grid element towards up of a node"""
        # starting from (0,1)
        ix_v, ix_h = grid_index_up(0, 1)
        self.assertEqual(ix_v, 1)
        self.assertEqual(ix_h, 0)

        # starting from (1,1)
        ix_v, ix_h = grid_index_up(1, 1)
        self.assertEqual(ix_v, 1)
        self.assertEqual(ix_h, 1)

        # starting from (1,2)
        ix_v, ix_h = grid_index_up(1, 2)
        self.assertEqual(ix_v, 3)
        self.assertEqual(ix_h, 1)

        # starting from (5,0)
        ix_v, ix_h = grid_index_up(5, 0)
        self.assertEqual(ix_v, -1)
        self.assertEqual(ix_h, 5)

    def test_index_right(self):
        """Tests the function return the indices of the grid element towards right of a node"""
        # starting from (0,0)
        ix_v, ix_h = grid_index_right(0, 0)
        self.assertEqual(ix_v, 0)
        self.assertEqual(ix_h, 0)

        # starting from (1,1)
        ix_v, ix_h = grid_index_right(1, 1)
        self.assertEqual(ix_v, 2)
        self.assertEqual(ix_h, 1)

        # starting from (2,1)
        ix_v, ix_h = grid_index_right(2, 1)
        self.assertEqual(ix_v, 2)
        self.assertEqual(ix_h, 2)

    def test_index_down(self):
        """Tests the function return the indices of the grid element towards down of a node"""
        # starting from (0,0)
        ix_v, ix_h = grid_index_down(0, 0)
        self.assertEqual(ix_v, 1)
        self.assertEqual(ix_h, 0)

        # starting from (1,1)
        ix_v, ix_h = grid_index_down(1, 1)
        self.assertEqual(ix_v, 3)
        self.assertEqual(ix_h, 1)

        # starting from (2,2)
        ix_v, ix_h = grid_index_down(2, 2)
        self.assertEqual(ix_v, 5)
        self.assertEqual(ix_h, 2)

    def test_index_left(self):
        """Tests the function return the indices of the grid element towards left of a node"""
        # starting from (1,0)
        ix_v, ix_h = grid_index_left(1, 0)
        self.assertEqual(ix_v, 0)
        self.assertEqual(ix_h, 0)

        # starting from (1,1)
        ix_v, ix_h = grid_index_left(1, 1)
        self.assertEqual(ix_v, 2)
        self.assertEqual(ix_h, 0)

        # starting from (3,2)
        ix_v, ix_h = grid_index_left(3, 2)
        self.assertEqual(ix_v, 4)
        self.assertEqual(ix_h, 2)

        # starting from (0,10)
        ix_v, ix_h = grid_index_left(0, 10)
        self.assertEqual(ix_v, 20)
        self.assertEqual(ix_h, -1)

    def test_index(self):
        """Tests the function return the indices of the grid element on which a player/bug is"""
        # on horizontal grid element between (0,0) -> (1,0)
        ix_v, ix_h = grid_index(0.3, 0)
        self.assertEqual(ix_v, 0)
        self.assertEqual(ix_h, 0)

        # on vertical grid element between (1,1) -> (1,2)
        ix_v, ix_h = grid_index(1, 1.9)
        self.assertEqual(ix_v, 3)
        self.assertEqual(ix_h, 1)

        # on horizontal grid element between (3,2) -> (4,2)
        ix_v, ix_h = grid_index(3.01, 2)
        self.assertEqual(ix_v, 4)
        self.assertEqual(ix_h, 3)

        # on vertical grid element between (3,2) -> (3,3)
        ix_v, ix_h = grid_index(3, 2.999)
        self.assertEqual(ix_v, 5)
        self.assertEqual(ix_h, 3)


unittest.main()
