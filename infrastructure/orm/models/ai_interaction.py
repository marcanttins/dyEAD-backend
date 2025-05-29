# backend/infrastructure/orm/models/ai_interaction.py
from datetime import datetime, timezone
from infrastructure.extensions import db

class AIInteraction(db.Model):
    __tablename__ = 'ai_interactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    request_text = db.Column(db.Text, nullable=False)
    response_text = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user = db.relationship('User', backref=db.backref('ai_interactions', lazy='dynamic'))

    def __repr__(self):
        return f"<AIInteraction id={self.id} user_id={self.user_id}>"