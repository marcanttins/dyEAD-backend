# backend/infrastructure/orm/models/revoked_token.py
from datetime import datetime, timezone
from infrastructure.extensions import db

class RevokedToken(db.Model):
    __tablename__ = 'revoked_tokens'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), unique=True, nullable=False)
    revoked_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    device_id = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<RevokedToken jti={self.jti}>"