
import unittest
import context

from config import Gameconfig
from runner import Runner


class TestRunner(unittest.TestCase):
    """Unittest class for an object moving on the grid (Runner)"""

    def setUp(self):
        """Initializes the variables etc."""
        self.cfg = Gameconfig()

    def test_move_middle(self):
        """Tests the movement in the middle of a grid line"""
        r = Runner(self.cfg, None)

        # moving up
        r.set_position(1.0, 1.5)
        r.vel = 0.2
        r.move_direction = 0
        r.update_position(1)
        self.assertTrue(r.x == 1.0)
        self.assertTrue(1.29 < r.y < 1.31)
        self.assertFalse(r.node_visited_x)
        self.assertFalse(r.node_visited_y)
        self.assertEqual(r.dt_ms_rem, 0)

        # moving right
        r.set_position(1.5, 1.0)
        r.vel = 0.2
        r.move_direction = 1
        r.update_position(1)
        self.assertTrue(1.69 < r.x < 1.71)
        self.assertTrue(r.y == 1.0)
        self.assertFalse(r.node_visited_x)
        self.assertFalse(r.node_visited_y)
        self.assertEqual(r.dt_ms_rem, 0)

        # moving down
        r.set_position(1.0, 1.5)
        r.vel = 0.2
        r.move_direction = 2
        r.update_position(1)
        self.assertTrue(r.x == 1.0)
        self.assertTrue(1.69 < r.y < 1.71)
        self.assertFalse(r.node_visited_x)
        self.assertFalse(r.node_visited_y)
        self.assertEqual(r.dt_ms_rem, 0)

        # moving left
        r.set_position(1.5, 1.0)
        r.vel = 0.2
        r.move_direction = 3
        r.update_position(1)
        self.assertTrue(1.29 < r.x < 1.31)
        self.assertTrue(r.y == 1.0)
        self.assertFalse(r.node_visited_x)
        self.assertFalse(r.node_visited_y)
        self.assertEqual(r.dt_ms_rem, 0)

    def test_move_from_node(self):
        """Tests the movement on one grid line (starting at a node)"""
        r = Runner(self.cfg, None)

        # moving up
        r.set_position(1.0, 1.0)
        r.vel = 0.2
        r.move_direction = 0
        r.update_position(1)
        self.assertTrue(r.x == 1.0)
        self.assertTrue(0.79 < r.y < 0.81)
        self.assertFalse(r.node_visited_x)
        self.assertFalse(r.node_visited_y)
        self.assertEqual(r.dt_ms_rem, 0)

        # moving right
        r.set_position(1.0, 1.0)
        r.vel = 0.2
        r.move_direction = 1
        r.update_position(1)
        self.assertTrue(1.19 < r.x < 1.21)
        self.assertTrue(r.y == 1.0)
        self.assertFalse(r.node_visited_x)
        self.assertFalse(r.node_visited_y)
        self.assertEqual(r.dt_ms_rem, 0)

        # moving down
        r.set_position(1.0, 1.0)
        r.vel = 0.2
        r.move_direction = 2
        r.update_position(1)
        self.assertTrue(r.x == 1.0)
        self.assertTrue(1.19 < r.y < 1.21)
        self.assertFalse(r.node_visited_x)
        self.assertFalse(r.node_visited_y)
        self.assertEqual(r.dt_ms_rem, 0)

        # moving left
        r.set_position(1.0, 1.0)
        r.vel = 0.2
        r.move_direction = 3
        r.update_position(1)
        self.assertTrue(0.79 < r.x < 0.81)
        self.assertTrue(r.y == 1.0)
        self.assertFalse(r.node_visited_x)
        self.assertFalse(r.node_visited_y)
        self.assertEqual(r.dt_ms_rem, 0)

    def test_move_node_crossing(self):
        """Tests that the moving across nodes is working ok"""
        r = Runner(self.cfg, None)

        # moving up
        r.set_position(1.0, 2.1)
        r.vel = 0.2
        r.move_direction = 0
        r.update_position(1)
        self.assertTrue(r.x == 1.0)
        self.assertTrue(1.89 < r.y < 1.91)
        self.assertEqual(r.node_visited_x, 1)
        self.assertEqual(r.node_visited_y, 2)
        self.assertEqual(r.dt_ms_rem, 0)

        # moving right
        r.set_position(1.9, 2.0)
        r.vel = 0.2
        r.move_direction = 1
        r.update_position(1)
        self.assertTrue(2.09 < r.x < 2.11)
        self.assertTrue(r.y == 2.0)
        self.assertEqual(r.node_visited_x, 2)
        self.assertEqual(r.node_visited_y, 2)
        self.assertEqual(r.dt_ms_rem, 0)

        # moving down
        r.set_position(1.0, 0.9)
        r.vel = 0.2
        r.move_direction = 2
        r.update_position(1)
        self.assertTrue(r.x == 1.0)
        self.assertTrue(1.09 < r.y < 1.11)
        self.assertEqual(r.node_visited_x, 1)
        self.assertEqual(r.node_visited_y, 1)
        self.assertEqual(r.dt_ms_rem, 0)

        # moving left
        r.set_position(1.9, 2.0)
        r.vel = 1.5
        r.move_direction = 3
        r.update_position(1)
        self.assertTrue(0.39 < r.x < 0.41)
        self.assertTrue(r.y == 2.0)
        self.assertEqual(r.node_visited_x, 1)
        self.assertEqual(r.node_visited_y, 2)
        self.assertEqual(r.dt_ms_rem, 0)


unittest.main()
