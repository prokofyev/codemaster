import pygame

class Engine:
    def __init__(self, game, step_delay_ms: int = 800):
        self.game = game
        self.step_delay = step_delay_ms
        self.commands = []
        self.current_idx = -1
        self.is_running = False
        self.is_done = False
        self.last_step_time = 0

    def start(self, commands):
        """Запускает выполнение списка команд."""
        self.commands = commands
        self.current_idx = -1
        self.is_running = True
        self.is_done = False
        self.game.reset()
        self.last_step_time = pygame.time.get_ticks()

    def update(self):
        """Вызывается в каждом кадре. Выполняет следующую команду по таймеру."""
        if not self.is_running:
            return

        now = pygame.time.get_ticks()
        if now - self.last_step_time >= self.step_delay:
            self.current_idx += 1
            if self.current_idx >= len(self.commands):
                self.is_running = False
                self.is_done = True
                return

            _, cmd = self.commands[self.current_idx]
            self.game.move(cmd)
            self.last_step_time = now

    def get_executing_line_idx(self):
        """Возвращает индекс строки в редакторе, которая выполняется сейчас."""
        if 0 <= self.current_idx < len(self.commands):
            return self.commands[self.current_idx][0]
        return -1