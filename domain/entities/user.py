# backend/domain/entities/user.py
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class UserRole(Enum):
    aluno = "aluno"
    instrutor = "instrutor"
    admin = "admin"

@dataclass
class User:
    id: Optional[int]
    name: str
    email: str
    password_hash: str
    role: UserRole
    created_at: datetime
    updated_at: Optional[datetime]
