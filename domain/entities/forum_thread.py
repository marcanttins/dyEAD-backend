# backend/domain/entities/forum_thread.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ForumThread:
    id: Optional[int]
    title: str
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]
