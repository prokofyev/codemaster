VALID_COMMANDS = {'up()', 'down()', 'left()', 'right()'}

def parse_code(text: str):
    """
    Парсит текст программы.
    Возвращает:
      - (commands, None, None) при успехе. commands = [(line_idx, cmd), ...]
      - (None, error_line_idx, error_message) при ошибке.
    """
    lines = text.split('\n')
    commands = []
    
    for i, line in enumerate(lines):
        cmd = line.strip().lower()
        if not cmd:
            continue  # Пропускаем пустые строки
        if cmd not in VALID_COMMANDS:
            return None, i, f"❌ Ошибка на строке {i+1}: неизвестная команда '{cmd}'"
        commands.append((i, cmd))
        
    return commands, None, None