# backend/application/use_cases/refresh_token_use_case.py
from domain.repositories.token_repository import ITokenRepository
from application.dtos.auth_dto import AuthTokensDTO
from datetime import datetime, timedelta, timezone
import uuid

class RefreshTokenUseCase:
    def __init__(
        self,
        token_repo: ITokenRepository,
        access_expires: timedelta
    ):
        self.token_repo = token_repo
        self.access_expires = access_expires

    def execute(self, refresh_jti: str) -> AuthTokensDTO:
        if self.token_repo.is_revoked(refresh_jti):
            raise ValueError("Refresh token revogado")

        self.token_repo.add_revoked(refresh_jti)
        now = datetime.now(tz=timezone.utc)
        new_jti = str(uuid.uuid4())
        access_token = {
            "jti": new_jti,
            "exp": now + self.access_expires
        }
        return AuthTokensDTO(
            access_token=access_token,
            refresh_token=None
        )
