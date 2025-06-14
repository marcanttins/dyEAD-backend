from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from infrastructure.database import db

class LessonType(str, Enum):
    VIDEO = 'video'
    QUIZ = 'quiz'
    MATERIAL = 'material'

class LessonStatus(str, Enum):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'

class Lesson(db.Model):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000))
    type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default=LessonStatus.DRAFT.value)
    duration = Column(Integer, nullable=False)
    video_url = Column(String(2048))
    material_url = Column(String(2048))
    questions = Column(JSON)
    progress = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)

    course = relationship('Course', back_populates='lessons')
