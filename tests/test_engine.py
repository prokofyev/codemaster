import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from game import Game
from engine import Engine, EngineState
import pygame.time

class MockTime:
    def __init__(self): self.ticks = 0
    def __call__(self): return self.ticks

class TestEngine(unittest.TestCase):
    def setUp(self):
        import pygame.time
        self.mock_time = MockTime()
        self.original_get_ticks = pygame.time.get_ticks
        pygame.time.get_ticks = self.mock_time

        self.game = Game()
        self.game.target_x, self.game.target_y = 9, 9  # Цель далеко
        self.game.x, self.game.y = 5, 5
        self.engine = Engine(self.game, step_delay_ms=100)

    def tearDown(self):
        import pygame.time
        pygame.time.get_ticks = self.original_get_ticks

    def _simulate_steps(self, count, start_tick=0, delay=100):
        for i in range(count):
            self.mock_time.ticks = start_tick + (i + 1) * delay
            self.engine.update()

    def test_move_with_steps_clamping(self):
        cmds = [(0, 'up', 100)]
        self.engine.start(cmds)
        self._simulate_steps(6)
        self.assertEqual((self.game.x, self.game.y), (5, 0))

    def test_multiple_commands_execution(self):
        cmds = [(0, 'right', 3), (1, 'down', 2)]
        self.engine.start(cmds)

        # 3 шага вправо
        self._simulate_steps(3)
        self.assertEqual((self.game.x, self.game.y), (8, 5))
        self.assertEqual(self.engine.current_cmd_idx, 1) 

        # 2 шага вниз
        self._simulate_steps(2, start_tick=300)
        self.assertEqual((self.game.x, self.game.y), (8, 7))
        self.assertEqual(self.engine.state, EngineState.COMPLETED)

if __name__ == '__main__':
    unittest.main()