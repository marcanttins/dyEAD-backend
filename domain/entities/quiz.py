# backend/domain/entities/quiz.py
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Quiz:
    id: Optional[int]
    course_id: int
    title: str
    created_at: datetime

@dataclass
class QuizQuestion:
    id: Optional[int]
    quiz_id: int
    text: str
    options: List[str]
    correct_option: int
