# services/assistant_chat.py
import openai
import os
from dotenv import load_dotenv
from services.database import session, CandidateProfile, Conversation
from bot.utils import format_profile, format_date

# Загрузка переменных окружения
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

ASSISTANT_ID = os.getenv("ASSISTANT_ID3")

if not ASSISTANT_ID:
    raise ValueError("ASSISTANT_ID3 не задан в .env")

def get_candidate_report(user_id):
    """Формирует отчет о всех кандидатах пользователя."""
    candidates = session.query(CandidateProfile).filter_by(user_id=user_id).all()
    if not candidates:
        return "Кандидаты не найдены."

    report = "Отчет о кандидатах:\n"
    for candidate in candidates:
        profile = {
            "name": candidate.name,
            "age": candidate.age,
            "city": candidate.city,
            "interests": candidate.interests,
            "goals": candidate.goals
        }
        report += format_profile(profile) + "\n"
        report += f"Логический рейтинг: {candidate.logic_score}, Эмоциональный рейтинг: {candidate.emotional_score}\n\n"
    return report

def get_conversation_summary(candidate_id):
    """Возвращает краткий обзор переписки с кандидатом."""
    conversations = (
        session.query(Conversation)
        .filter_by(candidate_id=candidate_id)
        .order_by(Conversation.timestamp.asc())
        .all()
    )
    if not conversations:
        return "Переписка отсутствует."

    summary = "История переписки:\n"
    for conv in conversations:
        summary += f"[{format_date(conv.timestamp)}]: {conv.message}\n"
    return summary

def generate_assistant_response(prompt):
    """Генерирует ответ с использованием ассистента 3."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"Assistant ID: {ASSISTANT_ID}. Вы предоставляете отчеты и информацию по запросу пользователя."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Ошибка генерации ответа: {str(e)}"

def handle_user_query(user_id, query_type, candidate_id=None):
    """Обрабатывает запрос пользователя и формирует соответствующий ответ."""
    if query_type == "candidate_report":
        return get_candidate_report(user_id)

    if query_type == "conversation_summary" and candidate_id:
        return get_conversation_summary(candidate_id)

    if query_type == "custom_prompt":
        prompt = "Введите ваш запрос для ассистента."
        return generate_assistant_response(prompt)

    return "Неизвестный запрос. Попробуйте снова."

# Пример использования
if __name__ == "__main__":
    user_id = 12345
    candidate_id = 1

    # Отчет о кандидатах
    report = handle_user_query(user_id, "candidate_report")
    print(report)

    # Сводка переписки
    summary = handle_user_query(user_id, "conversation_summary", candidate_id)
    print(summary)

    # Кастомный запрос
    custom_response = handle_user_query(user_id, "custom_prompt")
    print(custom_response)
