# backend/domain/repositories/revoked_token_repository.py

from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.revoked_token import RevokedToken

class IRevokedTokenRepository(ABC):
    """
    Interface para persistência de tokens revogados.
    """

    @abstractmethod
    def add(
        self,
        jti: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        device_id: Optional[str] = None
    ) -> RevokedToken:
        """
        Revoga um token, persistindo os metadados de jti, ip, user_agent e device_id.
        Retorna a entidade de domínio RevokedToken criada.
        """
        pass

    @abstractmethod
    def is_revoked(self, jti: str) -> bool:
        """
        Retorna True se o jti informado estiver revogado.
        """
        pass

    @abstractmethod
    def get(self, jti: str) -> Optional[RevokedToken]:
        """
        Recupera o registro de token revogado pelo seu jti,
        ou None caso não exista.
        """
        pass
