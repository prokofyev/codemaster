import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from game import Game
from engine import Engine

class MockTime:
    def __init__(self):
        self.ticks = 0
    def __call__(self):
        return self.ticks

class TestEngine(unittest.TestCase):
    def setUp(self):
        self.mock_time = MockTime()
        # Патчим pygame.time.get_ticks для тестов
        import pygame.time
        self.original_get_ticks = pygame.time.get_ticks
        pygame.time.get_ticks = self.mock_time
        
        self.game = Game()
        self.engine = Engine(self.game, step_delay_ms=100)

    def tearDown(self):
        import pygame.time
        pygame.time.get_ticks = self.original_get_ticks

    def test_execution_steps(self):
        cmds = [(0, 'up()'), (1, 'right()')]
        self.engine.start(cmds)
        
        # Первый шаг
        self.mock_time.ticks = 100
        self.engine.update()
        self.assertEqual(self.engine.get_executing_line_idx(), 0)
        self.assertEqual(self.game.get_pos(), (5, 4)) # up от центра (5,5) -> y=4
        
        # Второй шаг
        self.mock_time.ticks = 200
        self.engine.update()
        self.assertEqual(self.engine.get_executing_line_idx(), 1)
        self.assertEqual(self.game.get_pos(), (6, 4)) # right -> x=6
        
        # Завершение
        self.mock_time.ticks = 300
        self.engine.update()
        self.assertTrue(self.engine.is_done)
        self.assertFalse(self.engine.is_running)

    def test_boundary_clamping(self):
        cmds = [(0, 'left()') for _ in range(15)]
        self.engine.start(cmds)
        
        # Двигаем влево 15 раз (сетка 10x10, центр 5)
        for i in range(1, 16):
            self.mock_time.ticks = i * 100
            self.engine.update()
            
        x, y = self.game.get_pos()
        self.assertEqual(x, 0)  # Не должен уйти за левую границу
        self.assertEqual(y, 5)

if __name__ == '__main__':
    unittest.main()