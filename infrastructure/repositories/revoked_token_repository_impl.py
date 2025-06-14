# backend/infrastructure/repositories/revoked_token_repository_impl.py
from typing import Optional
from datetime import datetime, timezone

from infrastructure.extensions import db
from infrastructure.orm.models.revoked_token import RevokedToken as RevokedTokenModel
from domain.repositories.revoked_token_repository import IRevokedTokenRepository
from domain.entities.revoked_token import RevokedToken

class RevokedTokenRepositoryImpl(IRevokedTokenRepository):
    """
    Implementação de IRevokedTokenRepository usando SQLAlchemy.
    """

    def add(
        self,
        jti: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        device_id: Optional[str] = None
    ) -> RevokedToken:
        """
        Revoga um token, salvando metadados e retornando a entidade de domínio.
        """
        model = RevokedTokenModel(
            jti=jti,
            revoked_at=datetime.now(timezone.utc),
            ip_address=ip_address,
            user_agent=user_agent,
            device_id=device_id
        )
        db.session.add(model)
        db.session.commit()
        return RevokedToken(
            id=model.id,
            jti=model.jti,
            revoked_at=model.revoked_at,
            ip_address=model.ip_address,
            user_agent=model.user_agent,
            device_id=model.device_id
        )

    def is_revoked(self, jti: str) -> bool:
        """
        Verifica se um token com o JTI informado está revogado.
        """
        return db.session.query(RevokedTokenModel) \
            .filter_by(jti=jti) \
            .first() is not None

    def get(self, jti: str) -> Optional[RevokedToken]:
        """
        Recupera o registro de token revogado pelo JTI, ou None se não existir.
        """
        model = db.session.query(RevokedTokenModel).filter_by(jti=jti).first()
        if model is None:
            return None
        return RevokedToken(
            id=model.id,
            jti=model.jti,
            revoked_at=model.revoked_at,
            ip_address=model.ip_address,
            user_agent=model.user_agent,
            device_id=model.device_id
        )
