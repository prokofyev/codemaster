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
        pygame.time.get_ticks = self.mock_time
        self.game = Game()
        # Фиксируем цель для предсказуемости теста
        self.game.target_x, self.game.target_y = 5, 4
        self.engine = Engine(self.game, step_delay_ms=100)

    def test_target_reached_and_score(self):
        cmds = [(0, 'up()')]
        self.engine.start(cmds)
        self.mock_time.ticks = 100
        self.engine.update()
        
        self.assertTrue(self.engine.level_completed)
        self.assertEqual(self.game.score, 10)
        self.assertEqual(self.game.get_pos(), (5, 5)) # Вернулся на старт после сброса уровня
        self.assertFalse(self.engine.is_running)

    def test_boundary_clamping(self):
        cmds = [(0, 'left()') for _ in range(15)]
        self.engine.start(cmds)
        for i in range(1, 16):
            self.mock_time.ticks = i * 100
            self.engine.update()
        x, y = self.game.get_pos()
        self.assertEqual(x, 0)
        self.assertEqual(y, 5)

if __name__ == '__main__':
    unittest.main()