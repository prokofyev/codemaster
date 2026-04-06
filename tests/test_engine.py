import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from game import Game
from engine import Engine
import pygame.time

class MockTime:
    def __init__(self): self.ticks = 0
    def __call__(self): return self.ticks

class TestEngine(unittest.TestCase):
    def setUp(self):
        self.mock_time = MockTime()
        self.original_get_ticks = pygame.time.get_ticks
        pygame.time.get_ticks = self.mock_time
        
        self.game = Game()
        self.engine = Engine(self.game, step_delay_ms=100)

    def tearDown(self):
        pygame.time.get_ticks = self.original_get_ticks

    def test_move_with_steps_clamping(self):
        # Центр (5,5). up(100) должен привести к (5,0), не выходя за границу
        cmds = [(0, 'up', 100)]
        self.engine.start(cmds)
        self.mock_time.ticks = 100
        self.engine.update()
        self.assertEqual((self.game.x, self.game.y), (5, 0))
        self.assertTrue(self.game.check_target() if (5,0) == (self.game.target_x, self.game.target_y) else True)

    def test_multiple_commands_execution(self):
        cmds = [(0, 'right', 3), (1, 'down', 2)]
        self.engine.start(cmds)
        
        self.mock_time.ticks = 100
        self.engine.update()
        self.assertEqual((self.game.x, self.game.y), (8, 5))
        
        self.mock_time.ticks = 200
        self.engine.update()
        self.assertEqual((self.game.x, self.game.y), (8, 7))
        
        self.mock_time.ticks = 300
        self.engine.update()
        self.assertFalse(self.engine.is_running)
        self.assertTrue(self.engine.is_done)

if __name__ == '__main__':
    unittest.main()