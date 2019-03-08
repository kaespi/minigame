
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

    def test_filename_validation(self):
        """Tests the scanning for level files in function is_valid_level_file()"""
        # 1. no number of players argument
        # invalid level filenames
        self.assertFalse(util.is_valid_level_file(''))
        self.assertFalse(util.is_valid_level_file('.txt'))
        self.assertFalse(util.is_valid_level_file('abc.txt'))
        self.assertFalse(util.is_valid_level_file('abc_def.txt'))
        self.assertFalse(util.is_valid_level_file('abc_def_ghi.txt'))
        self.assertFalse(util.is_valid_level_file('abc_def_ghi_jkl.txt'))
        self.assertFalse(util.is_valid_level_file('abc_def_001.txt'))
        self.assertFalse(util.is_valid_level_file('abc_dep_001.txt'))
        self.assertFalse(util.is_valid_level_file('abc_1p_1.txt'))
        self.assertFalse(util.is_valid_level_file('abc_9p_9.txt'))
        self.assertFalse(util.is_valid_level_file('abc_01p_001.txt'))
        self.assertFalse(util.is_valid_level_file('abc_99p_999.txt'))
        self.assertFalse(util.is_valid_level_file('abc_def_01p_001.txt'))
        self.assertFalse(util.is_valid_level_file('abc_def_99p_999.txt'))

        # valid filenames
        self.assertTrue(util.is_valid_level_file('level_1p_1.txt'))
        self.assertTrue(util.is_valid_level_file('level_9p_9.txt'))
        self.assertTrue(util.is_valid_level_file('level_01p_001.txt'))
        self.assertTrue(util.is_valid_level_file('level_99p_999.txt'))
        self.assertTrue(util.is_valid_level_file('level_def_01p_001.txt'))
        self.assertTrue(util.is_valid_level_file('level_def_99p_999.txt'))

        # 2. with number of players argument
        # invalid level filenames
        self.assertFalse(util.is_valid_level_file('', 1))
        self.assertFalse(util.is_valid_level_file('.txt', 1))
        self.assertFalse(util.is_valid_level_file('abc.txt', 1))
        self.assertFalse(util.is_valid_level_file('abc_def.txt', 1))
        self.assertFalse(util.is_valid_level_file('abc_def_ghi.txt', 1))
        self.assertFalse(util.is_valid_level_file('abc_def_ghi_jkl.txt', 1))
        self.assertFalse(util.is_valid_level_file('abc_def_001.txt', 1))
        self.assertFalse(util.is_valid_level_file('abc_dep_001.txt', 1))
        self.assertFalse(util.is_valid_level_file('abc_1p_1.txt', 1))
        self.assertFalse(util.is_valid_level_file('abc_9p_9.txt', 1))
        self.assertFalse(util.is_valid_level_file('abc_01p_001.txt', 1))
        self.assertFalse(util.is_valid_level_file('abc_99p_999.txt', 1))
        self.assertFalse(util.is_valid_level_file('abc_def_01p_001.txt', 1))
        self.assertFalse(util.is_valid_level_file('abc_def_99p_999.txt', 1))
        self.assertFalse(util.is_valid_level_file('level_9p_9.txt', 1))

        # valid filenames
        self.assertTrue(util.is_valid_level_file('level_1p_1.txt', 1))
        self.assertTrue(util.is_valid_level_file('level_01p_1.txt', 1))
        self.assertTrue(util.is_valid_level_file('level_001p_1.txt', 1))
        self.assertTrue(util.is_valid_level_file('level_01p_001.txt', 1))
        self.assertTrue(util.is_valid_level_file('level_99p_999.txt', 99))
        self.assertTrue(util.is_valid_level_file('level_def_5p_001.txt', 5))
        self.assertTrue(util.is_valid_level_file('level_def_10p_999.txt', 10))


unittest.main()
