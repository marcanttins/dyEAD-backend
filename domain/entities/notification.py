# backend/domain/entities/notification.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Notification:
    id: Optional[int]
    user_id: int
    message: str
    read_status: bool
    created_at: datetime
