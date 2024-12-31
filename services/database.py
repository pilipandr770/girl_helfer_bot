# services/database.py
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, DateTime, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

def init_engine():
    """Инициализация подключения к базе данных."""
    engine = create_engine("sqlite:///girl_helper.db", echo=False)
    Base.metadata.create_all(engine)
    return engine

def init_db():
    """Инициализация базы данных."""
    Base.metadata.create_all(engine)

# Инициализация сессии
engine = init_engine()
Session = sessionmaker(bind=engine)
session = Session()

# Таблицы базы данных
class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)  # Telegram ID пользователя
    profile_text = Column(Text, nullable=True)  # Анкета пользователя
    desired_characteristics = Column(Text, nullable=True)  # Желаемые характеристики кандидата
    conversations = relationship("Conversation", back_populates="user")
    candidates = relationship("CandidateProfile", back_populates="user")

class CandidateProfile(Base):
    __tablename__ = 'candidate_profiles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profiles.id'), nullable=False)
    name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    city = Column(String, nullable=True)
    interests = Column(Text, nullable=True)
    goals = Column(Text, nullable=True)
    logic_score = Column(Float, default=0)  # Логический рейтинг
    emotional_score = Column(Float, default=0)  # Эмоциональный рейтинг
    user = relationship("UserProfile", back_populates="candidates")
    conversations = relationship("Conversation", back_populates="candidate")

class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profiles.id'), nullable=False)
    candidate_id = Column(Integer, ForeignKey('candidate_profiles.id'), nullable=True)
    message = Column(Text, nullable=False)  # Текст сообщения
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship("UserProfile", back_populates="conversations")
    candidate = relationship("CandidateProfile", back_populates="conversations")

# Функции для работы с базой данных
def add_user_profile(user_id, profile_text, desired_characteristics):
    """Добавление профиля пользователя."""
    user = UserProfile(user_id=user_id, profile_text=profile_text, desired_characteristics=desired_characteristics)
    session.add(user)
    session.commit()
    return user

def get_user_profile(user_id):
    """Получение профиля пользователя по Telegram ID."""
    return session.query(UserProfile).filter_by(user_id=user_id).first()

def add_candidate_profile(user_id, name, age, city, interests, goals):
    """Добавление профиля кандидата."""
    candidate = CandidateProfile(user_id=user_id, name=name, age=age, city=city, interests=interests, goals=goals)
    session.add(candidate)
    session.commit()
    return candidate

def get_candidate_profiles(user_id):
    """Получение всех профилей кандидатов для пользователя."""
    return session.query(CandidateProfile).filter_by(user_id=user_id).all()

def delete_candidate_profile(candidate_id):
    """Удаление профиля кандидата."""
    candidate = session.query(CandidateProfile).filter_by(id=candidate_id).first()
    if candidate:
        session.delete(candidate)
        session.commit()
        return True
    return False

def filter_candidates(user_id, filters):
    """
    Фильтрует кандидатов на основе заданных критериев.
    """
    query = session.query(CandidateProfile).filter_by(user_id=user_id)
    for key, value in filters.items():
        if hasattr(CandidateProfile, key):
            query = query.filter(getattr(CandidateProfile, key) == value)
    return query.all()

def update_candidate_rating(candidate_id, logic_score=None, emotional_score=None):
    """Обновление рейтинга кандидата."""
    candidate = session.query(CandidateProfile).filter_by(id=candidate_id).first()
    if candidate:
        if logic_score is not None:
            candidate.logic_score = logic_score
        if emotional_score is not None:
            candidate.emotional_score = emotional_score
        session.commit()
        return candidate
    return None

def update_candidate_profile(candidate_id, name=None, age=None, city=None, interests=None, goals=None):
    """Обновление профиля кандидата."""
    candidate = session.query(CandidateProfile).filter_by(id=candidate_id).first()
    if candidate:
        if name is not None:
            candidate.name = name
        if age is not None:
            candidate.age = age
        if city is not None:
            candidate.city = city
        if interests is not None:
            candidate.interests = interests
        if goals is not None:
            candidate.goals = goals
        session.commit()
        return candidate
    return None

def add_conversation(user_id, candidate_id, message):
    """Добавление записи о переписке."""
    conversation = Conversation(user_id=user_id, candidate_id=candidate_id, message=message)
    session.add(conversation)
    session.commit()
    return conversation

def get_conversations(user_id, candidate_id=None):
    """Получение переписки с кандидатом."""
    if candidate_id:
        return session.query(Conversation).filter_by(user_id=user_id, candidate_id=candidate_id).all()
    return session.query(Conversation).filter_by(user_id=user_id).all()

# Завершение файла
