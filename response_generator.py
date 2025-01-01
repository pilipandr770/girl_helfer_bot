# services/response_generator.py
import openai
import os
from dotenv import load_dotenv
from services.database import session, Conversation, CandidateProfile
from models.models import Instruction
from datetime import datetime

# Загрузка переменных окружения
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

ASSISTANT_ID = os.getenv("ASSISTANT_ID2")

if not ASSISTANT_ID:
    raise ValueError("ASSISTANT_ID2 не задан в .env")

def generate_response(instructions, candidate_data):
    """Генерация трех вариантов ответа от ассистента на основе инструкций и данных кандидатов."""
    prompt = f"Инструкции: {instructions}\n\nДанные кандидата: {candidate_data}\n\nСгенерируйте три варианта ответа:"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500
        )
        # Обработка результатов: разделяем варианты по строкам
        response_text = response["choices"][0]["message"]["content"]
        options = [opt.strip() for opt in response_text.split("\n") if opt.strip()]
        return options[:3]  # Возвращаем только первые три варианта
    except Exception as e:
        return [f"Ошибка генерации ответа: {str(e)}"]

def process_conversation(user_id, candidate_id, candidate_message):
    """Обрабатывает сообщение кандидата, генерирует варианты ответов и сохраняет переписку."""
    # Получение инструкций
    instruction = session.query(Instruction).filter_by(user_id=user_id, assistant_type="response_style").first()
    style = instruction.content if instruction else "friendly"

    # Генерация вариантов ответа
    response_options = generate_response(style, candidate_message)

    # Сохранение переписки
    new_message = Conversation(
        user_id=user_id,
        candidate_id=candidate_id,
        message=candidate_message,
        timestamp=datetime.utcnow()
    )
    session.add(new_message)
    session.commit()

    return {
        "response_options": response_options,
        "conversation_history": get_conversation_history(candidate_id)
    }

def get_conversation_history(candidate_id):
    """Получает историю переписки с кандидатом."""
    conversations = session.query(Conversation).filter_by(candidate_id=candidate_id).order_by(Conversation.timestamp.asc()).all()
    return [
        {"message": conv.message, "timestamp": conv.timestamp} for conv in conversations
    ]

def generate_report(candidate_id):
    """Генерация отчета о кандидате."""
    candidate = session.query(CandidateProfile).filter_by(id=candidate_id).first()
    if not candidate:
        return f"Кандидат с ID {candidate_id} не найден."

    report = {
        "name": candidate.name,
        "age": candidate.age,
        "city": candidate.city,
        "interests": candidate.interests,
        "goals": candidate.goals,
        "logic_score": candidate.logic_score,
        "emotional_score": candidate.emotional_score
    }
    return report

# Пример использования
if __name__ == "__main__":
    user_id = 12345
    candidate_id = 1
    candidate_message = "Привет! Мне интересно, как работает ваш проект."
    result = process_conversation(user_id, candidate_id, candidate_message)
    print(result)
