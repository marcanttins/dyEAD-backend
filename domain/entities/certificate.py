# backend/domain/entities/certificate.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Certificate:
    id: Optional[int]
    user_id: int
    course_id: int
    issue_date: datetime
    file_url: str
