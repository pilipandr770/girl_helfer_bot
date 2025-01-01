# services/candidate_filter.py
import openai
import os
from dotenv import load_dotenv
from services.database import session, CandidateProfile

# Загрузка переменных окружения
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

ASSISTANT_ID = os.getenv("ASSISTANT_ID1")

if not ASSISTANT_ID:
    raise ValueError("ASSISTANT_ID1 не задан в .env")

def analyze_message_and_update_candidate(user_id, candidate_id, message):
    """Анализирует сообщение кандидата, обновляет его показатели и формирует отчет."""
    # Проверяем, существует ли кандидат
    candidate = session.query(CandidateProfile).filter_by(id=candidate_id).first()

    if not candidate:
        return f"Ошибка: Кандидат с ID {candidate_id} не найден."

    try:
        # Анализ сообщения через OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": (
                    f"Assistant ID: {ASSISTANT_ID1}.\n"
                    "Analyze the candidate's message and determine which life spheres are relevant:\n"
                    "- Communication (⭐)\n"
                    "- Emotional Intelligence (❤️)\n"
                    "- Logic (💡)\n"
                    "- Shared Interests (🔗)\n"
                    "- Creativity (🎨)\n"
                    "- Responsibility (🛡)\n"
                    "- Career (💼)\n"
                    "- Support and Agreement (🤝)\n"
                    "- Overall Harmony (🌀).\n"
                    "Provide changes in the format: logic:+1, emotional:-1, etc."
                )},
                {"role": "user", "content": message}
            ],
            max_tokens=150
        )

        # Получаем анализ от OpenAI
        analysis = response["choices"][0]["message"]["content"].lower()

        # Пример анализа: "logic:+1, emotional:-1"
        changes = {item.split(":")[0].strip(): int(item.split(":")[1].strip())
                   for item in analysis.split(",")}

        # Обновляем карточку кандидата
        for sphere, change in changes.items():
            if hasattr(candidate, sphere + "_score"):  # Проверяем, существует ли атрибут
                setattr(candidate, sphere + "_score", getattr(candidate, sphere + "_score") + change)

        session.commit()
        return f"Кандидат обновлен: {changes}"

    except Exception as e:
        return f"Ошибка анализа сообщения: {e}"

def generate_candidate_report(candidate_id):
    """Генерирует отчет о текущем состоянии данных кандидата."""
    candidate = session.query(CandidateProfile).filter_by(id=candidate_id).first()
    if not candidate:
        return f"Кандидат с ID {candidate_id} не найден."

    missing_fields = []
    if not candidate.name:
        missing_fields.append("имя")
    if not candidate.age:
        missing_fields.append("возраст")
    if not candidate.city:
        missing_fields.append("город")
    if not candidate.interests:
        missing_fields.append("интересы")
    if not candidate.goals:
        missing_fields.append("цели")

    report = {
        "known": {
            "name": candidate.name,
            "age": candidate.age,
            "city": candidate.city,
            "interests": candidate.interests,
            "goals": candidate.goals,
        },
        "missing": missing_fields
    }
    return report

# Пример использования
def filter_example():
    user_id = 12345
    candidate_id = 1
    message = "Кандидат написал, что он увлекается спортом и любит логические задачи."
    result = analyze_message_and_update_candidate(user_id, candidate_id, message)
    print(result)

if __name__ == "__main__":
    filter_example()
