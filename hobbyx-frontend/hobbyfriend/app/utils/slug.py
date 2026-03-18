import re
import unicodedata
import random
import string

def generate_slug(text: str) -> str:
    """
    Генерирует уникальный slug:
    - Приводит текст к ASCII (убирает акценты)
    - Заменяет все небуквенно-цифровые символы на "-"
    - Добавляет уникальный суффикс из 4 символов
    """
    # Приводим текст к нормальной форме (убираем акценты)
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    
    # Делаем все маленькими буквами
    text = text.lower()
    
    # Заменяем все небуквенные и нецифровые символы на тире
    text = re.sub(r"[^a-z0-9]+", "-", text)
    
    # Убираем лишние тире по краям
    text = text.strip("-")
    
    # Добавляем случайный суффикс для уникальности
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    
    return f"{text}-{suffix}"