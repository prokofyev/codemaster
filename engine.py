import pygame
from enum import Enum, auto

class EngineState(Enum):
    RUNNING = auto()
    COMPLETED = auto()       # Все команды выполнены
    TARGET_REACHED = auto()  # Цель достигнута досрочно

class Engine:
    def __init__(self, game, step_delay_ms: int = 500):
        self.game = game
        self.step_delay = step_delay_ms
        self.commands = []
        self.current_cmd_idx = 0
        self.steps_left = 0
        self.current_dir = ""
        self.state = EngineState.COMPLETED
        self.last_step_time = 0

    def start(self, commands):
        self.commands = commands
        self.current_cmd_idx = 0
        self.state = EngineState.RUNNING
        self._load_command()
        self.last_step_time = pygame.time.get_ticks()

    def _load_command(self):
        if self.current_cmd_idx < len(self.commands):
            _, self.current_dir, self.steps_left = self.commands[self.current_cmd_idx]
        else:
            self.state = EngineState.COMPLETED

    def update(self):
        if self.state != EngineState.RUNNING:
            return

        now = pygame.time.get_ticks()
        if now - self.last_step_time >= self.step_delay:
            if self.steps_left > 0:
                self.game.move(self.current_dir, 1)
                self.steps_left -= 1
                self.last_step_time = now

                if self.game.check_target():
                    self.game.add_score()
                    self.state = EngineState.TARGET_REACHED
                    return

            # ✅ Мгновенный переход к следующей команде после последнего шага
            if self.steps_left == 0:
                self.current_cmd_idx += 1
                self._load_command()
                if self.state == EngineState.RUNNING:
                    self.last_step_time = now  # Сброс таймера для задержки перед следующей командой

    def get_executing_line_idx(self) -> int:
        if self.state == EngineState.RUNNING and self.current_cmd_idx < len(self.commands):
            return self.commands[self.current_cmd_idx][0]
        return -1