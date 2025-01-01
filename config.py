# config.py
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env
load_dotenv()

# OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

# Telegram
TELEGRAM_TOKEN = os.getenv("API_TOKEN")

# База данных
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///girl_helper.db")

# Валидация переменных
REQUIRED_VARS = {
    "OPENAI_API_KEY": OPENAI_API_KEY,
    "ASSISTANT_ID": ASSISTANT_ID,
    "TELEGRAM_TOKEN": TELEGRAM_TOKEN,
}

for var_name, var_value in REQUIRED_VARS.items():
    if not var_value:
        raise ValueError(f"Не задана обязательная переменная окружения: {var_name}")

# Завершение файла
