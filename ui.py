import pygame
from typing import Optional

pygame.font.init()
FONT = pygame.font.SysFont(["menlo", "couriernew", "dejavusansmono", "arial"], 22)
if FONT.get_height() == 0:
    raise RuntimeError("❌ Не удалось загрузить шрифт с поддержкой кириллицы.")

CHAR_W, LINE_H = FONT.size("A")
EDITOR_START_Y = 60
BUTTON_Y_OFFSET = 70

class UI:
    def __init__(self, screen_w, screen_h):
        self.w, self.h = screen_w, screen_h
        self.mid = screen_w // 2
        self.editor_x = self.mid + 10
        
        self.code_lines = [""]
        self.cursor_line = 0
        self.cursor_col = 0
        self.exec_line = -1
        self.error_msg = ""
        self.status_msg = ""
        
        self.run_btn = pygame.Rect(self.editor_x + 20, screen_h - BUTTON_Y_OFFSET, 120, 45)
        self.clear_btn = pygame.Rect(self.run_btn.right + 15, screen_h - BUTTON_Y_OFFSET, 110, 45)
        
        self.cell_size = 50
        self.grid_size = 10
        grid_pix = self.grid_size * self.cell_size
        self.grid_off_x = (self.mid - grid_pix) // 2
        self.grid_off_y = max(50, (screen_h - grid_pix) // 2)

    def get_code_text(self) -> str:
        return "\n".join(self.code_lines)

    def set_exec_line(self, idx: int):
        self.exec_line = idx

    def set_error(self, msg: str):
        self.error_msg = msg
        if msg: self.status_msg = ""

    def set_status(self, msg: str):
        self.status_msg = msg
        if msg: self.error_msg = ""

    def handle_event(self, event) -> Optional[str]:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.run_btn.collidepoint(event.pos): return "RUN"
            if self.clear_btn.collidepoint(event.pos): return "CLEAR"
            
            if event.pos[0] > self.mid:
                rel_y = event.pos[1] - EDITOR_START_Y
                self.cursor_line = max(0, min(len(self.code_lines) - 1, rel_y // (LINE_H + 2)))
                rel_x = event.pos[0] - self.editor_x
                self.cursor_col = max(0, min(len(self.code_lines[self.cursor_line]), round(rel_x / CHAR_W)))
            return None

        if event.type == pygame.KEYDOWN:
            line = self.code_lines[self.cursor_line]
            if event.key == pygame.K_RETURN:
                self.code_lines.insert(self.cursor_line + 1, line[self.cursor_col:])
                self.code_lines[self.cursor_line] = line[:self.cursor_col]
                self.cursor_line += 1; self.cursor_col = 0
            elif event.key == pygame.K_BACKSPACE:
                if self.cursor_col > 0:
                    self.code_lines[self.cursor_line] = line[:self.cursor_col-1] + line[self.cursor_col:]
                    self.cursor_col -= 1
                elif self.cursor_line > 0:
                    prev_len = len(self.code_lines[self.cursor_line-1])
                    self.code_lines[self.cursor_line-1] += line
                    del self.code_lines[self.cursor_line]
                    self.cursor_line -= 1; self.cursor_col = prev_len
            elif event.key == pygame.K_UP and self.cursor_line > 0:
                self.cursor_line -= 1
                self.cursor_col = min(self.cursor_col, len(self.code_lines[self.cursor_line]))
            elif event.key == pygame.K_DOWN and self.cursor_line < len(self.code_lines) - 1:
                self.cursor_line += 1
                self.cursor_col = min(self.cursor_col, len(self.code_lines[self.cursor_line]))
            elif event.key == pygame.K_LEFT:
                if self.cursor_col > 0: self.cursor_col -= 1
                elif self.cursor_line > 0:
                    self.cursor_line -= 1
                    self.cursor_col = len(self.code_lines[self.cursor_line])
            elif event.key == pygame.K_RIGHT:
                if self.cursor_col < len(line): self.cursor_col += 1
                elif self.cursor_line < len(self.code_lines) - 1:
                    self.cursor_line += 1
                    self.cursor_col = 0
            elif event.unicode and event.unicode.isprintable():
                self.code_lines[self.cursor_line] = line[:self.cursor_col] + event.unicode + line[self.cursor_col:]
                self.cursor_col += 1
        return None

    def draw(self, screen, game):
        screen.fill((25, 25, 35))
        
        # Очки
        score_surf = FONT.render(f"⭐ Очки: {game.score}", True, (255, 215, 0))
        screen.blit(score_surf, (self.mid - score_surf.get_width() // 2, 10))
        
        # Сетка
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                rect = pygame.Rect(self.grid_off_x + c * self.cell_size,
                                   self.grid_off_y + r * self.cell_size,
                                   self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (40, 40, 60), rect, 1)
                
        # Цель
        tx, ty = game.target_x, game.target_y
        pygame.draw.rect(screen, (60, 140, 240), 
                         pygame.Rect(self.grid_off_x + tx * self.cell_size + 4,
                                     self.grid_off_y + ty * self.cell_size + 4,
                                     self.cell_size - 8, self.cell_size - 8))
            
        # Игрок
        px, py = game.x, game.y
        pygame.draw.rect(screen, (230, 60, 60), 
                         pygame.Rect(self.grid_off_x + px * self.cell_size + 4,
                                     self.grid_off_y + py * self.cell_size + 4,
                                     self.cell_size - 8, self.cell_size - 8))

        # Редактор
        for i, line in enumerate(self.code_lines):
            y = EDITOR_START_Y + i * (LINE_H + 2)
            if y > self.h - 80: break
            
            bg = (80, 70, 30) if i == self.exec_line else (35, 35, 50)
            pygame.draw.rect(screen, bg, (self.mid, y, self.w - self.mid, LINE_H + 2))
            screen.blit(FONT.render(line, True, (220, 220, 220)), (self.editor_x, y + 2))
            
            if i == self.cursor_line:
                cx = self.editor_x + self.cursor_col * CHAR_W
                pygame.draw.line(screen, (255, 255, 0), (cx, y+2), (cx, y+LINE_H), 2)

        # Кнопки
        pygame.draw.rect(screen, (50, 160, 70), self.run_btn, border_radius=8)
        screen.blit(FONT.render("▶ RUN", True, (255, 255, 255)), (self.run_btn.x + 25, self.run_btn.y + 8))
        pygame.draw.rect(screen, (160, 60, 60), self.clear_btn, border_radius=8)
        screen.blit(FONT.render("✕ CLEAR", True, (255, 255, 255)), (self.clear_btn.x + 15, self.clear_btn.y + 8))

        # Сообщения
        msg = self.error_msg or self.status_msg
        if msg:
            color = (255, 100, 100) if self.error_msg else (100, 255, 150)
            screen.blit(FONT.render(msg, True, color), (self.editor_x, self.h - 35))