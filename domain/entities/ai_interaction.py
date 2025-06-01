# backend/domain/entities/ai_interaction.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class AIInteraction:
    id: Optional[int]
    user_id: Optional[int]
    request_text: str
    response_text: str
    created_at: datetime
