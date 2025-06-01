# backend/infrastructure/orm/models/user.py
from datetime import datetime, timezone
from sqlalchemy import Enum as SAEnum
from infrastructure.extensions import db
from domain.entities.user import UserRole

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(
        SAEnum(UserRole, name='user_role', native_enum=False),
        default=UserRole.ALUNO,
        server_default=UserRole.ALUNO.value,
        nullable=False
    )
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    def __repr__(self):
        return f"<User id={self.id} email={self.email!r}>"