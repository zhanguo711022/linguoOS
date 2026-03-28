from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SessionModel(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True)
    user_id = Column(String, index=True, nullable=False)
    language = Column(String, nullable=True)
    status = Column(String, nullable=False, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LearningRecordModel(Base):
    __tablename__ = "learning_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, index=True, nullable=False)
    action_type = Column(String, nullable=False)
    payload = Column(Text, nullable=False)
    correct = Column(Boolean, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class InterventionModel(Base):
    __tablename__ = "interventions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, index=True, nullable=False)
    reason = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")
    teacher_response = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
