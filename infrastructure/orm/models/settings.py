# backend/infrastructure/orm/models/settings.py
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import JSONB
from infrastructure.extensions import db

class Settings(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    preferences = db.Column(JSONB, nullable=False)
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user = db.relationship('User', backref=db.backref('settings', uselist=False))

    def __repr__(self):
        return f"<Settings user_id={self.user_id}>"
