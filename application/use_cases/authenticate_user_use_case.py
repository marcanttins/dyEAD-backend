# backend/application/use_cases/authenticate_user_use_case.py

from flask_jwt_extended import create_access_token, create_refresh_token
from application.dtos.auth_dto import AuthTokensDTO
from domain.repositories.user_repository import IUserRepository
from werkzeug.security import check_password_hash
from domain.exceptions import APIError

class AuthenticateUserUseCase:
    """
    Caso de uso para autenticar usuário e emitir tokens JWT.
    """

    def __init__(
        self,
        user_repo: IUserRepository,
        access_expires,
        refresh_expires
    ):
        self.user_repo = user_repo
        self.access_expires = access_expires
        self.refresh_expires = refresh_expires

    def execute(self, email: str, password: str) -> AuthTokensDTO:
        # Verifica credenciais
        user = self.user_repo.get_by_email(email)
        if not user or not check_password_hash(user.password_hash, password):
            raise APIError("Credenciais inválidas", status_code=401)

        # Gera os JWTs como strings
        access_jwt  = create_access_token(identity=user, expires_delta=self.access_expires)
        refresh_jwt = create_refresh_token(identity=user, expires_delta=self.refresh_expires)

        return AuthTokensDTO(
            access_token=access_jwt,
            refresh_token=refresh_jwt
        )
