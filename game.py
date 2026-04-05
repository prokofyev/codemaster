import random

class Game:
    def __init__(self, grid_size: int = 10):
        self.grid_size = grid_size
        self.start_x = self.start_y = grid_size // 2
        self.score = 0
        self.reset()

    def reset(self):
        self.x, self.y = self.start_x, self.start_y
        self.target_x, self.target_y = self._generate_target()

    def _generate_target(self):
        # Генерируем позицию, отличную от стартовой
        while True:
            tx = random.randint(0, self.grid_size - 1)
            ty = random.randint(0, self.grid_size - 1)
            if (tx, ty) != (self.start_x, self.start_y):
                return tx, ty

    def reset_level(self):
        """Возвращает игрока на старт и создаёт новую цель, сохраняя очки."""
        self.x, self.y = self.start_x, self.start_y
        self.target_x, self.target_y = self._generate_target()

    def move(self, direction: str):
        if direction == 'up()':
            self.y = max(0, self.y - 1)
        elif direction == 'down()':
            self.y = min(self.grid_size - 1, self.y + 1)
        elif direction == 'left()':
            self.x = max(0, self.x - 1)
        elif direction == 'right()':
            self.x = min(self.grid_size - 1, self.x + 1)

    def check_target(self):
        return (self.x, self.y) == (self.target_x, self.target_y)

    def add_score(self, points=10):
        self.score += points

    def get_pos(self):
        return self.x, self.y

    def get_target_pos(self):
        return self.target_x, self.target_y