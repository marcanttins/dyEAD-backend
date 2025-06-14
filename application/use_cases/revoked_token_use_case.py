# backend/application/use_cases/revoke_token_use_case.py

from typing import Optional
from domain.repositories.revoked_token_repository import IRevokedTokenRepository
from domain.entities.revoked_token import RevokedToken

class RevokedTokenUseCase:
    """
    Use Case para revogar um JWT, persistindo seus metadados.
    """

    def __init__(self, revoked_repo: IRevokedTokenRepository):
        self._revoked_repo = revoked_repo

    def execute(
        self,
        jti: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        device_id: Optional[str] = None
    ) -> RevokedToken:
        """
        Revoga o token identificado por `jti`, armazenando também ip, user_agent e device_id.

        Retorna a entidade RevokedToken criada.
        """
        return self._revoked_repo.add(
            jti=jti,
            ip_address=ip_address,
            user_agent=user_agent,
            device_id=device_id
        )
