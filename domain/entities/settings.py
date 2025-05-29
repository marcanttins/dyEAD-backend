# backend/domain/entities/settings.py
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

@dataclass
class Settings:
    id: Optional[int]
    user_id: int
    preferences: Dict[str, Any]
    updated_at: Optional[datetime]
