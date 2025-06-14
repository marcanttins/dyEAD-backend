# backend/infrastructure/orm/models/feedback.py
from datetime import datetime, timezone
from infrastructure.extensions import db

class Feedback(db.Model):
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(20), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user = db.relationship('User', backref=db.backref('feedbacks', lazy='dynamic'))
    course = db.relationship('Course', backref=db.backref('feedbacks', lazy='dynamic'))

    def __repr__(self):
        return f"<Feedback id={self.id} user_id={self.user_id} course_id={self.course_id}>"
