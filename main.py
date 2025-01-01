import logging
from queue import Queue
from threading import Thread
from dotenv import load_dotenv
import os
from bot.handlers import start_bot
from services.database import init_db
from services.candidate_filter import analyze_message_and_update_candidate
from services.response_generator import generate_response
from services.assistant_chat import handle_user_query

# Загрузка переменных окружения из .env
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Основные переменные
API_TOKEN = os.getenv("API_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# Очередь сообщений
message_queue = Queue()

def process_message_queue():
    """Обрабатывает очередь сообщений для ассистентов."""
    while True:
        try:
            task = message_queue.get()
            if task is None:
                break  # Завершаем поток
            user_id, candidate_id, message, task_type = task

            if task_type == "filter":
                logger.info(f"Обработка фильтрации для пользователя {user_id}...")
                analyze_message_and_update_candidate(user_id, candidate_id, message)
            
            elif task_type == "response":
                logger.info(f"Генерация ответа для пользователя {user_id}...")
                response = generate_response("friendly", message)
                logger.info(f"Ответ: {response}")
            
            elif task_type == "chat":
                logger.info(f"Запрос чата для пользователя {user_id}...")
                report = handle_user_query(user_id, "candidate_report")
                logger.info(f"Результат отчета: {report}")
            
            message_queue.task_done()
        except Exception as e:
            logger.error(f"Ошибка при обработке задачи в очереди: {e}")

def main():
    try:
        # Инициализация базы данных
        logger.info("Инициализация базы данных...")
        init_db()

        # Запуск обработки очереди в отдельном потоке
        logger.info("Запуск обработки очереди сообщений...")
        queue_thread = Thread(target=process_message_queue, daemon=True)
        queue_thread.start()

        # Добавление тестовых задач в очередь
        message_queue.put((12345, 1, "Пример сообщения для фильтрации", "filter"))
        message_queue.put((12345, None, "Пример запроса для генерации ответа", "response"))
        message_queue.put((12345, None, None, "chat"))

        # Запуск Telegram-бота
        logger.info("Запуск Telegram-бота...")
        start_bot(API_TOKEN)

        # Ожидание завершения обработки очереди
        message_queue.join()
        logger.info("Все задачи в очереди выполнены.")

    except Exception as e:
        logger.error(f"Ошибка в работе приложения: {e}")

if __name__ == "__main__":
    main()
