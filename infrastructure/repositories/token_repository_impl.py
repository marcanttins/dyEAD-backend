# backend/infrastructure/repositories/token_repository_impl.py
from typing import Optional

from domain.entities.revoked_token import RevokedToken as RevokedTokenEntity
from domain.repositories.token_repository import ITokenRepository
from infrastructure.extensions import db
from infrastructure.orm.models.revoked_token import RevokedToken as RevokedTokenModel


class TokenRepositoryImpl(ITokenRepository):
    def add_revoked(self, jti: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None, device_id: Optional[str] = None) -> RevokedTokenEntity:
        m = RevokedTokenModel(jti=jti, ip_address=ip_address, user_agent=user_agent, device_id=device_id)
        db.session.add(m)
        db.session.commit()
        return RevokedTokenEntity(
            id=m.id,
            jti=m.jti,
            revoked_at=m.revoked_at,
            ip_address=m.ip_address,
            user_agent=m.user_agent,
            device_id=m.device_id
        )

    def is_revoked(self, jti: str) -> bool:
        return db.session.query(RevokedTokenModel).filter_by(jti=jti).count() > 0

    def get_revoked(self, jti: str) -> Optional[RevokedTokenEntity]:
        m = RevokedTokenModel.query.filter_by(jti=jti).first()
        if not m:
            return None
        return RevokedTokenEntity(
            id=m.id,
            jti=m.jti,
            revoked_at=m.revoked_at,
            ip_address=m.ip_address,
            user_agent=m.user_agent,
            device_id=m.device_id
        )
