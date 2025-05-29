# backend/domain/entities/revoked_token.py
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class RevokedToken:
    id: uuid.UUID
    jti: str
    revoked_at: datetime
    ip_address: Optional[str]
    user_agent: Optional[str]
    device_id: Optional[str]
