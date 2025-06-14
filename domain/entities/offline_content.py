# backend/domain/entities/offline_content.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class OfflineContent:
    id: Optional[int]
    user_id: int
    content_type: str
    content_url: str
    downloaded_at: datetime
