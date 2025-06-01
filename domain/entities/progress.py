# backend/domain/entities/progress.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Progress:
    id: Optional[int]
    user_id: int
    course_id: int
    percentage: float
    last_updated: Optional[datetime]
