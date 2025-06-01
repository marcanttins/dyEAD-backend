# backend/infrastructure/orm/models/forum_thread.py
from datetime import datetime, timezone
from infrastructure.extensions import db

class ForumThread(db.Model):
    __tablename__ = 'forum_threads'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
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

    user = db.relationship('User', backref=db.backref('threads', lazy='dynamic'))

    def __repr__(self):
        return f"<ForumThread id={self.id} title={self.title!r}>"
