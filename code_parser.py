import re

# Паттерн: направление + опциональные скобки с числом внутри
CMD_PATTERN = re.compile(r'^(up|down|left|right)\s*(?:\(\s*(\d*)\s*\))?$', re.IGNORECASE)

def parse_code(text: str):
    lines = text.split('\n')
    commands = []

    for i, line in enumerate(lines):
        cmd = line.strip()
        if not cmd:
            continue

        match = CMD_PATTERN.match(cmd)
        if not match:
            return None, i, f"❌ Ошибка на строке {i+1}: неверный формат '{cmd}'"

        direction = match.group(1).lower()
        steps_str = match.group(2)
        steps = int(steps_str) if steps_str else 1

        if steps < 1:
            return None, i, f"❌ Ошибка на строке {i+1}: количество шагов должно быть >= 1"

        # Формат: (номер_строки, направление, шаги)
        commands.append((i, direction, steps))

    return commands, None, None