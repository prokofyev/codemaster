class Game:
    def __init__(self, grid_size: int = 10):
        self.grid_size = grid_size
        self.reset()

    def reset(self):
        # Стартовая позиция в центре сетки
        center = self.grid_size // 2
        self.x, self.y = center, center

    def move(self, direction: str):
        if direction == 'up()':
            self.y = max(0, self.y - 1)
        elif direction == 'down()':
            self.y = min(self.grid_size - 1, self.y + 1)
        elif direction == 'left()':
            self.x = max(0, self.x - 1)
        elif direction == 'right()':
            self.x = min(self.grid_size - 1, self.x + 1)

    def get_pos(self):
        return self.x, self.y