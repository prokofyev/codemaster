import pygame

class Engine:
    def __init__(self, game, step_delay_ms: int = 600):
        self.game = game
        self.step_delay = step_delay_ms
        self.commands = []
        self.current_idx = -1
        self.is_running = False
        self.is_done = False
        self.last_step_time = 0

    def start(self, commands):
        self.commands = commands
        self.current_idx = -1
        self.is_running = True
        self.is_done = False
        self.last_step_time = pygame.time.get_ticks()

    def update(self):
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

            if self.game.check_target():
                self.game.add_score()
                self.game.reset_level()
                self.is_running = False
                self.is_done = False  # Уровень сброшен, сбрасываем флаг завершения

    def get_executing_line_idx(self) -> int:
        return self.commands[self.current_idx][0] if 0 <= self.current_idx < len(self.commands) else -1