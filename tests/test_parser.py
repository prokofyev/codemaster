import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from code_parser import parse_code

class TestParser(unittest.TestCase):
    def test_basic_commands(self):
        cmds, _, _ = parse_code("up()\ndown\nleft()")
        self.assertEqual(cmds, [(0, 'up', 1), (1, 'down', 1), (2, 'left', 1)])

    def test_commands_with_steps(self):
        cmds, _, _ = parse_code("up(5)\nright(3)")
        self.assertEqual(cmds, [(0, 'up', 5), (1, 'right', 3)])

    def test_invalid_format(self):
        _, line, msg = parse_code("jump()\nup(5)")
        self.assertEqual(line, 0)
        self.assertIn("jump()", msg)

    def test_invalid_steps(self):
        _, line, msg = parse_code("up(0)\nup(-1)")
        self.assertEqual(line, 0)
        self.assertIn(">= 1", msg)

    def test_case_and_spaces(self):
        cmds, _, _ = parse_code("UP ( 4 )\nDown()")
        self.assertEqual(cmds, [(0, 'up', 4), (1, 'down', 1)])

if __name__ == '__main__':
    unittest.main()