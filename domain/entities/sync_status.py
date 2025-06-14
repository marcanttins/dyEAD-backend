# backend/domain/entities/sync_status.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class SyncStatus:
    id: Optional[int]
    user_id: int
    status: str
    last_sync: datetime
