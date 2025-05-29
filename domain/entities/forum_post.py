# backend/domain/entities/forum_post.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ForumPost:
    id: Optional[int]
    thread_id: int
    user_id: int
    content: str
    created_at: datetime
