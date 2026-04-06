import pygame
import sys
from code_parser import parse_code
from game import Game
from engine import Engine, EngineState
from ui import UI
from storage import load_code, save_code

def main():
    pygame.init()
    pygame.key.set_repeat(500, 50)
    info = pygame.display.Info()
    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption("Учимся программировать")
    clock = pygame.time.Clock()

    ui = UI(info.current_w, info.current_h)
    game = Game()
    engine = Engine(game, step_delay_ms=500)

    ui.code_lines = load_code()
    ui.cursor_line = len(ui.code_lines) - 1
    ui.cursor_col = len(ui.code_lines[-1]) if ui.code_lines else 0

    level_complete_start_time = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: running = False
            
            action = ui.handle_event(event)
            # Блокируем кнопки во время показа сообщения о новом уровне
            if action == "RUN":
                # Если предыдущий запуск завершился полностью (без цели)
                if engine.state == EngineState.COMPLETED:
                    game.reset_player()
                    ui.set_status("")
                    
                save_code(ui.code_lines)
                commands, err_line, err_msg = parse_code(ui.get_code_text())
                if commands is None:
                    ui.set_error(err_msg)
                    ui.set_exec_line(err_line)
                    engine.is_running = False
                else:
                    ui.set_error("")
                    ui.set_status("")
                    ui.set_exec_line(-1)
                    engine.start(commands)
                    
            elif level_complete_start_time == 0 and action == "CLEAR":
                ui.code_lines = [""]
                ui.cursor_line = 0; ui.cursor_col = 0
                ui.set_error(""); ui.set_status(""); ui.set_exec_line(-1)
                engine.is_running = False; engine.is_done = False
                save_code(ui.code_lines)

        if engine.state == EngineState.RUNNING:
            engine.update()
            ui.set_exec_line(engine.get_executing_line_idx())
            
            # Проверяем, почему остановился движок
            if engine.state != EngineState.RUNNING:
                ui.set_exec_line(-1)
                if engine.state == EngineState.COMPLETED:
                    ui.set_status("Программа выполнена!")
                elif engine.state == EngineState.TARGET_REACHED:
                    if level_complete_start_time == 0:
                        level_complete_start_time = pygame.time.get_ticks()

        # Таймер: через 2 секунды скрываем сообщение и запускаем новый уровень
        if level_complete_start_time > 0:
            now = pygame.time.get_ticks()
            if now - level_complete_start_time >= 2000:
                game.reset_level()
                ui.code_lines = [""]
                ui.cursor_line = 0; ui.cursor_col = 0
                save_code(ui.code_lines)
                ui.set_status("")
                level_complete_start_time = 0

        ui.draw(screen, game, show_level_msg=(level_complete_start_time > 0))
        pygame.display.flip()
        clock.tick(60)

    save_code(ui.code_lines)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()