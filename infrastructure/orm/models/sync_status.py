# backend/infrastructure/orm/models/sync_status.py
from datetime import datetime, timezone
from infrastructure.extensions import db

class SyncStatus(db.Model):
    __tablename__ = 'sync_status'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    last_sync = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user = db.relationship('User', backref=db.backref('sync_status', uselist=False))

    def __repr__(self):
        return f"<SyncStatus user_id={self.user_id} status={self.status}>"