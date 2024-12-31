# models/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Float
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class UserProfile(Base):
    """Таблица профилей пользователей."""
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)  # Telegram ID пользователя
    profile_text = Column(Text, nullable=True)  # Анкета пользователя
    desired_characteristics = Column(Text, nullable=True)  # Желаемые характеристики кандидата
    conversations = relationship("Conversation", back_populates="user")
    candidates = relationship("CandidateProfile", back_populates="user")

class CandidateProfile(Base):
    """Таблица профилей кандидатов."""
    __tablename__ = 'candidate_profiles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profiles.id'), nullable=False)
    name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    city = Column(String, nullable=True)
    interests = Column(Text, nullable=True)
    goals = Column(Text, nullable=True)
    logic_score = Column(Float, default=0.0)  # Логический рейтинг
    emotional_score = Column(Float, default=0.0)  # Эмоциональный рейтинг
    user = relationship("UserProfile", back_populates="candidates")
    conversations = relationship("Conversation", back_populates="candidate")

class Conversation(Base):
    """Таблица переписок."""
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profiles.id'), nullable=False)
    candidate_id = Column(Integer, ForeignKey('candidate_profiles.id'), nullable=True)
    message = Column(Text, nullable=False)  # Текст сообщения
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship("UserProfile", back_populates="conversations")
    candidate = relationship("CandidateProfile", back_populates="conversations")

class Instruction(Base):
    """Таблица инструкций для ассистентов."""
    __tablename__ = 'instructions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profiles.id'), nullable=False)
    assistant_type = Column(String, nullable=False)  # Тип ассистента (e.g., response_style, filtering)
    content = Column(Text, nullable=False)  # Инструкции для ассистента
    user = relationship("UserProfile")

# Завершение файла
