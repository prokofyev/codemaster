import pygame

pygame.font.init()
FONT = pygame.font.SysFont(["menlo", "couriernew", "dejavusansmono", "arial"], 22)
CHAR_W, LINE_H = FONT.size("A")

class UI:
    def __init__(self, screen_w, screen_h):
        self.w, self.h = screen_w, screen_h
        self.mid = screen_w // 2
        
        # Редактор
        self.editor_x = self.mid + 10
        self.code_lines = [""]
        self.cursor_line = 0
        self.cursor_col = 0
        self.exec_line = -1  # Индекс подсвечиваемой строки
        self.error_msg = ""
        
        # Кнопка RUN
        self.run_btn = pygame.Rect(self.editor_x + 20, screen_h - 70, 120, 45)
        self.clear_btn = pygame.Rect(self.run_btn.right + 15, screen_h - 70, 110, 45)
        
        # Игровое поле
        self.cell_size = 50
        self.grid_size = 10
        grid_pix = self.grid_size * self.cell_size
        self.grid_off_x = (self.mid - grid_pix) // 2
        self.grid_off_y = (screen_h - grid_pix) // 2

    def get_code_text(self):
        return "\n".join(self.code_lines)

    def set_exec_line(self, line_idx):
        self.exec_line = line_idx

    def set_error(self, msg):
        self.error_msg = msg

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.run_btn.collidepoint(event.pos):
                return "RUN"
            if self.clear_btn.collidepoint(event.pos):
                return "CLEAR"
            # Клик в области редактора
            if event.pos[0] > self.mid:
                rel_y = event.pos[1] - 30
                self.cursor_line = max(0, min(len(self.code_lines) - 1, rel_y // (LINE_H + 2)))
                rel_x = event.pos[0] - self.editor_x
                self.cursor_col = max(0, min(len(self.code_lines[self.cursor_line]), round(rel_x / CHAR_W)))
            return None

        # 2. Обработка клавиатуры — всегда разрешаем ввод, если фокус на редакторе
        # (упрощённо: считаем, что редактор всегда активен для клавиатуры)
        if event.type == pygame.KEYDOWN:
            line = self.code_lines[self.cursor_line]
            
            if event.key == pygame.K_RETURN:
                # Перенос строки
                self.code_lines.insert(self.cursor_line + 1, line[self.cursor_col:])
                self.code_lines[self.cursor_line] = line[:self.cursor_col]
                self.cursor_line += 1
                self.cursor_col = 0
            elif event.key == pygame.K_BACKSPACE:
                if self.cursor_col > 0:
                    self.code_lines[self.cursor_line] = line[:self.cursor_col-1] + line[self.cursor_col:]
                    self.cursor_col -= 1
                elif self.cursor_line > 0:
                    # Объединение с предыдущей строкой
                    prev_len = len(self.code_lines[self.cursor_line-1])
                    self.code_lines[self.cursor_line-1] += line
                    del self.code_lines[self.cursor_line]
                    self.cursor_line -= 1
                    self.cursor_col = prev_len
            elif event.key == pygame.K_UP and self.cursor_line > 0:
                self.cursor_line -= 1
                self.cursor_col = min(self.cursor_col, len(self.code_lines[self.cursor_line]))
            elif event.key == pygame.K_DOWN and self.cursor_line < len(self.code_lines) - 1:
                self.cursor_line += 1
                self.cursor_col = min(self.cursor_col, len(self.code_lines[self.cursor_line]))
            elif event.key == pygame.K_LEFT:
                if self.cursor_col > 0:
                    self.cursor_col -= 1
                elif self.cursor_line > 0:
                    self.cursor_line -= 1
                    self.cursor_col = len(self.code_lines[self.cursor_line])
            elif event.key == pygame.K_RIGHT:
                if self.cursor_col < len(line):
                    self.cursor_col += 1
                elif self.cursor_line < len(self.code_lines) - 1:
                    self.cursor_line += 1
                    self.cursor_col = 0
            elif event.unicode and event.unicode.isprintable():
                # Вставка символа
                self.code_lines[self.cursor_line] = line[:self.cursor_col] + event.unicode + line[self.cursor_col:]
                self.cursor_col += 1
            return None
            
        return None

    def draw(self, screen, game):
        screen.fill((25, 25, 35))
        
        # 1. Игровое поле (левая часть)
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                rect = pygame.Rect(self.grid_off_x + c * self.cell_size,
                                   self.grid_off_y + r * self.cell_size,
                                   self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (40, 40, 60), rect, 1)
                
        # Игрок
        px, py = game.get_pos()
        player_rect = pygame.Rect(self.grid_off_x + px * self.cell_size + 4,
                                  self.grid_off_y + py * self.cell_size + 4,
                                  self.cell_size - 8, self.cell_size - 8)
        pygame.draw.rect(screen, (230, 60, 60), player_rect)
        pygame.draw.rect(screen, (255, 255, 255), player_rect, 2)

        # 2. Редактор (правая часть)
        for i, line in enumerate(self.code_lines):
            y = 30 + i * (LINE_H + 2)
            if y > self.h - 80: break
            
            bg = (35, 35, 50)
            if i == self.exec_line:
                bg = (80, 70, 30)  # Подсветка выполняемой строки
                
            pygame.draw.rect(screen, bg, (self.mid, y, self.w - self.mid, LINE_H + 2))
            
            line_surf = FONT.render(line, True, (220, 220, 220))
            screen.blit(line_surf, (self.editor_x, y + 2))
            
            # Курсор
            if i == self.cursor_line:
                cx = self.editor_x + self.cursor_col * CHAR_W
                pygame.draw.line(screen, (255, 255, 0), (cx, y+2), (cx, y+LINE_H), 2)

        # 3. Кнопка RUN
        pygame.draw.rect(screen, (50, 160, 70), self.run_btn, border_radius=8)
        btn_txt = FONT.render("▶ RUN", True, (255, 255, 255))
        screen.blit(btn_txt, (self.run_btn.x + 25, self.run_btn.y + 8))

        # Кнопка CLEAR
        pygame.draw.rect(screen, (160, 60, 60), self.clear_btn, border_radius=8)
        clear_txt = FONT.render("✕ CLEAR", True, (255, 255, 255))
        screen.blit(clear_txt, (self.clear_btn.x + 15, self.clear_btn.y + 8))

        # 4. Сообщения об ошибках/статусе
        if self.error_msg:
            err_surf = FONT.render(self.error_msg, True, (255, 100, 100))
            screen.blit(err_surf, (self.editor_x, self.h - 35))