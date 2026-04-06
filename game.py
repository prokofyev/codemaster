import random

class Game:
    def __init__(self, grid_size: int = 10):
        self.grid_size = grid_size
        self.start_pos = (grid_size // 2, grid_size // 2)
        self.score = 0
        self.reset()

    def reset(self):
        self.x, self.y = self.start_pos
        self.target_x, self.target_y = self._generate_target()
        self.score = 0

    def reset_player(self):
        """Возвращает игрока на стартовую позицию, сохраняя текущую цель и очки."""
        self.x, self.y = self.start_pos

    def _generate_target(self):
        while True:
            tx = random.randint(0, self.grid_size - 1)
            ty = random.randint(0, self.grid_size - 1)
            if (tx, ty) != self.start_pos:
                return tx, ty

    def reset_level(self):
        self.x, self.y = self.start_pos
        self.target_x, self.target_y = self._generate_target()

    def move(self, direction: str, steps: int = 1):
        if direction == 'up':
            self.y = max(0, self.y - steps)
        elif direction == 'down':
            self.y = min(self.grid_size - 1, self.y + steps)
        elif direction == 'left':
            self.x = max(0, self.x - steps)
        elif direction == 'right':
            self.x = min(self.grid_size - 1, self.x + steps)

    def check_target(self) -> bool:
        return (self.x, self.y) == (self.target_x, self.target_y)

    def add_score(self, points: int = 10):
        self.score += points