# utils.py
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def format_profile(profile):
    """
    Форматирует данные профиля пользователя или кандидата для отображения.
    """
    if not profile:
        return "Профиль не найден."
    return (
        f"Имя: {profile.get('name', 'Не указано')}\n"
        f"Возраст: {profile.get('age', 'Не указан')}\n"
        f"Город: {profile.get('city', 'Не указан')}\n"
        f"Интересы: {profile.get('interests', 'Не указаны')}\n"
        f"Цели: {profile.get('goals', 'Не указаны')}\n"
    )

def format_date(timestamp):
    """
    Форматирует дату и время для отображения в переписке.
    """
    if not timestamp:
        return "Неизвестное время"
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def handle_error(error):
    """
    Логирует ошибки и возвращает пользовательское сообщение.
    """
    logger.error(f"Ошибка: {error}")
    return "Произошла ошибка. Попробуйте еще раз."

def prepare_openai_prompt(instructions, data):
    """
    Форматирует инструкции и данные для ассистента OpenAI.
    """
    return f"Инструкции:\n{instructions}\n\nДанные:\n{data}"
