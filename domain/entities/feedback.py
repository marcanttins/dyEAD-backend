# backend/domain/entities/feedback.py
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class FeedbackSentiment(Enum):
    POSITIVO = "positivo"
    NEGATIVO = "negativo"
    NEUTRO = "neutro"

@dataclass
class Feedback:
    id: Optional[int]
    user_id: int
    course_id: Optional[int]
    message: str
    sentiment: FeedbackSentiment
    created_at: datetime
