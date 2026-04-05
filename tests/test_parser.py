import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from code_parser import parse_code

class TestParser(unittest.TestCase):
    def test_valid_program(self):
        code = "up()\nleft()\nright()\ndown()"
        cmds, err_line, err_msg = parse_code(code)
        self.assertIsNotNone(cmds)
        self.assertEqual(len(cmds), 4)
        self.assertEqual(cmds[0][1], 'up()')
        self.assertIsNone(err_line)

    def test_invalid_command(self):
        code = "up()\njump()\nleft()"
        cmds, err_line, err_msg = parse_code(code)
        self.assertIsNone(cmds)
        self.assertEqual(err_line, 1)
        self.assertIn("jump()", err_msg)

    def test_case_insensitive(self):
        code = "UP()\nLeft()"
        cmds, _, _ = parse_code(code)
        self.assertIsNotNone(cmds)
        self.assertEqual(cmds[0][1], 'up()')
        self.assertEqual(cmds[1][1], 'left()')

    def test_empty_lines_ignored(self):
        code = "up()\n\nright()\n"
        cmds, _, _ = parse_code(code)
        self.assertEqual(len(cmds), 2)

if __name__ == '__main__':
    unittest.main()