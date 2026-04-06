import pygame

class Engine:
    def __init__(self, game, step_delay_ms: int = 500):
        self.game = game
        self.step_delay = step_delay_ms
        self.commands = []
        self.current_cmd_idx = 0
        self.steps_left = 0
        self.current_dir = ""
        self.is_running = False
        self.is_done = False
        self.last_step_time = 0

    def start(self, commands):
        self.commands = commands
        self.current_cmd_idx = 0
        self.is_running = True
        self.is_done = False
        self._load_command()
        self.last_step_time = pygame.time.get_ticks()

    def _load_command(self):
        if self.current_cmd_idx < len(self.commands):
            _, self.current_dir, self.steps_left = self.commands[self.current_cmd_idx]
        else:
            self.is_running = False
            self.is_done = True

    def update(self):
        if not self.is_running:
            return

        now = pygame.time.get_ticks()
        if now - self.last_step_time >= self.step_delay:
            if self.steps_left > 0:
                self.game.move(self.current_dir, 1)
                self.steps_left -= 1
                self.last_step_time = now

                if self.game.check_target():
                    self.game.add_score()
                    self.is_running = False
                    # Убран мгновенный reset_level() — теперь он в main.py после задержки
                    return
            else:
                self.current_cmd_idx += 1
                self._load_command()
                if self.is_running:
                    self.last_step_time = now
                else:
                    self.is_done = True

    def get_executing_line_idx(self) -> int:
        if self.is_running and self.current_cmd_idx < len(self.commands):
            return self.commands[self.current_cmd_idx][0]
        return -1