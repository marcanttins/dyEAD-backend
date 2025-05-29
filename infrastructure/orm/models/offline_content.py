# backend/infrastructure/orm/models/offline_content.py
from datetime import datetime, timezone
from infrastructure.extensions import db

class OfflineContent(db.Model):
    __tablename__ = 'offline_contents'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_type = db.Column(db.String(100), nullable=False)
    content_url = db.Column(db.String(500), nullable=False)
    downloaded_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user = db.relationship('User', backref=db.backref('offline_contents', lazy='dynamic'))

    def __repr__(self):
        return f"<OfflineContent id={self.id} content_type={self.content_type!r}>"