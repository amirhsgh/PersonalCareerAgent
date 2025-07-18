from sqlalchemy import String, Column, Integer, Boolean, DateTime, Text, ForeignKey, Enum
from ..core.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=None, nullable=True)


class ResumeUpload(Base):
    __tablename__ = 'resume_uploads'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    extracted_text = Column(Text)
    uploaded_at = Column(DateTime, default=datetime.now(timezone.utc))

    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship("User")

    chat_session = relationship("CareerChatSession", back_populates='resume')


class CareerChatSession(Base):
    __tablename__ = "career_chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    started_at = Column(DateTime, default=datetime.now(timezone.utc))
    resume_id = Column(Integer, ForeignKey("resume_uploads.id"))

    resume = relationship("ResumeUpload", back_populates="chat_session")
    messages = relationship("CareerChatMessage", back_populates="session")


class CareerChatMessage(Base):
    __tablename__ = "career_chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(Enum("user", "agent", name="chat_roles"))
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))

    session_id = Column(Integer, ForeignKey("career_chat_sessions.id"))
    session = relationship("CareerChatSession", back_populates="messages")
