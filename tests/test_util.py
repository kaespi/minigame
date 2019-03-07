
import unittest

import src.util as util
from src.enumtypes import Direction


class TestUtil(unittest.TestCase):
    """Unittest class for general utility functions"""

    def test_reverse_direction(self):
        """Tests the function get_reverse_direction()"""
        self.assertEqual(Direction.down, util.get_reverse_direction(Direction.up))
        self.assertEqual(Direction.left, util.get_reverse_direction(Direction.right))
        self.assertEqual(Direction.up, util.get_reverse_direction(Direction.down))
        self.assertEqual(Direction.right, util.get_reverse_direction(Direction.left))
        self.assertEqual(None, util.get_reverse_direction(None))


unittest.main()
