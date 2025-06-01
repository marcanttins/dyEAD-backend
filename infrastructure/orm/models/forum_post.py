# backend/infrastructure/orm/models/forum_post.py
from datetime import datetime, timezone
from infrastructure.extensions import db

class ForumPost(db.Model):
    __tablename__ = 'forum_posts'

    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('forum_threads.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    thread = db.relationship('ForumThread', backref=db.backref('posts', lazy='dynamic'))
    user = db.relationship('User', backref=db.backref('posts', lazy='dynamic'))

    def __repr__(self):
        return f"<ForumPost id={self.id} thread_id={self.thread_id}>"
