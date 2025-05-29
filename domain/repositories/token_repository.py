# backend/domain/repositories/token_repository.py
from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.revoked_token import RevokedToken

class ITokenRepository(ABC):
    @abstractmethod
    def add_revoked(self, jti: str, ip_address: str = None, user_agent: str = None, device_id: str = None) -> RevokedToken:
        """Adiciona um token à lista de revogados."""
        pass

    @abstractmethod
    def is_revoked(self, jti: str) -> bool:
        """Verifica se um token foi revogado."""
        pass

    @abstractmethod
    def get_revoked(self, jti: str) -> Optional[RevokedToken]:
        """Retorna o RevokedToken ou None se não existir."""
        pass
