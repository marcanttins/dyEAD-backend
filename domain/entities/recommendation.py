# backend/domain/entities/recommendation.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Recommendation:
    id: Optional[int]
    user_id: int
    course_id: Optional[int]
    recommendation_text: str
    created_at: datetime
    updated_at: Optional[datetime]
