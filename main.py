import pygame
import sys
from code_parser import parse_code  # Убедитесь, что файл называется code_parser.py
from game import Game
from engine import Engine
from ui import UI
from storage import load_code, save_code

def main():
    pygame.init()
    info = pygame.display.Info()
    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption("Учимся программировать")
    clock = pygame.time.Clock()

    ui = UI(info.current_w, info.current_h)
    game = Game()
    engine = Engine(game, step_delay_ms=600)

    # 🔽 Загружаем сохранённый код при запуске
    ui.code_lines = load_code()
    ui.cursor_line = len(ui.code_lines) - 1
    ui.cursor_col = len(ui.code_lines[-1])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            
            action = ui.handle_event(event)
            
            if action == "RUN":
                save_code(ui.code_lines)  # 💾 Сохраняем перед запуском
                code = ui.get_code_text()
                commands, err_line, err_msg = parse_code(code)
                if commands is None:
                    ui.set_error(err_msg)
                    ui.set_exec_line(err_line)
                    engine.is_running = False
                else:
                    ui.set_error("")
                    ui.set_exec_line(-1)
                    engine.start(commands)
                    
            elif action == "CLEAR":
                # 🧹 Очистка редактора и остановка выполнения
                ui.code_lines = [""]
                ui.cursor_line = 0
                ui.cursor_col = 0
                ui.set_error("")
                ui.set_exec_line(-1)
                engine.is_running = False
                engine.is_done = False
                game.reset()
                save_code(ui.code_lines)  # 💾 Сохраняем пустой файл

        # Обновление движка
        if engine.is_running:
            engine.update()
            ui.set_exec_line(engine.get_executing_line_idx())
            if engine.is_done:
                ui.set_exec_line(-1)
                ui.set_error("✅ Программа выполнена!")

        ui.draw(screen, game)
        pygame.display.flip()
        clock.tick(60)

    # 💾 Финальное сохранение при выходе
    save_code(ui.code_lines)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()