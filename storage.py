import os

DEFAULT_CODE_FILE = "saved_code.txt"

def load_code(filepath: str = DEFAULT_CODE_FILE):
    """Загружает код из файла. Возвращает список строк."""
    if not os.path.exists(filepath):
        return [""]
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        lines = content.split("\n")
        return lines if lines else [""]
    except Exception:
        return [""]

def save_code(lines: list, filepath: str = DEFAULT_CODE_FILE):
    """Сохраняет список строк в файл."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
    except Exception as e:
        print(f"⚠️ Ошибка сохранения: {e}")