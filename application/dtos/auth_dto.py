# backend/application/dtos/auth_dto.py

from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class AuthTokensDTO:
    """
    DTO para transportar os tokens JWT como strings.
    """
    access_token: str
    refresh_token: Optional[str] = None
