# bot/handlers.py
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from services.database import (
    add_candidate_profile,
    get_candidate_profiles,
    filter_candidates,
    delete_candidate_profile,
    update_candidate_profile
)
from services.response_generator import generate_report

# Левое меню кнопок
LEFT_MENU = [
    ["Старт"],
    ["Help"],
    ["Информация о себе"],
    ["Информация о кандидате"],
    ["Выбор языка"]
]
reply_markup_left = ReplyKeyboardMarkup(LEFT_MENU, resize_keyboard=True, one_time_keyboard=True)

# Правое меню кнопок
RIGHT_MENU = [
    ["Инструкции для фильтрации"],
    ["Инструкции для ответов"],
    ["Чат с ассистентом"],
    ["Резерв 1"],
    ["Резерв 2"]
]
reply_markup_right = ReplyKeyboardMarkup(RIGHT_MENU, resize_keyboard=True, one_time_keyboard=True)

async def start(update: Update, context: CallbackContext):
    """Обработчик команды /start."""
    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}! Добро пожаловать в бота. Выберите действие:",
        reply_markup=reply_markup_left,
    )

async def help_handler(update: Update, context: CallbackContext):
    """Инструкция пользования ботом."""
    await update.message.reply_text("Этот бот помогает вам управлять данными профиля и кандидатами.")

async def profile_handler(update: Update, context: CallbackContext):
    """Показать профиль пользователя."""
    user_profile = {"name": "Анна", "age": 28, "city": "Киев", "interests": "Чтение, спорт"}
    await update.message.reply_text(f"Ваш профиль:\n{user_profile}")

async def candidate_info_handler(update: Update, context: CallbackContext):
    """Показать параметры желаемого кандидата."""
    candidate_profile = {"age": "25-30", "city": "Москва", "interests": "Спорт, книги", "goals": "Дружба"}
    await update.message.reply_text(f"Информация о желаемом кандидате:\n{candidate_profile}")

async def change_language_handler(update: Update, context: CallbackContext):
    """Переключение языка на русский."""
    await update.message.reply_text("Язык переключен на русский.")

async def filter_instructions_handler(update: Update, context: CallbackContext):
    """Ввод инструкций для фильтрации."""
    await update.message.reply_text("Введите инструкции для фильтрации данных кандидатов:")
    context.user_data["input_mode"] = "filter_instructions"

async def response_instructions_handler(update: Update, context: CallbackContext):
    """Ввод инструкций для генерации ответов."""
    await update.message.reply_text("Введите инструкции для ассистента по генерации ответов:")
    context.user_data["input_mode"] = "response_instructions"

async def assistant_chat_handler(update: Update, context: CallbackContext):
    """Чат с ассистентом."""
    await update.message.reply_text("Вы можете задать вопрос ассистенту, и он предоставит информацию из базы данных.")

# Резервные кнопки
async def reserve_handler(update: Update, context: CallbackContext):
    await update.message.reply_text("Эта функция пока не реализована.")

def start_bot(api_token):
    """Запуск Telegram-бота с заданным токеном API."""
    from telegram import Bot
    from telegram.ext import Updater, CommandHandler

    bot = Bot(token=api_token)
    updater = Updater(bot=bot)

    # Пример обработчика команды /start
    def start(update, context):
        update.message.reply_text("Привет! Я ваш помощник.")

    start_handler = CommandHandler('start', start)
    updater.dispatcher.add_handler(start_handler)

    # Запуск бота
    updater.start_polling()
    updater.idle()
